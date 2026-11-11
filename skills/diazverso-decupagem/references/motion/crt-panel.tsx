import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useVideoConfig} from 'remotion';
import {planCrtPanel} from './crt-panel-math.mjs';

/** H06: contextual film/TV excerpt with perceptible CRT overlay.
 * No clip acquisition or license determination is performed. Asset rights
 * must be reviewed by a human, and preview/render inspected independently.
 */
export type CrtPanelProps = {
  src: string; rightsStatus: 'APPROVED'; rightsEvidence: string;
  clipStartFrame: number; sceneDurationFrames: number; verifiedSourceFrames: number;
  audioAuthorized?: boolean; audioVolume?: number; scanlineOpacity?: number;
  caption?: string;
};
export const DiazCrtPanel: React.FC<CrtPanelProps> = ({
  src,rightsStatus,rightsEvidence,clipStartFrame,sceneDurationFrames,
  verifiedSourceFrames,audioAuthorized=false,audioVolume=0,scanlineOpacity=0.28,
  caption
}) => {
  const {width,height} = useVideoConfig();
  const panel=planCrtPanel({
    src,rightsStatus,evidence:rightsEvidence,startFrame:clipStartFrame,
    durationFrames:sceneDurationFrames,availableFrames:verifiedSourceFrames,
    outputWidth:width,outputHeight:height,audioAllowed:audioAuthorized,
    audioVolume,scanlineOpacity
  });
  return <AbsoluteFill style={{backgroundColor:'#0D1017',justifyContent:'center',
    alignItems:'center',overflow:'hidden'}}>
    <div style={{position:'absolute',left:panel.panel.left,top:panel.panel.top,
      width:panel.panel.width,height:panel.panel.height,overflow:'hidden',
      border:'9px solid #292E36',borderRadius:22,
      boxShadow:'0 18px 65px rgba(0,0,0,0.65), 0 0 0 3px #565C66',
      backgroundColor:'#08090B'}}>
      <OffthreadVideo src={staticFile(src)} startFrom={clipStartFrame}
        endAt={clipStartFrame+sceneDurationFrames}
        volume={audioAuthorized ? audioVolume : 0}
        style={{width:'100%',height:'100%',objectFit:'contain'}} />
      <div aria-hidden style={{position:'absolute',inset:0,pointerEvents:'none',
        backgroundImage:`repeating-linear-gradient(to bottom, rgba(0,0,0,${scanlineOpacity}) 0px, rgba(0,0,0,${scanlineOpacity}) 2px, transparent 2px, transparent 5px)`,
        boxShadow:'inset 0 0 95px rgba(0,0,0,0.43)',
        mixBlendMode:'multiply'}} />
      <div aria-hidden style={{position:'absolute',inset:0,pointerEvents:'none',
        background:'linear-gradient(115deg, rgba(255,255,255,0.12), transparent 44%, rgba(255,255,255,0.025))'}}/>
    </div>
    {caption && <div style={{position:'absolute',bottom:'4%',maxWidth:'78%',
      background:'#090B0E',color:'#fff',padding:'8px 18px',fontSize:Math.round(height*0.028),
      textAlign:'center',fontFamily:'sans-serif'}}>{caption}</div>}
  </AbsoluteFill>;
};
