import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import {DiazParallax} from '../../references/motion/parallax';
import {DiazKineticText} from '../../references/motion/kinetic-text';
import {HQBackground} from './hq-background';

/** L02/L03: executes an explicit timed plan generated from a test script.
 * The standalone development runner generates WAV audio, a H01 decoupage
 * contract, captions SRT and --props JSON from the SAME original fixture.
 * This component does not fetch/approve assets, transcribe audio or publish.
 */
export type TimedDemoScene = {
  id:string;start_frame:number;duration_frames:number;objective:string;
  narration:string;title:string;cta:boolean;voice_file:string;
  voice_start_frame:number;voice_duration_frames:number;
  caption:{text:string;start_frame:number;duration_frames:number};
};
export type IntegratedPlan = {
  demo_only:true;editorial_approved:false;publishing_performed:false;
  production_id:string;script_version:string;format:'LONGO'|'SHORT';
  fps:number;duration_frames:number;scenes:TimedDemoScene[];
};
export type IntegratedSceneProps = {plan:IntegratedPlan|null};

const SceneContent:React.FC<{scene:TimedDemoScene;kind:'LONGO'|'SHORT'}> =
({scene,kind}) => {
  const {width,height} = useVideoConfig();
  const vertical=kind==='SHORT';
  const imageWidth=vertical?width*.72:width*.45;
  const imageHeight=vertical?height*.32:height*.46;
  const titleSize=vertical?75:82;
  const layers=[
    {id:'background',kind:'background' as const,src:staticFile('i04-background.svg'),
      imageWidth:1080,imageHeight:1920,depth:0.15},
    {id:'nox',kind:'cutout' as const,src:staticFile('i04-nox-canonical.png'),
      imageWidth:1408,imageHeight:768,depth:0.85,
      anchorX:width*.5,anchorY:height*(vertical?.49:.53),
      maxFrameWidth:imageWidth,maxFrameHeight:imageHeight}
  ];
  return <AbsoluteFill style={{overflow:'hidden',backgroundColor:'#0B1423'}}>
    <DiazParallax layers={layers} sceneDurationFrames={scene.duration_frames}/>
    <HQBackground mode="halftone" baseColor="#152741" opacity={11}/>
    <div style={{position:'absolute',left:vertical?130:width*.20,
      top:vertical?342:height*.11,width:vertical?770:width*.60,
      height:vertical?185:180}}>
      <DiazKineticText
        words={[{text:scene.title,startFrame:0,durationFrames:scene.duration_frames}]}
        sceneDurationFrames={scene.duration_frames}
        fontFamily="Impact, Arial, sans-serif" fontSize={titleSize}
        foreground="#FFFFFF" background="#122038" safeWidthPercent={80}/>
    </div>
    <div style={{position:'absolute',left:vertical?130:width*.16,
      top:vertical?1220:height*.76,width:vertical?770:width*.68,
      minHeight:vertical?140:124,padding:vertical?'24px':'20px 32px',
      boxSizing:'border-box',border:'3px solid #B6D1F5',
      borderRadius:16,backgroundColor:'#101C2E',color:'#FFFFFF',
      display:'flex',alignItems:'center',justifyContent:'center',
      fontFamily:'Arial, sans-serif',fontWeight:750,
      fontSize:vertical?40:42,lineHeight:1.24,textAlign:'center'}}>
      {scene.narration}
    </div>
    {scene.cta&&<div style={{
      position:'absolute',left:vertical?175:width*.24,
      top:vertical?1055:height*.60,width:vertical?730:width*.52,
      borderRadius:15,backgroundColor:'#6EDBCF',color:'#0B1423',
      fontFamily:'Arial, sans-serif',fontSize:vertical?35:40,
      fontWeight:850,textAlign:'center',padding:'18px 15px'}}>
      ACOMPANHE O DIAZVERSO
    </div>}
    <div style={{position:'absolute',top:vertical?257:40,left:vertical?130:60,
      fontFamily:'Arial, sans-serif',fontSize:vertical?26:23,
      fontWeight:800,letterSpacing:2.5,color:'#C6DFFF'}}>
      {vertical?'SHORT • TESTE INTEGRADO':'VÍDEO LONGO • TESTE INTEGRADO'}
    </div>
  </AbsoluteFill>;
};

export const IntegratedScene:React.FC<IntegratedSceneProps> = ({plan}) => {
  const {width,height,fps,durationInFrames}=useVideoConfig();
  const kind=(width===1080&&height===1920)?'SHORT':'LONGO';
  if (!plan || !plan.demo_only || plan.editorial_approved!==false ||
      plan.publishing_performed!==false || plan.format!==kind ||
      plan.fps!==fps || plan.duration_frames!==durationInFrames ||
      !plan.scenes?.length) {
    throw new Error('Explicit test-only input props required for integrated renderer');
  }
  let end=0;
  for (const scene of plan.scenes) {
    if (scene.start_frame!==end || scene.duration_frames<=0 ||
        scene.voice_start_frame<0 || scene.voice_duration_frames<1 ||
        scene.voice_start_frame+scene.voice_duration_frames>scene.duration_frames ||
        scene.caption.start_frame!==scene.voice_start_frame ||
        scene.caption.duration_frames!==scene.voice_duration_frames ||
        scene.caption.text!==scene.narration) {
      throw new Error('Invalid or unsynchronized integrated scene timing');
    }
    end+=scene.duration_frames;
  }
  if (end!==durationInFrames) throw new Error('Gapped integrated timeline');
  return <AbsoluteFill style={{backgroundColor:'#0B1423'}}>
    {plan.scenes.map((scene)=> <Sequence key={scene.id}
      from={scene.start_frame} durationInFrames={scene.duration_frames}>
      <SceneContent scene={scene} kind={kind}/>
    </Sequence>)}
    {plan.scenes.map(scene=> <Sequence key={scene.id+'-voice'}
      from={scene.start_frame+scene.voice_start_frame}
      durationInFrames={scene.voice_duration_frames}>
      <Audio src={staticFile(scene.voice_file)} volume={.95}/>
    </Sequence>)}
  </AbsoluteFill>;
};
