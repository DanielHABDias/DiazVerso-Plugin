import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill,cancelRender,continueRender,delayRender,useCurrentFrame,useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Entrance='abrir'|'escrita'|'kinetic'|'none'|null;
type Exit='fechar'|'none'|null;
type TextStyle=HQBackgroundOptions & {fontFamily?:HQFont;textColor?:string;textScale?:number;
  kineticUnit?:'letter'|'word';kineticDirection?:'up'|'down'|'left'|'right';kineticStagger?:number;kineticAccentColor?:string;
  entryAnimation?:Entrance;exitAnimation?:Exit;entryDuration?:number;exitDuration?:number;entryDelay?:number;writeDuration?:number};
type TextStep=TextStyle & {text:string;at:number;duration:number};
type Props=TextStyle & {text?:string;texts?:TextStep[];assets?:{bangers?:string;anton?:string}};
type PreparedStep=TextStep & {fontFamily:HQFont;textColor:string;textScale:number;entryAnimation:Entrance;exitAnimation:Exit;
  entryDuration:number;exitDuration:number;entryDelay:number};
type Layout={lines:string[];fontSize:number};
const clampText=(x:number)=>Math.max(0,Math.min(1,x));
const easeText=(x:number)=>{const p=clampText(x);return p*p*(3-2*p);};

export function prepareTextSteps(props:Props,duration:number,fps:number):PreparedStep[]{
  if(props.text!==undefined&&props.texts!==undefined)throw new Error('Use text OU texts, não os dois.');
  const sequence=props.texts!==undefined;
  const raw=sequence?props.texts:[{text:props.text??'',at:0,duration}];
  if(!Array.isArray(raw)||!raw.length)throw new Error('TextoHQ requer text ou texts não vazio.');
  return raw.map((item,i)=>{
    if(!item.text?.trim()||!Number.isFinite(item.at)||item.at<0||!Number.isFinite(item.duration)||item.duration<=0||item.at+item.duration>duration+1e-7||
      (i>0&&item.at<raw[i-1].at+raw[i-1].duration-1e-7))throw new Error('Cada texto exige text, at e duration dentro da cena, ordenados e sem sobreposição.');
    const s={...props,...item};
    const entrance=s.entryAnimation===null?'none':s.entryAnimation??'escrita',exit=s.exitAnimation??'none';
    const delay=s.entryDelay??(sequence||entrance==='none'?0:Math.min(.12,item.duration*.1));
    const exitTime=exit==='fechar'?(s.exitDuration??.5):0;
    const available=item.duration-delay-exitTime;
    const write=s.writeDuration??1.8;
    if(!['abrir','escrita','kinetic','none'].includes(entrance)||!['fechar','none'].includes(exit))throw new Error('Entrada: abrir/escrita/kinetic/none; saída: fechar/none.');
    if(entrance==='kinetic'&&!['letter','word'].includes(s.kineticUnit??'letter'))throw Error('kineticUnit: letter ou word.');
    if(entrance==='kinetic'&&(!['up','down','left','right'].includes(s.kineticDirection??'up')||!Number.isFinite(s.kineticStagger??.035)||(s.kineticStagger??.035)<0||(s.kineticStagger??.035)>.15|| (s.kineticAccentColor!==undefined&&!/^#[a-f\d]{6}$/i.test(s.kineticAccentColor))))throw new Error('Kinetic: direction up/down/left/right; stagger 0–0.15 s; accentColor #RRGGBB.');
    if(!Number.isFinite(delay)||delay<0||!Number.isFinite(write)||write<=0||!Number.isFinite(exitTime)||exitTime<0||available<1/fps||
      (exit==='fechar'&&exitTime<1/fps)|| (s.entryDuration!==undefined&&(!Number.isFinite(s.entryDuration)||s.entryDuration<=0)))throw new Error('Tempos de animação inválidos ou maiores que o intervalo do texto.');
    const entryTime=s.entryDuration??Math.min(write,Math.max(1/fps,available-Math.min(.35,item.duration*.15)));
    if(entrance!=='none'&&entryTime>available+1e-7)throw new Error('Entrada e saída não cabem no intervalo do texto.');
    const family=s.fontFamily??'Bangers',color=s.textColor??'#FFFFFF',scale=s.textScale??1;
    if(!['Bangers','Anton'].includes(family)||!/^#[a-f\d]{6}$/i.test(color)||!Number.isFinite(scale)||scale<.2||scale>1)throw new Error('Fonte: Bangers/Anton; textColor: #RRGGBB; textScale: 0.2–1.');
    return {...s,text:item.text.normalize('NFC').toLocaleUpperCase('pt-BR').trim(),at:item.at,duration:item.duration,
      fontFamily:family,textColor:color,textScale:scale,entryAnimation:entrance,exitAnimation:exit,entryDelay:delay,entryDuration:entryTime,exitDuration:exitTime};
  });
}
export function activeTextIndex(steps:{at:number;duration:number}[],frame:number,fps:number){
  return steps.findIndex(s=>frame>=Math.ceil(s.at*fps-1e-8)&&frame<Math.ceil((s.at+s.duration)*fps-1e-8));
}
// The stagger compresses for long phrases; the last glyph always settles by entryDuration.
export function kineticGlyph(local:number,index:number,count:number,duration:number,stagger=.035){
  const gap=Math.min(stagger,duration*.65/Math.max(1,count-1));
  const progress=clampText((local-index*gap)/Math.max(.000001,duration-(count-1)*gap));
  const p=easeText(progress);
  return {opacity:p,offset:1-p,scale:(.65+.35*p)*(1+.12*Math.sin(Math.PI*p)),rotation:-12*(1-p)};
}
function fitHQText(text:string,family:HQFont,width:number,height:number,scale:number):Layout{
  const ctx=document.createElement('canvas').getContext('2d');if(!ctx)throw new Error('Canvas indisponível.');
  const wrap=(size:number)=>{ctx.font=`${size}px ${family}`;const lines:string[]=[];
    for(const paragraph of text.split('\n')){let line='';for(const word of paragraph.split(/\s+/).filter(Boolean)){
      if(line&&ctx.measureText(line+' '+word).width>width){lines.push(line);line=word;}else line+=(line?' ':'')+word;
    }lines.push(line);}return lines;};
  let low=1,high=Math.max(width,height);
  for(let i=0;i<20;i++){const size=(low+high)/2,lines=wrap(size);if(lines.length*size*1.16<=height&&lines.every(l=>ctx.measureText(l).width<=width))low=size;else high=size;}
  return {lines:wrap(low),fontSize:low*scale};
}
export default function TextoHQ(props:Props){
  const {width,height,fps,durationInFrames}=useVideoConfig();const frame=useCurrentFrame();
  const inputKey=JSON.stringify(props);
  const steps=React.useMemo(()=>prepareTextSteps(props,durationInFrames/fps,fps),[inputKey,durationInFrames,fps]),assets=props.assets??{};
  const urls=steps.map(s=>resolveHQFont(s.fontFamily,assets));
  const [layouts,setLayouts]=React.useState<Layout[]|null>(null);
  const [handle]=React.useState(()=>delayRender('Preparando Texto HQ'));
  const signature=JSON.stringify({steps,urls,width,height});
  React.useEffect(()=>{let live=true;Promise.all(steps.map((s,i)=>loadFont({family:s.fontFamily,url:urls[i]}))).then(()=>{if(!live)return;
    setLayouts(steps.map(s=>fitHQText(s.text,s.fontFamily,width*(width>height?.84:.8)*(s.entryAnimation==='kinetic'?.88:1),height*(width>height?.64:.66)*(s.entryAnimation==='kinetic'?.82:1),s.textScale)));
    continueRender(handle);
  }).catch(error=>{if(live)cancelRender(error);});return()=>{live=false;};},[signature,handle]);
  const index=activeTextIndex(steps,frame,fps),s=index<0?undefined:steps[index],layout=index<0?undefined:layouts?.[index];
  const bg=s??props,unit=Math.min(width,height)/1080;
  const local=s?frame/fps-s.at:0;
  const p=s?(s.entryAnimation==='none'?(local>=s.entryDelay?1:0):clampText((local-s.entryDelay)/s.entryDuration)):0;
  const opening=easeText(p),closing=s?.exitAnimation==='fechar'?easeText((local-(s.duration-s.exitDuration))/Math.max(1/fps,s.exitDuration-1/fps)):0;
  const openMask=s?.entryAnimation==='abrir'&&opening<1?`linear-gradient(to right, transparent ${50-opening*55-5}%, black ${50-opening*55}%, black ${50+opening*55}%, transparent ${50+opening*55+5}%)`:undefined;
  const closeMask=closing>0?`linear-gradient(to right, black ${50-closing*60-5}%, transparent ${50-closing*60}%, transparent ${50+closing*60}%, black ${50+closing*60+5}%)`:undefined;
  const units=(line:string)=>s?.entryAnimation==='kinetic'&&s.kineticUnit==='word'?line.split(/(\s+)/).filter(Boolean):Array.from(line);
  const total=layout?.lines.reduce((a,l)=>a+units(l).length,0)??0,visible=s?.entryAnimation==='escrita'?Math.floor(p*total):total;let letter=0;
  return <AbsoluteFill style={{overflow:'hidden',justifyContent:'center',alignItems:'center'}}>
    <HQBackground {...bg}><AbsoluteFill style={{pointerEvents:'none',opacity:.28,backgroundImage:`radial-gradient(circle, #080A11 ${3.2*unit}px, transparent ${3.8*unit}px)`,backgroundSize:`${18*unit}px ${18*unit}px`}}/></HQBackground>
    {s&&layout&&<div style={{position:'relative',width:width>height?'84%':'80%',textAlign:'center',opacity:(s.entryAnimation==='abrir'?opening:p>0?1:0)*(1-closing),maskImage:closeMask,WebkitMaskImage:closeMask}}>
      <div style={{fontFamily:s.fontFamily,fontSize:layout.fontSize,lineHeight:1.16,color:s.textColor,WebkitTextStroke:s.fontFamily === 'Anton' ? '0px transparent' : `${2*unit}px #080A11`,textShadow:s.fontFamily === 'Anton' ? 'none' : `${9*unit}px ${12*unit}px 0 #080A11`,maskImage:openMask,WebkitMaskImage:openMask}}>
        {layout.lines.map((line,i)=><div key={i} style={{whiteSpace:'pre'}}>{units(line).map((char,j)=>{
          const n=letter++;
          if(s.entryAnimation!=='kinetic')return <span key={j} style={{opacity:n<visible?1:0}}>{char}</span>;
          const k=kineticGlyph(local-s.entryDelay,n,total,s.entryDuration,s.kineticStagger),direction=s.kineticDirection??'up',distance=Math.min(layout.fontSize*.55,100*unit);
          return <span key={j} style={{display:'inline-block',opacity:k.opacity,color:s.kineticAccentColor&&n%5===0?s.kineticAccentColor:undefined,translate:`${direction==='left'?k.offset*distance:direction==='right'?-k.offset*distance:0}px ${direction==='up'?k.offset*distance:direction==='down'?-k.offset*distance:0}px`,rotate:`${k.rotation}deg`,scale:k.scale}}>{char}</span>;
        })}</div>)}
      </div>
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
