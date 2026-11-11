import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {HQBackground} from './hq-background';
import {HQOverlay} from './hq-overlay';

/** G06 two independent component migrations, both used in one short test scene.
 * No legacy Content Lab, no images, audio or unlicensed font dependencies.
 */
export const HQMigrationScene:React.FC = () => {
  const frame=useCurrentFrame();
  const {width,height}=useVideoConfig();
  return <AbsoluteFill style={{overflow:'hidden',backgroundColor:'#111827'}}>
    <HQBackground mode="grid" baseColor="#111827" gridColor="#536D9A" opacity={95}/>
    <div style={{position:'absolute',top:'25%',left:'10%',width:'80%',
      height:'42%',border:'5px solid #ACC2E6',borderRadius:8,
      transform:`translateX(${Math.sin(frame/18)*16}px)`,
      boxShadow:'0 18px 45px rgba(0,0,0,.55)'}}/>
    <HQOverlay upperText="Diazverso" lowerText={width>height?'Quadro HQ independente':'HQ vertical independente'}
      tagColor="#5CA5AD" compactAt={1.2} compactDuration={.5} compactScale={.72}/>
  </AbsoluteFill>;
};
