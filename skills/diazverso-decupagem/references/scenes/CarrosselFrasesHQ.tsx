import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill,cancelRender,continueRender,delayRender,useCurrentFrame,useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Phrase={text:string;at:number;color?:string};
type Props=HQBackgroundOptions & {phrases:Phrase[];fontFamily?:HQFont;align?:'left'|'right';
  activeColor?:string;inactiveColor?:string;inactiveOpacity?:number;inactiveScale?:number;
  activeBandColor?:string;activeBandOpacity?:number;
  motionDuration?:number;textScale?:number;assets?:{bangers?:string;anton?:string}};
type Layout={lines:string[];size:number;height:number};
const clampCarousel=(v:number)=>Math.max(0,Math.min(1,v));
const smoothCarousel=(v:number)=>{const t=clampCarousel(v);return t*t*(3-2*t);};

export function validateCarousel(phrases:Phrase[],duration:number,motionDuration:number){
  if(!Number.isFinite(duration)||duration<=0)throw new Error('Duração da cena deve ser positiva.');
  if(!Number.isFinite(motionDuration)||motionDuration<0)throw new Error('motionDuration deve ser não negativo.');
  if(!Array.isArray(phrases)||!phrases.length)throw new Error('Informe phrases com pelo menos uma frase.');
  phrases.forEach((p,i)=>{
    if(typeof p.text!=='string'||!p.text.trim()||!Number.isFinite(p.at)||p.at<0||p.at>=duration)throw new Error('Frase precisa de text e at dentro da cena.');
    if(i&&p.at<=phrases[i-1].at)throw new Error('at deve ser estritamente crescente.');
    if(i&&p.at-phrases[i-1].at<motionDuration-1e-7)throw new Error('Intervalo entre chegadas deve ser >= motionDuration.');
    if(!i&&p.at>0&&p.at<motionDuration-1e-7)throw new Error('Primeiro at deve ser 0 ou >= motionDuration.');
    if(p.color&&!/^#[a-f\d]{6}$/i.test(p.color))throw new Error('Cor da frase deve usar #RRGGBB.');
  });
}

// at is ARRIVAL, not the start of the transition: words are ready when spoken.
export function carouselPosition(phrases:Phrase[],time:number,motionDuration:number){
  let current=-1;
  for(let i=0;i<phrases.length;i++){
    const at=phrases[i].at;
    if(time>=at){current=i;continue;}
    if(motionDuration>0&&time>=at-motionDuration)return i-1+smoothCarousel((time-at+motionDuration)/motionDuration);
    break;
  }
  return current;
}

export function carouselTextLayout(ctx:CanvasRenderingContext2D,text:string,family:HQFont,width:number,height:number,maximum:number):Layout{
  const wrap=(size:number)=>{
    ctx.font=`${size}px ${family}`;const lines:string[]=[];
    for(const paragraph of text.normalize('NFC').toLocaleUpperCase('pt-BR').split('\n')){
      let line='';for(const word of paragraph.split(/\s+/).filter(Boolean)){
        if(line&&ctx.measureText(line+' '+word).width>width){lines.push(line);line=word;}else line+=(line?' ':'')+word;
      }lines.push(line);
    }return lines;
  };
  let lo=1,hi=maximum;
  for(let i=0;i<20;i++){const size=(lo+hi)/2,lines=wrap(size);if(lines.length<=2&&lines.length*size*1.12<=height&&lines.every(l=>ctx.measureText(l).width<=width))lo=size;else hi=size;}
  const lines=wrap(lo);if(lines.length>2)throw new Error('Use frases curtas: no máximo duas linhas por frase.');
  return {lines,size:lo,height:lines.length*lo*1.12};
}

export default function CarrosselFrasesHQ({phrases,fontFamily='Anton',align='left',activeColor='#F4C542',inactiveColor='#9698A2',inactiveOpacity=.38,inactiveScale=.60,
  activeBandColor='#A0A0A0',activeBandOpacity=.12,motionDuration=.45,textScale=1,backgroundStyle='halftone',backgroundColor='#10131E',backgroundOpacity=100,paperTone='light',gridBackgroundColor='#10101A',gridLineColor='#858595',assets={}}:Props){
  const {width:w,height:h,fps,durationInFrames}=useVideoConfig(),frame=useCurrentFrame();
  validateCarousel(phrases,durationInFrames/fps,motionDuration);
  if(!['left','right'].includes(align))throw new Error('align: left ou right.');
  if(![activeColor,inactiveColor].every(c=>/^#[a-f\d]{6}$/i.test(c)))throw new Error('Cores devem usar #RRGGBB.');
  if(!/^#[a-f\d]{6}$/i.test(activeBandColor))throw new Error('activeBandColor deve usar #RRGGBB.');
  if(!Number.isFinite(activeBandOpacity)||activeBandOpacity<0||activeBandOpacity>1)throw new Error('activeBandOpacity: 0–1.');
  if(!Number.isFinite(inactiveOpacity)||inactiveOpacity<0||inactiveOpacity>1)throw new Error('inactiveOpacity: 0–1.');
  if(!Number.isFinite(inactiveScale)||inactiveScale<.3||inactiveScale>.85)throw new Error('inactiveScale: 0.3–0.85.');
  if(!Number.isFinite(textScale)||textScale<.25||textScale>1)throw new Error('textScale: 0.25–1.');
  const url=resolveHQFont(fontFamily,assets),textW=w*.84,maximum=Math.min(h*.20,w*.19)*textScale;
  const [prepared,setPrepared]=React.useState<{signature:string;layouts:Layout[]}|null>(null);
  const [handle]=React.useState(()=>delayRender('Preparando Carrossel de Frases HQ'));
  const signature=JSON.stringify({phrases,fontFamily,url,w,h,textScale});
  React.useEffect(()=>{let live=true;loadFont({family:fontFamily,url}).then(()=>{
    const ctx=document.createElement('canvas').getContext('2d');if(!ctx)throw new Error('Canvas indisponível.');
    const layouts=phrases.map(p=>carouselTextLayout(ctx,p.text,fontFamily,textW,h*.24,maximum));
    if(live)setPrepared({signature,layouts});continueRender(handle);
  }).catch(cancelRender);return()=>{live=false;};},[signature,handle]);
  const cursor=carouselPosition(phrases,frame/fps,motionDuration);
  const blendColor=(from:string,to:string,p:number)=>{const a=from.slice(1).match(/../g)!.map(x=>parseInt(x,16)),b=to.slice(1).match(/../g)!.map(x=>parseInt(x,16));return `rgb(${a.map((v,i)=>Math.round(v+(b[i]-v)*p)).join(',')})`;};
  return <AbsoluteFill style={{overflow:'hidden',pointerEvents:'none'}}>
    <HQBackground backgroundStyle={backgroundStyle} backgroundColor={backgroundColor} backgroundOpacity={backgroundOpacity} paperTone={paperTone} gridBackgroundColor={gridBackgroundColor} gridLineColor={gridLineColor}/>
    <div data-active-band style={{position:'absolute',left:0,top:h*.36,width:w,height:h*.28,backgroundColor:activeBandColor,opacity:activeBandOpacity}}/>
    {prepared?.signature===signature&&phrases.slice(Math.max(0,Math.floor(cursor)-2),Math.ceil(cursor)+3).map((phrase,offset)=>{
      const i=Math.max(0,Math.floor(cursor)-2)+offset;
      const slot=i-cursor;if(slot>2||slot< -2)return null;
      const layout=prepared.layouts[i],focus=clampCarousel(1-Math.abs(slot)),scale=inactiveScale+(1-inactiveScale)*focus;
      const gap=h*.045,smallH=layout.height*inactiveScale;
      const yAt=(n:number)=>n>=2?-smallH:n===1?h/3-gap-smallH/2:n===0?h/2:n===-1?2*h/3+gap+smallH/2:h+smallH;
      const lower=Math.floor(slot),mix=slot-lower,cy=yAt(lower)+(yAt(lower+1)-yAt(lower))*mix;
      const edge=clampCarousel(2-Math.abs(slot)),opacity=(inactiveOpacity+(1-inactiveOpacity)*focus)*edge;
      const ink=blendColor(inactiveColor,phrase.color??activeColor,focus);
      return <div key={i} data-phrase={i} style={{position:'absolute',left:w*.08,top:cy-layout.height/2,width:textW,height:layout.height,
        scale,transformOrigin:align==='left'?'left center':'right center',fontFamily,fontSize:layout.size,lineHeight:1.12,
        textAlign:align,color:ink,opacity,whiteSpace:'pre',textShadow:fontFamily==='Anton'?'none':`0 ${Math.min(w,h)*.005}px 0 #080A11`,
        WebkitTextStroke:fontFamily==='Anton'?undefined:`${Math.min(w,h)*.0012}px #080A11`,paintOrder:'stroke fill'}}>{layout.lines.join('\n')}</div>;
    })}
  </AbsoluteFill>;
}

type HQFont = 'Bangers' | 'Anton';
export function resolveHQFont(family:HQFont, assets:{bangers?:string;anton?:string}){
  if(family!=='Bangers'&&family!=='Anton')throw new Error('fontFamily deve ser Bangers ou Anton.');
  const key=family==='Anton'?'anton':'bangers';
  if(!assets[key])throw new Error(`Informe assets.${key} para a fonte ${family}.`);
  return assets[key]!;
}
