import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {overlayMotion,tagInk,validateHQOverlay} from '../../references/motion/hq-overlay-math.mjs';

export type HQOverlayProps = {
  upperText:string;
  lowerText:string;
  tagColor?:string;
  compactAt?:number;
  compactDuration?:number;
  compactScale?:number;
};

/** G06 part 2: independent HQ overlay. Uses system fonts deliberately:
 * no @remotion/fonts, Content Lab, canvas, HQComicPage or third-party media.
 */
export const HQOverlay:React.FC<HQOverlayProps> = (props) => {
  const params=validateHQOverlay(props);
  const frame=useCurrentFrame();
  const {fps,width,height}=useVideoConfig();
  const state=overlayMotion(frame,fps,width,height,params);
  const {unit,isWide}=state;
  const paper='#F5EFDE';
  const ink='#111723';
  const font='Arial, Helvetica, sans-serif';
  const lower=params.lowerText.toLocaleUpperCase('pt-BR');
  const upper=params.upperText.toLocaleUpperCase('pt-BR');
  const fontSize=Math.max(32*unit,Math.min(90*unit,
    width*(lower.length>28?.055:lower.length>19?.07:.088)));
  return <AbsoluteFill style={{background:'transparent',pointerEvents:'none',overflow:'hidden'}}>
    <div style={{position:'absolute',top:'3%',left:'5%',color:paper,
      fontFamily:font,fontSize:Math.max(25,30*unit),fontWeight:900,
      textShadow:'1px 2px 2px #05060B',opacity:state.reveal}}>
      {upper}
    </div>
    <div style={{position:'absolute',left:'5%',right:isWide?'30%':'5%',
      bottom:isWide?'6%':'13%',transform:`scale(${state.scale})`,
      transformOrigin:'left bottom',opacity:state.reveal,
      filter:`drop-shadow(${6*unit}px ${8*unit}px 0 #05060B)`}}>
      <div style={{display:'inline-block',background:params.tagColor,
        color:tagInk(params.tagColor),border:`${3*unit}px solid #0D1016`,
        padding:`${6*unit}px ${16*unit}px`,fontFamily:font,
        fontSize:Math.max(21,27*unit),fontWeight:900,
        clipPath:`inset(0 ${(1-state.tagReveal)*100}% 0 0)`}}>
        {upper}
      </div>
      <div style={{background:paper,border:`${5*unit}px solid #080B11`,
        color:ink,padding:`${18*unit}px ${22*unit}px`,
        fontFamily:font,fontWeight:900,fontSize,
        lineHeight:1.04,overflowWrap:'anywhere',
        clipPath:`inset(0 ${(1-state.titleReveal)*100}% 0 0)`}}>
        {lower}
      </div>
    </div>
  </AbsoluteFill>;
};
