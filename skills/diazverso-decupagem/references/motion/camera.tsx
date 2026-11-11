import React from 'react';
import {AbsoluteFill, Img, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {cropAndPan} from './motion-math.mjs';

/** camera camera for a still image, pixel-cover invariant even under pan/zoom.
 * imageWidth/Height must be the ACTUAL media dimensions, not guessed.
 * Runtime preview is still required for content-specific crop/visual QA.
 */
export const DiazCamera: React.FC<{
  src: string; imageWidth: number; imageHeight: number;
  zoomFrom?: number; zoomTo?: number;
  panFrom?: [number, number]; panTo?: [number, number];
  blurStart?: number; blurEnd?: number; sceneDurationFrames: number;
}> = ({src,imageWidth,imageHeight,zoomFrom=1.04,zoomTo=1.12,
      panFrom=[0,0],panTo=[0,0],blurStart=0,blurEnd=0,sceneDurationFrames}) => {
  const frame = useCurrentFrame();
  const {width,height} = useVideoConfig();
  const endFrame=Math.max(1,sceneDurationFrames-1);
  const t=Math.max(0,Math.min(1,frame/endFrame));
  const geom=cropAndPan(imageWidth,imageHeight,width,height,t,{zoomFrom,zoomTo,panFrom,panTo});
  const blur=interpolate(frame,[0,endFrame],[blurStart,blurEnd],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <AbsoluteFill style={{overflow:'hidden'}}>
    <Img src={src} style={{position:'absolute',left:geom.x,top:geom.y,width:geom.width,height:geom.height,
      maxWidth:'none',maxHeight:'none',filter:`blur(${Math.max(0,blur)}px)`}} />
  </AbsoluteFill>;
};
