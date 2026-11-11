import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';
export type HQComicPageOptions={backgroundStyle?:'comic-page';backgroundOpacity?:number};
export function HQComicPage({opacity=100,src=staticFile('assets/brand/backgrounds/comic-page.png')}:{opacity?:number;src?:string}){
 if(!Number.isFinite(opacity)||opacity<0||opacity>100)throw Error('opacity must be 0–100');
 return <AbsoluteFill style={{pointerEvents:'none',opacity:opacity/100,overflow:'hidden'}}><Img src={src} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'center'}}/></AbsoluteFill>;
}
