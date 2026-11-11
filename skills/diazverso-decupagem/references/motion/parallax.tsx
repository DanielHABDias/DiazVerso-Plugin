import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {parallaxGeometry, clamp} from './motion-math.mjs';

export type ParallaxLayer = {
  id: string; src: string; imageWidth: number; imageHeight: number;
  depth: number; kind: 'background' | 'cutout';
  /** cutout placed within conservative design area; no crop */
  anchorX?: number; anchorY?: number; maxFrameWidth?: number; maxFrameHeight?: number;
};

/** parallax reusable layers. First layer must be opaque background.
 * Background layers cover; cutout images CONTAIN within the requested safe area.
 * No assumption that PNG assets are licensed or actually transparent.
 */
export const DiazParallax: React.FC<{layers: ParallaxLayer[], sceneDurationFrames: number}> =
({layers,sceneDurationFrames}) => {
  const frame=useCurrentFrame(), {width,height}=useVideoConfig();
  const t=clamp(frame/Math.max(1,sceneDurationFrames-1),0,1);
  if (!layers.length || layers[0].kind!=='background') throw new Error('opaque background layer required');
  return <AbsoluteFill style={{overflow:'hidden'}}>
    {layers.map((layer,i) => {
      if (!(layer.imageWidth>0&&layer.imageHeight>0)) throw new Error('actual layer dimensions required');
      if (layer.kind==='background') {
        const g=parallaxGeometry(layer.imageWidth,layer.imageHeight,width,height,t,layer.depth);
        return <Img key={layer.id} src={layer.src} style={{
          position:'absolute',left:g.x,top:g.y,width:g.width,height:g.height,
          maxWidth:'none',maxHeight:'none'}}/>;
      }
      if (layer.depth<0||layer.depth>1) throw new Error('invalid depth');
      const allowedW=Math.min(width*0.76, layer.maxFrameWidth??width*0.76);
      const allowedH=Math.min(height*0.68,layer.maxFrameHeight??height*0.68);
      const ratio=Math.min(allowedW/layer.imageWidth,allowedH/layer.imageHeight);
      const w=layer.imageWidth*ratio,h=layer.imageHeight*ratio;
      const centerX=clamp(layer.anchorX??width*0.5,w/2+width*0.08,width-w/2-width*0.08);
      const centerY=clamp(layer.anchorY??height*0.54,h/2+height*0.1,height-h/2-height*0.1);
      const drift=(t-0.5)*Math.min(width,height)*0.04*layer.depth;
      const x=clamp(centerX-w/2+drift,width*0.08,width*0.92-w);
      return <Img key={layer.id} src={layer.src} style={{
        position:'absolute',left:x,top:centerY-h/2,width:w,height:h,
        maxWidth:'none',maxHeight:'none'}}/>;
    })}
  </AbsoluteFill>;
};
