import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {cropAndPan} from '../../references/motion/motion-math.mjs';
import {verifyPalette,entranceProgress} from '../../references/motion/kinetic-text-math.mjs';

/** An original generated-color scene that exercises live Remotion hooks.
 * Does not simulate or claim the real Nox/CRT/audio components passed render.
 */
export const SmokeScene:React.FC<{title:string}> = ({title}) => {
 const frame=useCurrentFrame(), {width,height}=useVideoConfig();
 const t=Math.min(1,frame/59);
 const camera=cropAndPan(1408,768,width,height,t,{zoomFrom:1.05,zoomTo:1.15,
   panFrom:[-25,0],panTo:[25,0]});
 const opacity=entranceProgress({startFrame:5,durationFrames:20,endFrame:25,index:0,text:title},frame,12);
 const color=verifyPalette('#FFFFFF','#111827');
 if(!color.passes) throw new Error('Invalid contrast');
 const drift=interpolate(frame,[0,59],[-36,36],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <AbsoluteFill style={{overflow:'hidden',backgroundColor:'#111827'}}>
   <div style={{position:'absolute',left:camera.x,top:camera.y,
     width:camera.width,height:camera.height,
     background:'radial-gradient(circle at 42% 48%, #314E86 5%, #111827 65%)'}}/>
   <div style={{position:'absolute',left:width*0.12+drift,top:height*0.23,
     width:width*0.76,height:height*0.55,
     border:'12px solid #D6DDF3',borderRadius:22,
     boxShadow:'0 18px 55px rgba(0,0,0,0.5)'}}/>
   <div style={{position:'absolute',left:'10%',width:'80%',top:'43%',
     color:'#FFFFFF',fontFamily:'sans-serif',fontWeight:900,fontSize:76,
     backgroundColor:'#111827',borderRadius:12,padding:'20px 24px',
     transform:`translateY(${(1-opacity)*24}px)`,opacity,textAlign:'center'}}>{title}</div>
 </AbsoluteFill>;
};
