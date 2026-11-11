/** H07 - deterministic and rights-aware audiovisual cue planner.
 * Runs only on creator-reviewed catalog metadata; no downloads, synthesis,
 * licensing judgments, audio listening, rendering or publishing.
 */
const assertInt=(value,name,allowZero=false)=>{
  if(!Number.isSafeInteger(value) || (allowZero ? value<0 : value<=0))
    throw new Error('Invalid '+name);
};
const validVolume=(v)=>Number.isFinite(v)&&v>=0&&v<=1;
const requireSafeAsset=(asset)=>{
  if(!asset||typeof asset!=='object'||typeof asset.id!=='string'||!asset.id.trim()||
     typeof asset.path!=='string'||!asset.path.trim()||
     /^(https?:|file:|\/|\\|~)/i.test(asset.path)||
     asset.path.split(/[\\/]/).some(part=>!part||part==='.'||part==='..'))
    throw new Error('Unsafe catalog asset');
  if(!['music','sfx'].includes(asset.kind))throw new Error('Unsupported audio kind');
  if(asset.rights!=='APPROVED'||typeof asset.evidence!=='string'||!asset.evidence.trim())
    throw new Error('Catalog contains unapproved or undocumented audio');
  if(!Array.isArray(asset.tags)||!asset.tags.length||asset.tags.some(t=>typeof t!=='string'||!t.trim()))
    throw new Error('Asset requires descriptive tags');
  assertInt(asset.durationFrames,'media duration');
  return asset;
};
const match=(asset,tag)=>asset.tags.some(t=>t.toLocaleLowerCase('pt-BR')===tag.toLocaleLowerCase('pt-BR'));
function intervalsForDucking(durationFrames,voice){
  if(!Array.isArray(voice))throw new Error('Voice interval list required');
  const merged=[];
  for(const v of voice){
    if(!v||typeof v!=='object')throw new Error('Invalid voice interval');
    const {startFrame,endFrame}=v;
    assertInt(startFrame,'voice start',true);assertInt(endFrame,'voice end');
    if(endFrame<=startFrame||endFrame>durationFrames)throw new Error('Voice outside scene');
    if(merged.length&&startFrame<merged.at(-1).endFrame)throw new Error('Overlapping/unsorted voice');
    merged.push({startFrame,endFrame});
  }
  const pieces=[];let cursor=0;
  for(const v of merged){
    if(v.startFrame>cursor)pieces.push({startFrame:cursor,durationFrames:v.startFrame-cursor,duck:false});
    pieces.push({startFrame:v.startFrame,durationFrames:v.endFrame-v.startFrame,duck:true});
    cursor=v.endFrame;
  }
  if(cursor<durationFrames)pieces.push({startFrame:cursor,durationFrames:durationFrames-cursor,duck:false});
  return pieces;
}
/** scene: id, durationFrames, mood, sfxTags[], voice:[{startFrame,endFrame}]
 * output startFrame values are relative to the owning scene.
 * SFX start is zero unless a per-tag offset is supplied in sfxOffsets.
 */
export function planAudio(catalog,scene,{musicLevel=0.22,sfxLevel=0.32,duckFactor=0.3}={}){
  if(!Array.isArray(catalog)||!scene||typeof scene!=='object')throw new Error('Invalid input');
  const {durationFrames,mood,sfxTags=[],voice=[],sfxOffsets={}}=scene;
  assertInt(durationFrames,'scene duration');
  if(typeof mood!=='string'||!mood.trim()||!Array.isArray(sfxTags)||
     sfxTags.some(t=>typeof t!=='string'||!t.trim())||typeof sfxOffsets!=='object'||sfxOffsets===null)
    throw new Error('Invalid audiovisual intent');
  if([musicLevel,sfxLevel,duckFactor].some(v=>!validVolume(v)))throw new Error('Invalid gain parameter');
  const ids=new Set();
  for(const asset of catalog){requireSafeAsset(asset);if(ids.has(asset.id))throw new Error('Duplicate audio ID');ids.add(asset.id);}
  // Deterministic: catalog order determines preference, no popularity claims.
  const music=catalog.find(a=>a.kind==='music'&&match(a,mood)&&a.durationFrames>=durationFrames);
  const cues=[],missing=[];
  if(music) {
    for(const piece of intervalsForDucking(durationFrames,voice)) {
      cues.push({assetId:music.id,kind:'music',path:music.path,
        startFrame:piece.startFrame,sourceStartFrame:piece.startFrame,
        durationFrames:piece.durationFrames,
        volume:Number((piece.duck?musicLevel*duckFactor:musicLevel).toFixed(3)),
        duckedForNarration:piece.duck,rightsEvidence:music.evidence});
    }
  } else {
    // Validate voice even with no matching music.
    intervalsForDucking(durationFrames,voice);
    missing.push({kind:'music',tag:mood,reason:'No approved track of sufficient length'});
  }
  for(const tag of sfxTags){
    const sfx=catalog.find(a=>a.kind==='sfx'&&match(a,tag));
    if(!sfx){missing.push({kind:'sfx',tag,reason:'No approved matching SFX'});continue;}
    const offset=Object.prototype.hasOwnProperty.call(sfxOffsets,tag)?sfxOffsets[tag]:0;
    assertInt(offset,'SFX offset',true);
    if(offset>=durationFrames){missing.push({kind:'sfx',tag,reason:'SFX cue starts outside scene'});continue;}
    cues.push({assetId:sfx.id,kind:'sfx',path:sfx.path,
      startFrame:offset,sourceStartFrame:0,
      durationFrames:Math.min(sfx.durationFrames,durationFrames-offset),
      volume:sfxLevel,duckedForNarration:false,rightsEvidence:sfx.evidence});
  }
  return {status:missing.length?'NEEDS_APPROVED_AUDIO':'READY_FOR_AUDIO_RENDER',
    sceneId:scene.id??null,cues,missing,
    synchronizationVerified:false,listened:false,renderVerified:false,
    publishingPerformed:false};
}
