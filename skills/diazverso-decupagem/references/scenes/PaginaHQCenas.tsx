import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {progressHQ} from './HQMotion';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {
  AbsoluteFill, Freeze, Img, OffthreadVideo, cancelRender, continueRender, delayRender,
  interpolateColors, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {loadFont} from './load-font';

type Panel = {asset: string; label?: string; sourceStart?: number; crt?: boolean; mediaType?:'video'|'image'; fit?:'cover'|'contain'; at?:number; accentColor?:string; backgroundColor?:string};
type Focus = {panel: number; at: number; until: number};
type Entry = {panel: number; at: number; duration?: number};
type Props = HQBackgroundOptions & {fontFamily?: HQFont;
  panels: Panel[];
  focus: Focus[];
  enter?: Entry;
  backgroundColor?: string;
  accentColor?: string;
  panelLayout?: 'grid'|'asymmetric'|'split'|'parallax';
  parallaxDuration?:number;
  splitColors?: [string,string];
  dividerColor?:string;
  heading?:string;
  headingColor?:string;
  entryDuration?:number;
  assets?: Record<string, string>;
};
type Interval = {at: number; until: number};
const clamp = (n: number) => Math.max(0, Math.min(1, n));
const ease = (n: number) => {const t = clamp(n); return t*t*t*(t*(t*6-15)+10);};
const mix = (a: number, b: number, p: number) => a + (b - a) * p;

// Playback advances only during this panel's active intervals, then freezes in place.
export function intervalsFor(panel: number, focus: Focus[], enter: Entry | undefined, end: number): Interval[] {
  const intervals = focus.filter(cue => cue.panel === panel).map(cue => ({
    at: cue.at, until: Math.min(cue.until, enter?.at ?? end, end),
  })).filter(cue => cue.until > cue.at);
  if (enter?.panel === panel) intervals.push({at: enter.at, until: end});
  intervals.sort((a, b) => a.at - b.at);
  const merged: Interval[] = [];
  for (const interval of intervals) {
    const last = merged[merged.length - 1];
    if (last && interval.at <= last.until) last.until = Math.max(last.until, interval.until);
    else merged.push({...interval});
  }
  return merged;
}

function TileVideo({src, sourceStart, elapsed, crt, unit,fit='cover'}: {
  src: string; sourceStart: number; elapsed: number; crt: boolean; unit: number;fit?:'cover'|'contain';
}) {
  const {fps} = useVideoConfig();
  return <>
    <Freeze frame={Math.round(elapsed * fps)}>
      <OffthreadVideo src={src} muted trimBefore={Math.round(sourceStart * fps)}
        style={{position: 'absolute', width: '100%', height: '100%', objectFit: fit, objectPosition: 'center'}} />
    </Freeze>
    {crt && <AbsoluteFill style={{pointerEvents: 'none',
      backgroundImage: `radial-gradient(circle at center, transparent 45%, #0006 100%), repeating-linear-gradient(to bottom, #0004 0px, #0004 ${unit}px, #FFFFFF08 ${2 * unit}px, transparent ${4 * unit}px)`,
      backgroundSize: `100% 100%, 100% ${4 * unit}px`}} />}
  </>;
}

export function parallaxCamera(time:number,focus:Focus[],duration:number){
  let position=0;
  for(const cue of focus){if(time<cue.at)break;const next=cue.panel-1;position=mix(position,next,ease((time-cue.at)/duration));}
  return position;
}
export function panelGeometry(w:number,h:number,layout:'grid'|'asymmetric'|'split'|'parallax',index:number){
  if(layout==='parallax')return {x:w*(w>h?.21:.14),y:h*(w>h?.24:.30),width:w*(w>h?.58:.72),height:h*(w>h?.60:.40),angle:0};
  if(layout==='split')return w>h?{x:w*(index===0?.055:.555),y:h*.28,width:w*.39,height:h*.57,angle:index===0?-1:1}:{x:w*.10,y:h*(index===0?.16:.59),width:w*.80,height:h*.29,angle:index===0?-1:1};
  if(layout==='asymmetric')return w>h?(index===0?{x:w*.07,y:h*.23,width:w*.57,height:h*.64,angle:-2}:{x:w*.68,y:h*.32,width:w*.25,height:h*.48,angle:2}):(index===0?{x:w*.08,y:h*.16,width:w*.84,height:h*.37,angle:-1.4}:{x:w*.20,y:h*.59,width:w*.72,height:h*.27,angle:1.8});
  const horizontal=w>h,tileH=h*(horizontal?.36:.38),yTop=h*(horizontal?.10:.09),yGap=h*(horizontal?.055:.04);
  return {x:w*(.055+(index%2)*.46),y:yTop+Math.floor(index/2)*(tileH+yGap),width:w*.43,height:tileH,angle:0};
}
export function validatePanelLayout(panels:Panel[],layout:string,duration:number,entryDuration:number,heading:string){
  if(!['grid','asymmetric','split','parallax'].includes(layout))throw new Error('panelLayout: grid, asymmetric, split ou parallax.');
  const count=layout==='grid'?4:2;
  if(!Array.isArray(panels)||(layout==='parallax'?(panels.length<2||panels.length>4):panels.length!==count))throw new Error(`panelLayout ${layout} requer ${layout==='parallax'?'2 a 4':count} panels.`);
  if(typeof heading!=='string'||heading.length>80)throw new Error('heading: texto com até 80 caracteres.');
  if(layout!=='grid'&&(!Number.isFinite(entryDuration)||entryDuration<=0||entryDuration>duration))throw new Error('entryDuration deve ser positiva e caber na cena.');
  panels.forEach((p,i)=>{
    if(!['video','image'].includes(p.mediaType??'video'))throw new Error('mediaType: video ou image.');
    if(!['cover','contain'].includes(p.fit??'cover'))throw new Error('fit: cover ou contain.');
    if(p.accentColor&&!/^#[a-f\d]{6}$/i.test(p.accentColor))throw new Error('accentColor do painel: #RRGGBB.');
    if(p.backgroundColor&&!/^#[a-f\d]{6}$/i.test(p.backgroundColor))throw new Error('backgroundColor do painel: #RRGGBB.');
    if(layout!=='grid'){const at=p.at??i*.55;if(!Number.isFinite(at)||at<0||at+entryDuration>duration+1e-8)throw new Error('Entrada do painel precisa caber na cena.');}
  });
}

export default function PaginaHQCenas({fontFamily='Anton', backgroundStyle="halftone", backgroundOpacity=100, paperTone="light", gridBackgroundColor="#10101A", gridLineColor="#858595", panels, focus, enter, backgroundColor = '#E8C64F', accentColor = '#2676E8', panelLayout='grid',parallaxDuration=.65,splitColors=['#D92F45','#2459C9'],dividerColor='#111723',heading='',headingColor='#111723',entryDuration=.55,assets = {}}: Props) {
  const fontUrl=panels?.some(p=>p.label)||(panelLayout!=='grid'&&heading)?resolveHQFont(fontFamily,assets):'';
  const {width: w, height: h, fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const time = frame / fps;
  const duration = durationInFrames / fps;
  const horizontal = w > h;
  const unit = Math.min(w, h) / 1080;
  validatePanelLayout(panels,panelLayout,duration,entryDuration,heading);
  const rangeKey=JSON.stringify({focus,enter,duration});
  const preparedRanges=React.useMemo(()=>panels.map((_,i)=>intervalsFor(i+1,[...focus].sort((a,b)=>a.at-b.at),enter,duration)),[rangeKey,panels.length]);
  const panelCount=panels.length,asymmetric=panelLayout!=='grid',split=panelLayout==='split',parallax=panelLayout==='parallax';
  if(parallax&&(!Number.isFinite(parallaxDuration)||parallaxDuration<=0||parallaxDuration>duration))throw new Error('parallaxDuration deve ser positiva e caber na cena.');
  if(split&&(!Array.isArray(splitColors)||splitColors.length!==2||!splitColors.every(c=>/^#[a-f\d]{6}$/i.test(c))||!/^#[a-f\d]{6}$/i.test(dividerColor)))throw new Error('splitColors: duas cores #RRGGBB; dividerColor: #RRGGBB.');
  if (!Array.isArray(focus)) throw new Error('PaginaHQCenas requer focus com os tempos de destaque.');
  if (!/^#[0-9a-fA-F]{6}$/.test(backgroundColor) || !/^#[0-9a-fA-F]{6}$/.test(accentColor)) {
    throw new Error('As cores devem usar #RRGGBB.');
  }
  const ordered = [...focus].sort((a, b) => a.at - b.at);
  ordered.forEach((cue, index) => {
    if (!Number.isInteger(cue.panel) || cue.panel < 1 || cue.panel > panelCount || !Number.isFinite(cue.at) || !Number.isFinite(cue.until) || cue.at < 0 || cue.until <= cue.at || cue.until > duration + 1 / fps) {
      throw new Error(`focus requer panel de 1 a ${panelCount} e at/until válidos dentro da cena.`);
    }
    if (index && cue.at < ordered[index - 1].until) throw new Error('Os intervalos de focus não podem se sobrepor.');
    if(parallax&&cue.until-cue.at<parallaxDuration-1e-8)throw new Error('Cada focus deve durar ao menos parallaxDuration.');
  });
  if (enter && (!Number.isInteger(enter.panel) || enter.panel < 1 || enter.panel > panelCount || !Number.isFinite(enter.at) || enter.at < 0 || !Number.isFinite(enter.duration ?? 1.1) || (enter.duration ?? 1.1) <= 0 || enter.at + (enter.duration ?? 1.1) > duration + 1 / fps)) {
    throw new Error(`enter deve apontar para panel de 1 a ${panelCount} e terminar dentro da cena.`);
  }
  panels.forEach(panel => {
    if (!assets[panel.asset]) throw new Error(`Asset ausente: ${panel.asset}`);
    if (!Number.isFinite(panel.sourceStart ?? 0) || (panel.sourceStart ?? 0) < 0) throw new Error('sourceStart deve ser um tempo positivo ou zero.');
  });
  if(!/^#[a-f\d]{6}$/i.test(headingColor))throw new Error('headingColor: #RRGGBB.');
  const labels = panels.some(panel => panel.label)||(asymmetric&&Boolean(heading));
  if (labels && !fontUrl) throw new Error('Informe fontUrl para usar etiquetas nos quadros.');
  const [fontHandle] = React.useState(() => labels ? delayRender('Carregando etiquetas da página HQ') : null);
  React.useEffect(() => {
    if (fontHandle === null) return;
    loadFont({family: fontFamily, url: fontUrl})
      .then(() => continueRender(fontHandle)).catch(error => cancelRender(error));
  }, [fontHandle, fontUrl, fontFamily]);

  const zoom = enter ? ease(progressHQ(time,enter.at,enter.duration??1.1,fps)) : 0;
  const drift = 1 - zoom;
  const boardX = Math.sin(time * .7) * w * .003 * drift;
  const boardY = Math.sin(time * .9 + .4) * h * .004 * drift;
  const boardAngle = Math.sin(time * .6) * .25 * drift;
  const target = enter && time >= enter.at ? enter.panel : null;
  const camera=parallax?parallaxCamera(Math.min(time,enter?.at??duration),ordered,parallaxDuration):0;

  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <HQBackground {...{backgroundStyle,backgroundColor,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor}}>
      <AbsoluteFill style={{opacity: .23 * (1 - zoom), backgroundImage: `radial-gradient(#080A11 ${3 * unit}px, transparent ${3.7 * unit}px)`,
      backgroundSize: `${19 * unit}px ${19 * unit}px`}} />
    </HQBackground>
    {split&&<AbsoluteFill style={{pointerEvents:'none',opacity:backgroundOpacity/100*(1-zoom)}}>
      {splitColors.map((color,i)=>{const reveal=ease((time-(panels[i].at??i*.55))/entryDuration);return <div key={i} style={{position:'absolute',left:horizontal?`${i*50}%`:0,top:horizontal?0:`${i*50}%`,width:horizontal?'50%':'100%',height:horizontal?'100%':'50%',backgroundColor:color,backgroundImage:`radial-gradient(#080A1138 ${3*unit}px, transparent ${3.7*unit}px)`,backgroundSize:`${19*unit}px ${19*unit}px`,clipPath:horizontal?`inset(0 ${i===0?(1-reveal)*100:0}% 0 ${i===1?(1-reveal)*100:0}%)`:`inset(${i===1?(1-reveal)*100:0}% 0 ${i===0?(1-reveal)*100:0}% 0)`}}/>;})}
      <div style={{position:'absolute',left:horizontal?'calc(50% - 4px)':'5%',top:horizontal?'22%':'calc(50% - 4px)',width:horizontal?8*unit:'90%',height:horizontal?'70%':8*unit,background:dividerColor,transformOrigin:horizontal?'top':'left',transform: `${horizontal?'scaleY':'scaleX'}(${ease((time-Math.max(...panels.map((p,i)=>(p.at??i*.55)+entryDuration)))/.35)})`}}/>
    </AbsoluteFill>}
    <AbsoluteFill style={{translate: `${boardX}px ${boardY}px`, rotate: `${boardAngle}deg`}}>
      {panels.map((panel, index) => {
        const number = index + 1;
        const ranges = preparedRanges[index];
        const elapsed = ranges.reduce((sum, range) => sum + Math.max(0, Math.min(time, range.until) - range.at), 0);
        const active = ranges.find(range => range.at <= time && time < range.until);
        const previous = ranges.filter(range => range.until <= time).at(-1);
        const light = asymmetric&&ordered.length===0&&!enter?1:active ? ease((time - active.at) / .24) : previous ? 1 - ease((time - previous.until) / .24) : 0;
        const selected = target === number;
        const expand = selected ? zoom : 0;
        const base=panelGeometry(w,h,panelLayout,index),relative=index-camera,depth=Math.min(3,Math.abs(relative));
        const layerScale=parallax?1-depth*.12:1;
        const tileW=base.width*layerScale,tileH=base.height*layerScale;
        const x=parallax?base.x+(base.width-tileW)/2+relative*w*.18:base.x;
        const y=parallax?base.y+(base.height-tileH)/2+depth*h*.025:base.y;
        const angle=parallax?relative*4:base.angle;
        const border = 8 * unit * (1 - expand);
        const arrival = asymmetric?ease((time-(panel.at??index*.55))/entryDuration):ease(time / .38);
        return <div key={number} style={{position: 'absolute', left: mix(x, 0, expand), top: mix(y, 0, expand),
          width: mix(tileW, w, expand), height: mix(tileH, h, expand), zIndex: selected ? 200 : parallax?100-Math.round(depth*20):active ? 3 : 1,
          boxSizing: 'border-box', overflow: 'hidden', border: `${border}px solid ${interpolateColors(light, [0, 1], ['#F5EFDE', asymmetric?(panel.accentColor??accentColor):accentColor])}`,
          background: asymmetric?(panel.backgroundColor??'#F5EFDE'):'#080A11', opacity: selected ? arrival : arrival * (1 - zoom),
          boxShadow: `${10 * unit * (1 - expand)}px ${13 * unit * (1 - expand)}px 0 #080A11`,
          translate: split?`${horizontal?(index===0?-1:1)*(1-arrival)*w*.20:0}px ${horizontal?0:(index===0?-1:1)*(1-arrival)*h*.18}px`:`0 ${(1 - arrival) * (asymmetric?90:35) * unit}px`,rotate:asymmetric?`${angle*(1-expand)}deg`:undefined}}>
          <AbsoluteFill style={{filter: `grayscale(${1 - light}) brightness(${.26 + .74 * light})`}}>
            {panel.mediaType==='image'?<><Img src={assets[panel.asset]} style={{position:'absolute',width:'100%',height:'100%',objectFit:panel.fit??'cover'}}/>{panel.crt&&<AbsoluteFill style={{pointerEvents:'none',backgroundImage:`repeating-linear-gradient(to bottom, #0004 0px, #0004 ${unit}px, transparent ${4*unit}px)`}}/>}</>:<TileVideo src={assets[panel.asset]} sourceStart={panel.sourceStart ?? 0} elapsed={elapsed} crt={panel.crt ?? false} unit={unit} fit={panel.fit}/>}
          </AbsoluteFill>
          {panel.label && <div style={{position: 'absolute', left: 16 * unit, bottom: 13 * unit,
            padding: `${7 * unit}px ${14 * unit}px`, background: '#080A11', color: '#FFFFFF',
            fontFamily: fontFamily, fontSize: asymmetric?Math.min((horizontal?46:44)*unit,tileW*.82/Math.max(1,panel.label.length*.58)):(horizontal ? 36 : 31) * unit,
            opacity: (1 - expand) * (.45 + .55 * light)}}>{panel.label.toLocaleUpperCase('pt-BR')}</div>}
        </div>;
      })}
    </AbsoluteFill>
    {asymmetric&&heading&&<div style={{position:'absolute',left:w*.08,right:w*.08,top:h*.06,color:headingColor,fontFamily,fontSize:Math.min(58*unit,w*.82/Math.max(1,heading.length*.58)),textTransform:'uppercase',lineHeight:1.15,borderBottom:`${5*unit}px solid ${accentColor}`,paddingBottom:14*unit,opacity:1-zoom}}>{heading}</div>}
  </AbsoluteFill>;
}

type HQFont = 'Bangers' | 'Anton';
export function resolveHQFont(family:HQFont, assets:{bangers?:string;anton?:string}){
  if(family!=='Bangers'&&family!=='Anton')throw new Error('fontFamily deve ser Bangers ou Anton.');
  const key=family==='Anton'?'anton':'bangers';
  if(!assets[key])throw new Error(`Informe assets.${key} para a fonte ${family}.`);
  return assets[key]!;
}
