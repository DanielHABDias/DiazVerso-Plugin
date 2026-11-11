import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {entranceProgress, verifyPalette, wordAtFrame} from './kinetic-text-math.mjs';

export type TimedWord = {text:string;startFrame:number;durationFrames:number};

/** kinetic-text: word-by-word kinetic typography with an opaque, verified-color panel.
 * Provide real measured/aligned timings in scene-relative frames. This
 * component does not align speech, load fonts, render or publish on its own.
 * Anton is a preference; pass a host-installed/licensed font separately.
 */
export const DiazKineticText: React.FC<{
  words: TimedWord[]; sceneDurationFrames:number;
  foreground?:string; background?:string;
  fontFamily?:string; fontSize?:number; safeWidthPercent?:number;
  position?:'center'|'lower';
}> = ({words,sceneDurationFrames,foreground='#FFFFFF',background='#121212',
      fontFamily='Anton, Impact, sans-serif',fontSize=82,
      safeWidthPercent=76,position='center'}) => {
  const frame=useCurrentFrame();
  const palette=verifyPalette(foreground,background,{largeText:false});
  if(!palette.passes) throw new Error('Text contrast below 4.5:1');
  if(!(Number.isFinite(fontSize)&&fontSize>0&&fontSize<=200)) throw new Error('Invalid font size');
  if(!(Number.isFinite(safeWidthPercent)&&safeWidthPercent>=30&&safeWidthPercent<=80))
    throw new Error('Unsafe text width');
  const word=wordAtFrame(words,sceneDurationFrames,frame);
  const progress=word?entranceProgress(word,frame):0;
  return <AbsoluteFill style={{justifyContent:position==='lower'?'flex-end':'center',
      alignItems:'center',paddingBottom:position==='lower'?'20%':0,pointerEvents:'none'}}>
    {word&&<div style={{
      width:`${safeWidthPercent}%`,boxSizing:'border-box',textAlign:'center',
      padding:'18px 22px',borderRadius:12,backgroundColor:background,color:foreground,
      fontFamily,fontSize,fontWeight:800,lineHeight:1.12,
      transform:`translateY(${(1-progress)*24}px) scale(${0.92+progress*0.08})`,
      opacity:progress,overflowWrap:'anywhere'
    }}>{word.text}</div>}
  </AbsoluteFill>;
};
