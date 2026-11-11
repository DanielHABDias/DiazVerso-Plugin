import React from 'react';
import {AbsoluteFill,Easing,interpolate,useCurrentFrame} from 'remotion';
export type CameraKeyframe={frame:number;x:number;y:number;zoom:number;roll?:number};
export function narrativeCameraPose(frame:number,keyframes:CameraKeyframe[]){
 if(keyframes.length<2||keyframes[0].frame!==0)throw Error('At least two camera keyframes starting at zero are required');
 keyframes.forEach((key,i)=>{
  if(!Number.isSafeInteger(key.frame)||key.frame<0||(i>0&&key.frame<=keyframes[i-1].frame)||![key.x,key.y,key.zoom,key.roll??0].every(Number.isFinite)||key.zoom<=0)throw Error('Invalid camera keyframe');
 });
 const frames=keyframes.map(k=>k.frame),options={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const,easing:Easing.bezier(.72,0,.18,1)};
 return {x:interpolate(frame,frames,keyframes.map(k=>k.x),options),y:interpolate(frame,frames,keyframes.map(k=>k.y),options),zoom:interpolate(frame,frames,keyframes.map(k=>k.zoom),options),roll:interpolate(frame,frames,keyframes.map(k=>k.roll??0),options)};
}
/** Compose a spatial page with motivated camera stops; child layers may use translateZ. */
export const NarrativeCamera:React.FC<{keyframes:CameraKeyframe[];perspective?:number;children:React.ReactNode}> = ({keyframes,perspective=1600,children})=>{
 if(!Number.isFinite(perspective)||perspective<=0)throw Error('Invalid camera perspective');
 const frame=useCurrentFrame(),pose=narrativeCameraPose(frame,keyframes);
 return <AbsoluteFill style={{overflow:'hidden',perspective}}><div style={{position:'absolute',left:'50%',top:'50%',transformOrigin:'0 0',transformStyle:'preserve-3d',transform:`scale(${pose.zoom}) rotateZ(${pose.roll}deg) translate3d(${-pose.x}px,${-pose.y}px,0)`}}>{children}</div></AbsoluteFill>;
};
