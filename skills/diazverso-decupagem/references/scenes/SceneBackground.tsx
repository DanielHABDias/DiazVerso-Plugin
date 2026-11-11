import React from 'react';
import {HQBackground} from '../motion/hq-background';
export type SceneBackgroundProps={backgroundStyle?:'comic-page'|'halftone'|'solid'|'stars'|'film'|'paper'|'grid';backgroundColor?:string;backgroundOpacity?:number;paperTone?:'light'|'dark';gridBackgroundColor?:string;gridLineColor?:string;children?:React.ReactNode};
export const SceneBackground:React.FC<SceneBackgroundProps> = ({backgroundStyle='halftone',backgroundColor='#162034',backgroundOpacity=100,paperTone='dark',gridBackgroundColor='#10101A',gridLineColor='#858595',children}) => <HQBackground mode={backgroundStyle} baseColor={backgroundColor} opacity={backgroundOpacity} paperTone={paperTone} gridBaseColor={gridBackgroundColor} gridColor={gridLineColor}>{children}</HQBackground>;
