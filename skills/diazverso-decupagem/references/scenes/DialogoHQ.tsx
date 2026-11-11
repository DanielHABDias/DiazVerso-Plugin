import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {imageBoundsHQ} from './HQMotion';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill,Img,cancelRender,continueRender,delayRender,useCurrentFrame,useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Speaker='left'|'right';
type Participant={asset:string;name?:string;color?:string;scale?:number};
type Turn={speaker:Speaker;text:string;at:number;duration:number;animation?:'escrita'|'none';writeDuration?:number;textDelay?:number;textColor?:string};
type Props=HQBackgroundOptions & {left:Participant;right:Participant;turns:Turn[];fontFamily?:HQFont;
  textColor?:string;motionDuration?:number;highlightOpacity?:number;assets?:Record<string,string>};
type Bounds={x:number;y:number;width:number;height:number;sourceWidth:number;sourceHeight:number};
type TextLayout={lines:string[];size:number};
const clampDialogue=(x:number)=>Math.max(0,Math.min(1,x));
const easeDialogue=(x:number)=>{const p=clampDialogue(x);return p*p*(3-2*p);};

export function validateDialogue(turns:Turn[],duration:number,motionDuration:number){
  if(!Array.isArray(turns)||!turns.length)throw new Error('Informe turns com pelo menos uma fala.');
  if(!Number.isFinite(motionDuration)||motionDuration<0)throw new Error('motionDuration deve ser não negativo.');
  turns.forEach((turn,i)=>{
    if(!['left','right'].includes(turn.speaker)||!turn.text?.trim()||!Number.isFinite(turn.at)||turn.at<0||!Number.isFinite(turn.duration)||turn.duration<=0||turn.at+turn.duration>duration+1e-7||
      (i>0&&turn.at<turns[i-1].at+turns[i-1].duration-1e-7))throw new Error('Falas: speaker left/right, text, at/duration dentro da cena, ordenados e sem sobreposição.');
    if(!['escrita','none'].includes(turn.animation??'escrita'))throw new Error('animation deve ser escrita ou none.');
    const delay=turn.textDelay??0,write=turn.writeDuration??Math.min(1.2,Math.max(.01,(turn.duration-delay)*.55));
    if(!Number.isFinite(delay)||delay<0||delay>=turn.duration||!Number.isFinite(write)||write<=0||((turn.animation??'escrita')==='escrita'&&delay+write>turn.duration+1e-7))throw new Error('textDelay e writeDuration precisam caber na fala.');
    if(turn.textColor&&!/^#[a-f\d]{6}$/i.test(turn.textColor))throw new Error('textColor deve usar #RRGGBB.');
  });
}
export function dialogueEvents(turns:Turn[]){return turns.flatMap(turn=>[{at:turn.at,order:1,left:turn.speaker==='left'?1:0,right:turn.speaker==='right'?1:0},{at:turn.at+turn.duration,order:0,left:0,right:0}]).sort((a,b)=>a.at-b.at||a.order-b.order);}
export function dialogueWeights(turns:Turn[],time:number,motionDuration:number,events=dialogueEvents(turns)){
  let origin={left:0,right:0},target={left:0,right:0},start=0;
  const sample=(at:number)=>{const p=motionDuration===0?1:easeDialogue((at-start)/motionDuration);return {left:origin.left+(target.left-origin.left)*p,right:origin.right+(target.right-origin.right)*p};};
  for(const event of events){if(event.at>time)break;origin=sample(event.at);target={left:event.left,right:event.right};start=event.at;}
  return sample(time);
}
export function dialogueTurnIndex(turns:Turn[],frame:number,fps:number){
  return turns.findIndex(turn=>frame>=Math.ceil(turn.at*fps-1e-8)&&frame<Math.ceil((turn.at+turn.duration)*fps-1e-8));
}
const dialogueImageBounds=imageBoundsHQ;
function dialogueTextLayout(text:string,family:HQFont,width:number,height:number,maximum:number):TextLayout{
  const ctx=document.createElement('canvas').getContext('2d');if(!ctx)throw new Error('Canvas indisponível.');
  const wrap=(size:number)=>{ctx.font=`${size}px ${family}`;const lines:string[]=[];for(const paragraph of text.split('\n')){let line='';for(const word of paragraph.split(/\s+/).filter(Boolean)){if(line&&ctx.measureText(line+' '+word).width>width){lines.push(line);line=word;}else line+=(line?' ':'')+word;}lines.push(line);}return lines;};
  let low=1,high=maximum;for(let i=0;i<18;i++){const size=(low+high)/2,lines=wrap(size);if(lines.length*size*1.15<=height&&lines.every(line=>ctx.measureText(line).width<=width))low=size;else high=size;}
  return {lines:wrap(low),size:low};
}

export default function DialogoHQ({left,right,turns,fontFamily='Anton',textColor='#FFFFFF',motionDuration=.45,highlightOpacity=85,
  backgroundStyle='halftone',backgroundColor='#10131E',backgroundOpacity=100,paperTone='light',gridBackgroundColor='#10101A',gridLineColor='#858595',assets={}}:Props){
  const {width:w,height:h,fps,durationInFrames}=useVideoConfig();const frame=useCurrentFrame(),time=frame/fps,portrait=h>w,u=Math.min(w,h)/1080;
  validateDialogue(turns,durationInFrames/fps,motionDuration);const fontUrl=resolveHQFont(fontFamily,assets);
  if(!left?.asset||!right?.asset||!assets[left.asset]||!assets[right.asset])throw new Error('Informe left/right.asset e os arquivos em assets.');
  const colors=[left.color??'#2676E8',right.color??'#EF3F49'];
  if(![...colors,textColor].every(c=>/^#[a-f\d]{6}$/i.test(c)))throw new Error('Cores devem usar #RRGGBB.');
  if(!Number.isFinite(highlightOpacity)||highlightOpacity<0||highlightOpacity>100)throw new Error('highlightOpacity: 0–100%.');
  if(!Number.isFinite(backgroundOpacity)||backgroundOpacity<0||backgroundOpacity>100)throw new Error('backgroundOpacity: 0–100%.');
  for(const p of [left,right])if(!Number.isFinite(p.scale??1)||(p.scale??1)<.5||(p.scale??1)>1)throw new Error('scale de participante: 0.5–1.');
  const textWidth=w*(portrait?.78:.40),textHeight=h*(portrait?.29:.52);
  const [prepared,setPrepared]=React.useState<{bounds:Bounds[];texts:TextLayout[];names:TextLayout[]}|null>(null);
  const [handle]=React.useState(()=>delayRender('Preparando Diálogo HQ'));
  const signature=JSON.stringify({left,right,turns,fontFamily,fontUrl,w,h,assets});
  React.useEffect(()=>{let live=true;Promise.all([loadFont({family:fontFamily,url:fontUrl}),dialogueImageBounds(assets[left.asset]),dialogueImageBounds(assets[right.asset])]).then(([,a,b])=>{if(!live)return;
    setPrepared({bounds:[a,b],texts:turns.map(t=>dialogueTextLayout(t.text.normalize('NFC').toLocaleUpperCase('pt-BR'),fontFamily,textWidth,textHeight,(portrait?95:110)*u)),names:[left,right].map(p=>dialogueTextLayout((p.name??'').toLocaleUpperCase('pt-BR'),fontFamily,textWidth,h*.05,38*u))});continueRender(handle);
  }).catch(error=>{if(live)cancelRender(error);});return()=>{live=false;};},[signature,handle]);
  const events=React.useMemo(()=>dialogueEvents(turns),[turns]);
  const index=dialogueTurnIndex(turns,frame,fps),turn=index<0?undefined:turns[index],weights=dialogueWeights(turns,time,motionDuration,events);
  const isRight=turn?.speaker==='right',layout=index<0?undefined:prepared?.texts[index];
  const delay=turn?.textDelay??0,local=turn?time-turn.at:0;
  const write=turn?.writeDuration??Math.min(1.2,Math.max(.01,((turn?.duration??1)-delay)*.55));
  const progress=turn?(turn.animation==='none'?(local>=delay?1:0):clampDialogue((local-delay)/write)):0;
  const total=layout?.lines.reduce((a,line)=>a+Array.from(line).length,0)??0;const visible=turn?.animation==='none'?total:Math.floor(progress*total);let letter=0;
  return <AbsoluteFill style={{overflow:'hidden'}}>
    <AbsoluteFill style={{opacity:backgroundOpacity/100,pointerEvents:'none'}}>
      <HQBackground {...{backgroundStyle,backgroundColor,paperTone,gridBackgroundColor,gridLineColor}}/>
      {colors.map((color,i)=><AbsoluteFill key={i} style={{opacity:(i===0?weights.left:weights.right)*highlightOpacity/100,background:`linear-gradient(to ${i===0?'right':'left'}, ${color} 0%, ${color}B8 24%, ${color}00 72%)`}}/>)}
    </AbsoluteFill>
    {prepared&&[left,right].map((participant,i)=>{
      const active=i===0?weights.left:weights.right,b=prepared.bounds[i];
      const fit=Math.min(w*(portrait?.59:.38)/b.width,h*(portrait?.48:.92)/b.height)*(participant.scale??1)*(.88+.12*active);
      const iw=b.width*fit,ih=b.height*fit;
      const idleX=i===0?0:w,activeX=w*(portrait?(i===0?.29:.71):(i===0?.19:.81)),cx=idleX+(activeX-idleX)*active;
      return <div key={i} style={{position:'absolute',left:cx-iw/2,top:h*.98-ih,width:iw,height:ih,overflow:'hidden',zIndex:active>.5?2:1,filter:`grayscale(${1-active}) brightness(${.55+.45*active})`,opacity:.45+.55*active}}>
        <Img src={assets[participant.asset]} style={{position:'absolute',left:-b.x*fit,top:-b.y*fit,width:b.sourceWidth*fit,height:b.sourceHeight*fit,maxWidth:'none'}}/>
      </div>;
    })}
    {turn&&layout&&progress>0&&<div style={{position:'absolute',zIndex:3,left:portrait?w*.11:w*(isRight?.17:.43),top:h*(portrait?.11:.18),width:textWidth,fontFamily,textAlign:portrait?'center':'left',color:turn.textColor??textColor,textShadow:fontFamily==='Anton'?'none':`${4*u}px ${6*u}px 0 #080A11`,WebkitTextStroke:fontFamily==='Anton'?'0px transparent':`${1.2*u}px #080A11`}}>
      {prepared?.names[isRight?1:0].lines.some(l=>l.length>0)&&<div style={{fontSize:prepared.names[isRight?1:0].size,lineHeight:1.1,marginBottom:h*.035,color:colors[isRight?1:0],whiteSpace:'pre'}}>{prepared.names[isRight?1:0].lines.join('\n')}</div>}
      <div style={{fontSize:layout.size,lineHeight:1.15}}>{layout.lines.map((line,i)=><div key={i} style={{whiteSpace:'pre'}}>{Array.from(line).map((c,j)=><span key={j} style={{opacity:letter++<visible?1:0}}>{c}</span>)}</div>)}</div>
    </div>}
  </AbsoluteFill>;
}

type HQFont = 'Bangers' | 'Anton';
export function resolveHQFont(family:HQFont, assets:{bangers?:string;anton?:string}){
  if(family!=='Bangers'&&family!=='Anton')throw new Error('fontFamily deve ser Bangers ou Anton.');
  const key=family==='Anton'?'anton':'bangers';
  if(!assets[key])throw new Error(`Informe assets.${key} para a fonte ${family}.`);
  return assets[key]!;
}
