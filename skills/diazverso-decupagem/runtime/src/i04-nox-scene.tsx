import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {DiazParallax} from '../../references/motion/parallax';
import {DiazKineticText} from '../../references/motion/kinetic-text';
import {HQBackground} from './hq-background';

/** I04 original vertical demonstration. Asset is copied byte-for-byte from the
 * checked canonical assets/brand/nox/Nox.png at build time. The sound is a
 * locally synthesized ORIGINAL whoosh, not an approved third-party SFX.
 * Caption cues describe ON-SCREEN actions. There is NO voice narration here,
 * so this does not demonstrate speech transcription or audio-caption sync.
 */
export const I04NoxScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {width,height,durationInFrames} = useVideoConfig();
  if (width !== 1080 || height !== 1920) throw new Error('I04 is a 9:16 composition');

  const layers = [
    {id:'background',kind:'background' as const,src:staticFile('i04-background.svg'),
      imageWidth:1080,imageHeight:1920,depth:0.18},
    {id:'nox',kind:'cutout' as const,src:staticFile('i04-nox-canonical.png'),
      imageWidth:1408,imageHeight:768,depth:0.92,
      anchorX:width*0.5,anchorY:height*0.48,
      maxFrameWidth:width*.73,maxFrameHeight:height*.32},
  ];
  const words = [
    {text:'NOX',startFrame:0,durationFrames:80},
    {text:'PARALLAX',startFrame:80,durationFrames:80},
    {text:'DIAZVERSO',startFrame:160,durationFrames:80},
  ];
  const captions = [
    {start:0,end:80,text:'O Nox entra no quadro.'},
    {start:80,end:160,text:'As camadas criam profundidade.'},
    {start:160,end:240,text:'Texto e movimento em 9:16.'},
  ];
  const caption = captions.find(c=>frame>=c.start&&frame<c.end);

  return <AbsoluteFill style={{overflow:'hidden',backgroundColor:'#0B1423'}}>
    <DiazParallax layers={layers} sceneDurationFrames={durationInFrames}/>
    <HQBackground mode="halftone" baseColor="#122038" opacity={9}/>
    <div style={{position:'absolute',left:130,top:350,width:770,height:350}}>
      <DiazKineticText words={words} sceneDurationFrames={durationInFrames}
        foreground="#FFFFFF" background="#122038"
        fontFamily="Impact, Arial, sans-serif" fontSize={82}
        safeWidthPercent={76} position="center"/>
    </div>
    <div style={{position:'absolute',left:130,top:1245,width:770,minHeight:160,
      boxSizing:'border-box',borderRadius:18,backgroundColor:'#101C2E',
      border:'3px solid #B6D1F5',color:'#FFFFFF',padding:'24px 30px',
      fontFamily:'Arial, sans-serif',fontSize:43,fontWeight:700,
      lineHeight:1.24,textAlign:'center',display:'flex',
      alignItems:'center',justifyContent:'center'}}>
      {caption?.text ?? ''}
    </div>
    <div style={{position:'absolute',top:259,left:140,color:'#C6DFFF',
      fontFamily:'Arial, sans-serif',fontSize:30,fontWeight:800,letterSpacing:4}}>
      TESTE TÉCNICO • I04
    </div>
    <Sequence from={70}>
      <Audio src={staticFile('i04-whoosh-original.wav')} volume={0.75}/>
    </Sequence>
  </AbsoluteFill>;
};
