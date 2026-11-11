import test from 'node:test';
import assert from 'node:assert/strict';
import {planAudio} from '../references/audio/audio-plan.mjs';
const catalog=()=>[
 {id:'ambient',path:'assets/audio/ambient.wav',kind:'music',rights:'APPROVED',
   evidence:'Autorização registrada e conferida',tags:['tensão'],durationFrames:600},
 {id:'impact',path:'assets/audio/impact.wav',kind:'sfx',rights:'APPROVED',
   evidence:'SFX criado pelo canal',tags:['impacto'],durationFrames:18},
];
const scene=()=>({id:'S01',durationFrames:180,mood:'tensão',
 sfxTags:['impacto'],sfxOffsets:{impacto:42},
 voice:[{startFrame:30,endFrame:120}]});
test('selects approved assets and applies narration ducking',()=>{
 const p=planAudio(catalog(),scene());
 assert.equal(p.status,'READY_FOR_AUDIO_RENDER');
 assert.equal(p.cues.filter(c=>c.kind==='music').length,3);
 assert.equal(p.cues.find(c=>c.duckedForNarration).volume,0.066);
 assert.equal(p.cues.find(c=>c.kind==='sfx').startFrame,42);
 assert.equal(p.synchronizationVerified,false);
});
test('missing approved track is a visible blocker, not an invented asset',()=>{
 const d=scene();d.mood='aventura';
 const p=planAudio(catalog(),d);
 assert.equal(p.status,'NEEDS_APPROVED_AUDIO');
 assert.ok(p.missing.some(c=>c.kind==='music'));
});
test('no music/SFX selected when catalog is empty',()=>{
 const p=planAudio([],scene());
 assert.equal(p.cues.length,0);assert.equal(p.missing.length,2);
});
test('unapproved or undocumented sound is refused',()=>{
 const l=catalog();l[0].rights='PENDING';
 assert.throws(()=>planAudio(l,scene()));
 l[0].rights='APPROVED';l[0].evidence='';
 assert.throws(()=>planAudio(l,scene()));
});
test('remote and traversal sources refused',()=>{
 for(const path of ['https://example.com/a.wav','../secret.wav','/private/a.wav']){
  const l=catalog();l[0].path=path;
  assert.throws(()=>planAudio(l,scene()));
 }
});
test('overlapping voice intervals rejected',()=>{
 const d=scene();d.voice=[{startFrame:30,endFrame:120},{startFrame:110,endFrame:150}];
 assert.throws(()=>planAudio(catalog(),d));
});
test('invalid volume parameters rejected',()=>{
 assert.throws(()=>planAudio(catalog(),scene(),{musicLevel:1.1}));
 assert.throws(()=>planAudio(catalog(),scene(),{duckFactor:-1}));
});
test('SFX cannot exceed available clip or scene',()=>{
 const d=scene();d.sfxOffsets={impacto:175};
 const p=planAudio(catalog(),d);
 assert.equal(p.cues.find(c=>c.kind==='sfx').durationFrames,5);
});
test('duplicate audio IDs rejected',()=>{
 const l=catalog();l.push({...l[1]});
 assert.throws(()=>planAudio(l,scene()));
});
test('source frame reflects music split offset',()=>{
 const p=planAudio(catalog(),scene());
 const after=p.cues.filter(c=>c.kind==='music').at(-1);
 assert.equal(after.startFrame,120);
 assert.equal(after.sourceStartFrame,120);
 assert.equal(after.durationFrames,60);
});
