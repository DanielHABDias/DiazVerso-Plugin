import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {backgroundMotion,stableNoise,validateHQBackground} from './hq-background-math.mjs';

type BackgroundMode = 'solid'|'halftone'|'grid'|'stars'|'film'|'paper';
export type HQBackgroundProps = {
  mode?: BackgroundMode;
  baseColor?: string;
  opacity?: number;
  gridColor?: string;
  paperTone?: 'light'|'dark';
};

/** Procedural HQ component using local, frame-based parameters. */
export const HQBackground:React.FC<HQBackgroundProps> = (props) => {
  const {mode,baseColor,opacity,gridColor,paperTone}=validateHQBackground(props);
  const frame=useCurrentFrame();
  const {fps,width,height}=useVideoConfig();
  const motion=backgroundMotion(frame,fps,mode);
  const dotScale=Math.max(12,Math.round(Math.min(width,height)*.022));
  if(opacity===0) return null;
  const backdrop = paperTone==='light'?'#EDE8DC':'#222733';
  const bg=mode==='paper'?backdrop:mode==='film'?'#11141A':baseColor;
  const faintDots={backgroundImage:'radial-gradient(circle, rgba(2,6,13,.26) 1.5px, transparent 2px)',
    backgroundSize:`${dotScale}px ${dotScale}px`};
  return <AbsoluteFill style={{overflow:'hidden',pointerEvents:'none',opacity:opacity/100,backgroundColor:bg}}>
    {mode==='halftone'&&<AbsoluteFill style={faintDots}/>}
    {mode==='grid'&&<AbsoluteFill style={{backgroundImage:
      `linear-gradient(to right, ${gridColor}77 1px, transparent 1px),linear-gradient(to bottom, ${gridColor}77 1px, transparent 1px)`,
      backgroundSize:'84px 84px',backgroundPosition:`${motion.gridOffset}px 0px`}}/>}
    {mode==='paper'&&<>
      <AbsoluteFill style={{backgroundImage:'repeating-linear-gradient(118deg, transparent 0px, rgba(0,0,0,.09) 2px, transparent 5px, transparent 118px)',
        transform:`translateX(${(motion.paperPose-4)*2}px)`,opacity:.8}}/>
      <AbsoluteFill style={faintDots}/>
    </>}
    {mode==='film'&&<>
      {Array.from({length:9},(_,i)=>{
        const x=stableNoise(i,motion.filmTick)*width;
        return <div key={i} style={{position:'absolute',left:x,top:0,bottom:0,
          width:i%3===0?2:1,backgroundColor:'#E5D7B3',opacity:.05+stableNoise(i,11)*.08}}/>;
      })}
      <AbsoluteFill style={{background:'radial-gradient(ellipse,transparent 26%,rgba(0,0,0,.55) 100%)'}}/>
    </>}
    {mode==='stars'&&<svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
      {Array.from({length:95},(_,i)=>{
        const phase=(stableNoise(i,3)+motion.starPhase)%1;
        const x=stableNoise(i,23)*width,y=stableNoise(i,79)*height;
        return <circle key={i} cx={x} cy={y} r={.8+2.1*phase}
          fill={i%7===0?'#BFD2FF':'#F7F4E9'} opacity={.18+.7*phase}/>;
      })}
    </svg>}
  </AbsoluteFill>;
};
