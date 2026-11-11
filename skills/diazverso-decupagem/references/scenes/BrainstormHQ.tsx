import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill, Img, cancelRender, continueRender, delayRender, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Node = {id:string; text?:string; subtitle?:string; asset?:string; x?:number; y?:number; color?:string};
type Step = {node:string; from?:string; hold:number; moveDuration?:number; connect?:boolean};
type Props = HQBackgroundOptions & {fontFamily?: HQFont; nodes:Node[]; steps:Step[]; backgroundColor?:string; cardColor?:string; textColor?:string;
  lineColor?:string; zoomOutDuration?:number; presentation?:'cards'|'path'|'narrative'|'evidence'; heading?:string; pathBend?:number; dotColor?:string; dotSize?:number; assets?:Record<string,string>};
const smooth=(x:number)=>{const t=Math.max(0,Math.min(1,x));return t*t*t*(t*(t*6-15)+10);};
export function buildTimeline(nodes:Node[], steps:Step[], zoomOutDuration:number) {
  if(!nodes.length || !steps.length) throw new Error('Informe nodes e steps.');
  const ids=new Set(nodes.map(n=>n.id));
  if(ids.size!==nodes.length || nodes.some(n=>!n.id || (!n.text?.trim()&&!n.asset))) throw new Error('Cada nó precisa de id único e texto ou imagem.');
  nodes.forEach(n=>{if((n.x===undefined)!==(n.y===undefined) || (n.x!==undefined&&(!Number.isFinite(n.x)||!Number.isFinite(n.y))))throw new Error('Informe x e y juntos, em coordenadas finitas.');});
  let cursor=0;const seen=new Set<string>();
  const result=steps.map((s,i)=>{
    const move=i===0?0:(s.moveDuration??.85);
    if(!ids.has(s.node)||!Number.isFinite(s.hold)||s.hold<=0||!Number.isFinite(move)||move<0)throw new Error('Etapas precisam de nó existente, hold positivo e moveDuration não negativo.');
    const from=i===0?undefined:(s.from??steps[i-1].node);
    if(from&&!seen.has(from))throw new Error('from deve apontar para um nó já apresentado.');
    const start=cursor,arrival=start+move;cursor=arrival+s.hold;seen.add(s.node);
    return {...s,from,start,arrival,end:cursor,move};
  });
  if(seen.size!==nodes.length)throw new Error('Todos os nós precisam ser visitados em steps.');
  if(!Number.isFinite(zoomOutDuration)||zoomOutDuration<=0)throw new Error('zoomOutDuration deve ser positivo.');
  const firstByNode=new Map<string,typeof result[number]>();for(const step of result)if(!firstByNode.has(step.node))firstByNode.set(step.node,step);
  return {steps:result,firstByNode,overviewAt:cursor,minimumDuration:cursor+zoomOutDuration};
}

export default function BrainstormHQ({fontFamily='Anton', backgroundStyle="halftone", backgroundOpacity=100, paperTone="light", gridBackgroundColor="#10101A", gridLineColor="#858595", nodes,steps,backgroundColor='#18243C',cardColor='#FFF5D7',textColor:suppliedTextColor,lineColor='#FF435A',zoomOutDuration=1.4,presentation='cards',heading='',pathBend=.18,dotColor='#F4C542',dotSize=14,assets={}}:Props){
  const textColor=suppliedTextColor??(['cards','evidence'].includes(presentation)?'#172338':'#FFFFFF');
  const fontUrl=resolveHQFont(fontFamily,assets);
  const {width:w,height:h,fps,durationInFrames}=useVideoConfig();const t=useCurrentFrame()/fps;
  const timelineKey=JSON.stringify({nodes,steps,zoomOutDuration});
  const timeline=React.useMemo(()=>buildTimeline(nodes,steps,zoomOutDuration),[timelineKey]);
  if(timeline.minimumDuration>durationInFrames/fps+1e-6)throw new Error(`Cena curta: mínimo ${timeline.minimumDuration.toFixed(2)}s; reserve também tempo para contemplar o mapa.`);
  if(!fontUrl)throw new Error('Informe fontUrl.');
  const [ready,setReady]=React.useState(false);
  const [handle]=React.useState(()=>delayRender('Carregando Bangers'));
  React.useEffect(()=>{loadFont({family:fontFamily,url:fontUrl}).then(()=>{setReady(true);continueRender(handle);}).catch(cancelRender);},[fontUrl,fontFamily,handle]);
  const portrait=h>w;
  const boxes=nodes.map((n,i)=>({...n,x:n.x??(portrait?(i%2)*580:(i%3)*580),y:n.y??(portrait?Math.floor(i/2)*490:Math.floor(i/3)*490),width:400,height:n.asset?(n.text?390:330):210}));
  const box=(id:string)=>boxes.find(n=>n.id===id)!;
  const fit=(n:typeof boxes[number])=>Math.min(w*.76/n.width,h*.74/n.height);
  const bounds={left:Math.min(...boxes.map(n=>n.x-225)),right:Math.max(...boxes.map(n=>n.x+225)),top:Math.min(...boxes.map(n=>n.y-n.height/2-30)),bottom:Math.max(...boxes.map(n=>n.y+n.height/2+30))};
  const first=box(steps[0].node);let cx=first.x,cy=first.y,scale=fit(first);
  timeline.steps.forEach((s,i)=>{if(!i||t<s.start)return;const a=box(steps[i-1].node),b=box(s.node),p=s.move===0?1:smooth((t-s.start)/s.move);cx=a.x+(b.x-a.x)*p;cy=a.y+(b.y-a.y)*p;scale=fit(a)+(fit(b)-fit(a))*p;});
  if(t>=timeline.overviewAt){const p=smooth((t-timeline.overviewAt)/zoomOutDuration);cx+=((bounds.left+bounds.right)/2-cx)*p;cy+=((bounds.top+bounds.bottom)/2-cy)*p;scale+=(Math.min(w*.88/(bounds.right-bounds.left),h*.84/(bounds.bottom-bounds.top))-scale)*p;}
  const uid=React.useId().replace(/:/g,'');
  if(!['cards','path','narrative','evidence'].includes(presentation))throw new Error('presentation: cards, path, narrative ou evidence.');
  if(presentation==='evidence'){
    validateNarrative(nodes,heading);
    return <EvidenceHQ {...{nodes,steps,timeline,t,w,h,fontFamily,ready,heading,backgroundStyle,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor,backgroundColor,cardColor,textColor,lineColor,zoomOutDuration,assets}}/>;
  }
  if(presentation==='path'||presentation==='narrative'){
    validateJourney(pathBend,dotSize,dotColor);
    if(presentation==='narrative')validateNarrative(nodes,heading);
    timeline.steps.forEach((s,i)=>{if(i&&s.connect!==false&&s.from!==steps[i-1].node)throw new Error('No modo path, from deve ser o ponto anterior; use cards para ramificações.');});
    return <JourneyHQ {...{nodes,steps,timeline,t,w,h,fontFamily,ready,backgroundStyle,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor,backgroundColor,textColor,lineColor,pathBend,dotColor,dotSize,zoomOutDuration,assets}} narrative={presentation==='narrative'} heading={heading}/>;
  }
  return <AbsoluteFill style={{overflow:'hidden',fontFamily:fontFamily}}>
    <HQBackground {...{backgroundStyle,backgroundColor,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor}}>
      <AbsoluteFill style={{opacity:.15,backgroundImage:'radial-gradient(#FFFFFF 1.6px, transparent 2px)',backgroundSize:'12px 12px'}}/>
    </HQBackground>
    <div style={{position:'absolute',left:0,top:0,transformOrigin:'0 0',transform:`translate(${w/2}px,${h/2}px) scale(${scale}) translate(${-cx}px,${-cy}px)`}}>

      {boxes.map(n=>{const debut=timeline.firstByNode.get(n.id)!;if(t<debut.start)return null;const p=debut.move===0?1:smooth((t-debut.start)/Math.max(.15,debut.move));const color=n.color??cardColor;if(n.asset&&!assets[n.asset])throw new Error(`Asset ausente: ${n.asset}`);return <div key={n.id} style={{position:'absolute',left:n.x-200,top:n.y-n.height/2,width:400,height:n.height,boxSizing:'border-box',border:'6px solid #080A10',background:color,boxShadow:'12px 14px 0 #080A10',opacity:p,transform:`scale(${.86+.14*p})`,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',padding:22,gap:16}}>
        {n.asset&&<Img src={assets[n.asset]} style={{width:'100%',height:n.text?245:270,objectFit:'contain',minHeight:0}}/>}
        {n.text&&<div style={{color:textColor,fontSize:Math.min(55,220/Math.sqrt(Math.max(1,n.text.length/4))),textTransform:'uppercase',textAlign:'center',lineHeight:1.1,overflowWrap:'anywhere',textShadow:fontFamily === 'Anton' ? 'none' : '3px 4px 0 #080A10',WebkitTextStroke:fontFamily === 'Anton' ? '0px transparent' : '.7px #080A10',opacity:ready?1:0}}>{n.text}</div>}
      </div>;})}
      <svg style={{position:'absolute',overflow:'visible',width:1,height:1}}>
        {timeline.steps.map((s,i)=>{if(!i||s.connect===false||t<s.start||s.from===s.node)return null;const a=box(s.from!),b=box(s.node);const p=s.move===0?1:smooth((t-s.start)/s.move);const ports=cardPorts(a,b),pa=ports.a,pb=ports.b;const d=`M ${pa.x} ${pa.y} C ${pa.x+(pb.x-pa.x)*.5} ${pa.y}, ${pa.x+(pb.x-pa.x)*.5} ${pb.y}, ${pb.x} ${pb.y}`;return <g key={i}><defs><mask id={`${uid}-${i}`} maskUnits="userSpaceOnUse" x={Math.min(a.x,b.x)-500} y={Math.min(a.y,b.y)-500} width={Math.abs(a.x-b.x)+1000} height={Math.abs(a.y-b.y)+1000}><path d={d} fill="none" stroke="white" strokeWidth={22} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p}/></mask></defs><path d={d} fill="none" stroke="#080A10" strokeWidth={13} mask={`url(#${uid}-${i})`}/><path d={d} fill="none" stroke={lineColor} strokeWidth={7} strokeDasharray="17 12" mask={`url(#${uid}-${i})`}/></g>;})}
      </svg>
    </div>
  </AbsoluteFill>;
}

export function cardPorts(a:{x:number;y:number;width:number;height:number},b:{x:number;y:number;width:number;height:number}){
  const dx=b.x-a.x,dy=b.y-a.y;if(dx===0&&dy===0)return {a:{x:a.x,y:a.y},b:{x:b.x,y:b.y}};
  const edge=(n:typeof a)=>Math.min(dx===0?Infinity:n.width/2/Math.abs(dx),dy===0?Infinity:n.height/2/Math.abs(dy));
  const ea=edge(a),eb=edge(b);return {a:{x:a.x+dx*ea,y:a.y+dy*ea},b:{x:b.x-dx*eb,y:b.y-dy*eb}};
}
type JourneyPoint={x:number;y:number};
export function evidenceBoxes(nodes:Node[],portrait:boolean){
  return nodes.map((n,i)=>({...n,x:n.x??(portrait?(i%2)*500:i*560),y:n.y??(portrait?Math.floor(i/2)*620:(i%2)*130)}));
}
export function evidencePorts(a:JourneyPoint,b:JourneyPoint){
  const dx=b.x-a.x,dy=b.y-a.y;
  if(dx===0&&dy===0)throw new Error('Cartões conectados precisam de posições diferentes.');
  const edge=Math.min(dx===0?Infinity:180/Math.abs(dx),dy===0?Infinity:230/Math.abs(dy));
  return {a:{x:a.x+dx*edge,y:a.y+dy*edge},b:{x:b.x-dx*edge,y:b.y-dy*edge}};
}
export function evidenceCurve(a:JourneyPoint,b:JourneyPoint,p:number){
  const horizontal=Math.abs(b.x-a.x)>=Math.abs(b.y-a.y);
  const control=horizontal?{x:(a.x+b.x)/2,y:Math.min(a.y,b.y)-Math.max(120,Math.abs(b.x-a.x)*.45)}:{x:Math.min(a.x,b.x)-Math.max(120,Math.abs(b.y-a.y)*.35),y:(a.y+b.y)/2};
  const q=Math.max(0,Math.min(1,p)),point={x:(1-q)**2*a.x+2*(1-q)*q*control.x+q*q*b.x,y:(1-q)**2*a.y+2*(1-q)*q*control.y+q*q*b.y};
  const partial={x:a.x+(control.x-a.x)*q,y:a.y+(control.y-a.y)*q};
  return {point,control,path:`M ${a.x} ${a.y} Q ${partial.x} ${partial.y} ${point.x} ${point.y}`};
}
function EvidenceHQ(p:HQBackgroundOptions & {nodes:Node[];steps:Step[];timeline:ReturnType<typeof buildTimeline>;t:number;w:number;h:number;fontFamily:HQFont;ready:boolean;heading:string;cardColor:string;textColor:string;lineColor:string;zoomOutDuration:number;assets:Record<string,string>}){
  const {nodes,steps,timeline,t,w,h,fontFamily,ready,heading,cardColor,textColor,lineColor,zoomOutDuration,assets}=p;
  if(![cardColor,textColor,lineColor].every(c=>/^#[a-f\d]{6}$/i.test(c)))throw new Error('Cores de evidence devem usar #RRGGBB.');
  const fitted=React.useMemo(()=>new Map(nodes.map(n=>[n.id,{title:ready&&n.text?narrativeFit(n.text,fontFamily,300,66,43):undefined,caption:ready&&n.subtitle?narrativeFit(n.subtitle,fontFamily,300,48,24):undefined}])),[nodes,fontFamily,ready]);
  const boxes=evidenceBoxes(nodes,h>w),box=(id:string)=>boxes.find(n=>n.id===id)!;
  const links=timeline.steps.flatMap((s,i)=>{
    if(!i||s.connect===false||s.from===s.node)return [];
    const ports=evidencePorts(box(s.from!),box(s.node));
    return [{...s,index:i,...ports,curve:evidenceCurve(ports.a,ports.b,1)}];
  });
  const first=box(steps[0].node);let cx=first.x,cy=first.y,scale=Math.min(w*.78/360,h*.64/460);
  timeline.steps.forEach((s,i)=>{if(!i||t<s.start)return;const a=box(steps[i-1].node),b=box(s.node),q=s.move===0?1:smooth((t-s.start)/s.move);cx=a.x+(b.x-a.x)*q;cy=a.y+(b.y-a.y)*q;});
  const hull=links.flatMap(l=>[l.a,l.b,l.curve.control]);
  const left=Math.min(...boxes.map(n=>n.x-210),...hull.map(n=>n.x-30)),right=Math.max(...boxes.map(n=>n.x+210),...hull.map(n=>n.x+30));
  const top=Math.min(...boxes.map(n=>n.y-260),...hull.map(n=>n.y-30)),bottom=Math.max(...boxes.map(n=>n.y+270),...hull.map(n=>n.y+30));
  const overview=smooth((t-timeline.overviewAt)/zoomOutDuration),state=narrativeState(timeline,t),u=Math.min(w,h)/1080;
  if(t>=timeline.overviewAt){cx+=((left+right)/2-cx)*overview;cy+=((top+bottom)/2-cy)*overview;scale+=(Math.min(w*.84/(right-left),h*.72/(bottom-top))-scale)*overview;}
  return <AbsoluteFill style={{overflow:'hidden',fontFamily}}>
    <HQBackground backgroundStyle={p.backgroundStyle} backgroundColor={p.backgroundColor} backgroundOpacity={p.backgroundOpacity} paperTone={p.paperTone} gridBackgroundColor={p.gridBackgroundColor} gridLineColor={p.gridLineColor}/>
    <div style={{position:'absolute',left:0,top:0,transformOrigin:'0 0',transform:`translate(${w/2}px,${h/2}px) scale(${scale}) translate(${-cx}px,${-cy}px)`}}>
      {boxes.map((n,i)=>{
        const debut=timeline.firstByNode.get(n.id)!;if(t<debut.start)return null;
        if(n.asset&&!assets[n.asset])throw new Error('Asset ausente: '+n.asset);
        const reveal=debut.move===0?1:smooth((t-debut.start)/debut.move),accent=n.color??lineColor;
        let focus=steps[state.index].node===n.id?1:0;if(state.moving>=0)focus=steps[state.moving].node===n.id?state.progress:steps[state.moving-1].node===n.id?1-state.progress:0;
        const emphasis=focus+(1-focus)*overview;
        const {title,caption}=fitted.get(n.id)!;
        return <div key={n.id} style={{position:'absolute',left:n.x-180,top:n.y-230,width:360,height:460,boxSizing:'border-box',background:cardColor,border:'6px solid #080A10',boxShadow:'12px 14px 0 #080A10',opacity:ready?reveal*(.68+.32*emphasis):0,transform:`translateY(${40*(1-reveal)}px) scale(${.94+.06*reveal})`,overflow:'hidden'}}>
          <div style={{position:'absolute',inset:0,opacity:.10,backgroundImage:'radial-gradient(#080A10 1.5px,transparent 2px)',backgroundSize:'12px 12px'}}/>
          <div style={{position:'absolute',left:0,right:0,top:0,height:12,background:accent}}/>
          <div style={{position:'absolute',left:18,top:24,fontSize:28,color:textColor}}>{String(i+1).padStart(2,'0')}</div>
          {n.asset?<Img src={assets[n.asset]} style={{position:'absolute',left:22,top:65,width:304,height:226,objectFit:'contain',filter:`grayscale(${(1-emphasis)*.85})`}}/>:<div style={{position:'absolute',left:0,right:0,top:80,height:200,display:'grid',placeItems:'center',fontSize:135,color:accent}}>{String(i+1).padStart(2,'0')}</div>}
          <div style={{position:'absolute',left:20,right:20,top:310,height:5,background:accent}}/>
          {title&&<div style={{position:'absolute',left:24,top:330,width:300,height:66,whiteSpace:'pre',fontSize:title.size,lineHeight:1.08,color:textColor,textShadow:fontFamily==='Anton'?'none':'1px 2px 0 #080A1040'}}>{title.text}</div>}
          {caption&&<div style={{position:'absolute',left:24,top:398,width:300,height:48,whiteSpace:'pre',fontSize:caption.size,lineHeight:1.08,color:textColor,opacity:.8,textShadow:fontFamily==='Anton'?'none':'1px 1px 0 #080A1030'}}>{caption.text}</div>}
        </div>;
      })}
      <svg style={{position:'absolute',width:1,height:1,overflow:'visible',pointerEvents:'none'}}>
        {links.map(l=>{if(t<l.start)return null;const q=l.move===0?1:smooth((t-l.start)/l.move),d=evidenceCurve(l.a,l.b,q).path;return <g key={l.index} opacity={ready?1:0}><path d={d} fill='none' stroke='#080A10' strokeWidth={13} strokeLinecap='round'/><path d={d} fill='none' stroke={lineColor} strokeWidth={7} strokeLinecap='round'/>{[l.a,l.b].map((port,i)=><circle key={i} cx={port.x} cy={port.y} r={12} fill={box(l.node).color??lineColor} stroke='#080A10' strokeWidth={4} opacity={i===0?1:q}/>)}</g>;})}
      </svg>
    </div>
    {heading&&<div style={{position:'absolute',left:w*.08,top:h*.06,maxWidth:w*.68,background:cardColor,color:textColor,borderLeft:`${8*u}px solid ${lineColor}`,padding:`${10*u}px ${20*u}px`,fontSize:Math.min(36*u,w*.035),lineHeight:1.12,textTransform:'uppercase',overflowWrap:'anywhere',opacity:ready?1:0}}>{heading}</div>}
    <div style={{position:'absolute',right:w*.08,top:h*.06,background:cardColor,color:textColor,padding:`${10*u}px ${15*u}px`,fontSize:32*u,opacity:ready?1:0}}>{String(state.index+1).padStart(2,'0')} / {String(steps.length).padStart(2,'0')}</div>
    <div style={{position:'absolute',left:w*.08,right:w*.08,bottom:h*.07,display:'flex',gap:12*u}}>{timeline.steps.map((s,i)=><div key={i} style={{height:8*u,flex:1,background:lineColor,opacity:i<=state.index?1:.18}}/>)}</div>
  </AbsoluteFill>;
}
export function validateJourney(bend:number,size:number,color:string){
  if(!Number.isFinite(bend)||bend< -1||bend>1)throw new Error('pathBend: -1–1.');
  if(!Number.isFinite(size)||size<6||size>30)throw new Error('dotSize: 6–30 unidades virtuais.');
  if(!/^#[a-f\d]{6}$/i.test(color))throw new Error('dotColor deve usar #RRGGBB.');
}
export function journeyCurve(a:JourneyPoint,b:JourneyPoint,p:number,bend:number){
  const q=Math.max(0,Math.min(1,p)),c={x:(a.x+b.x)/2-(b.y-a.y)*bend,y:(a.y+b.y)/2+(b.x-a.x)*bend};
  const point={x:(1-q)**2*a.x+2*(1-q)*q*c.x+q*q*b.x,y:(1-q)**2*a.y+2*(1-q)*q*c.y+q*q*b.y};
  const control={x:a.x+(c.x-a.x)*q,y:a.y+(c.y-a.y)*q};
  return {point,path:`M ${a.x} ${a.y} Q ${control.x} ${control.y} ${point.x} ${point.y}`};
}
export function validateNarrative(nodes:Node[],heading:string){
  if(typeof heading!=='string'||heading.length>70)throw new Error('heading deve ser texto com até 70 caracteres.');
  nodes.forEach(n=>{if(n.subtitle!==undefined&&(typeof n.subtitle!=='string'||n.subtitle.length>120))throw new Error('subtitle deve ser texto com até 120 caracteres.');if(n.color&&!/^#[a-f\d]{6}$/i.test(n.color))throw new Error('Cor do ponto deve usar #RRGGBB.');});
}
export function narrativeState(timeline:ReturnType<typeof buildTimeline>,time:number){
  let index=0;timeline.steps.forEach((s,i)=>{if(time>=s.arrival-1e-8)index=i;});
  const moving=timeline.steps.findIndex(s=>s.move>0&&time>=s.start-1e-8&&time<s.arrival-1e-8);
  return {index,moving,progress:moving<0?1:smooth((time-timeline.steps[moving].start)/timeline.steps[moving].move)};
}
function narrativeFit(text:string,font:HQFont,width:number,height:number,max:number){
  const ctx=document.createElement('canvas').getContext('2d');if(!ctx)throw new Error('Canvas indisponível.');
  const wrap=(size:number)=>{ctx.font=`${size}px ${font}`;const lines:string[]=[];for(const paragraph of text.toLocaleUpperCase('pt-BR').split('\n')){let line='';for(const word of paragraph.split(/\s+/).filter(Boolean)){if(line&&ctx.measureText(line+' '+word).width>width){lines.push(line);line=word;}else line+=(line?' ':'')+word;}lines.push(line);}return lines;};
  let lo=1,hi=max;for(let i=0;i<18;i++){const size=(lo+hi)/2,lines=wrap(size);if(lines.length<=2&&lines.length*size*1.08<=height&&lines.every(l=>ctx.measureText(l).width<=width))lo=size;else hi=size;}const lines=wrap(lo);if(lines.length>2)throw new Error('Prefira frases curtas, com até duas linhas.');return {size:lo,text:lines.join('\n')};
}
function JourneyHQ(p:{nodes:Node[];steps:Step[];timeline:ReturnType<typeof buildTimeline>;t:number;w:number;h:number;fontFamily:HQFont;ready:boolean;textColor:string;lineColor:string;pathBend:number;dotColor:string;dotSize:number;zoomOutDuration:number;assets:Record<string,string>;narrative?:boolean;heading?:string} & HQBackgroundOptions){
  const {nodes,steps,timeline,t,w,h,fontFamily,ready,textColor,lineColor,pathBend,dotColor,dotSize,zoomOutDuration,assets}=p;
  const fitted=React.useMemo(()=>new Map(nodes.map(n=>[n.id,{title:p.narrative&&ready&&n.text?narrativeFit(n.text,fontFamily,412,n.asset?86:140,90):undefined,subtitle:p.narrative&&ready&&n.subtitle?narrativeFit(n.subtitle,fontFamily,412,58,29):undefined}])),[nodes,fontFamily,ready,p.narrative]);
  const state=narrativeState(timeline,t),overview=smooth((t-timeline.overviewAt)/zoomOutDuration),u=Math.min(w,h)/1080;
  if(![textColor,lineColor].every(c=>/^#[a-f\d]{6}$/i.test(c)))throw new Error('Cores do percurso devem usar #RRGGBB.');
  const boxes=nodes.map((n,i)=>({...n,x:n.x??(h>w?(i%2)*580:(i%3)*580),y:n.y??(h>w?Math.floor(i/2)*490:Math.floor(i/3)*490)}));
  const box=(id:string)=>boxes.find(n=>n.id===id)!;
  const point=(id:string)=>({x:box(id).x,y:box(id).y+130});
  let dot=point(steps[0].node);
  timeline.steps.forEach((s,i)=>{if(!i||t<s.start)return;dot=journeyCurve(point(steps[i-1].node),point(s.node),s.move===0?1:smooth((t-s.start)/s.move),pathBend).point;});
  let cx=dot.x,cy=dot.y-130,scale=Math.min(w*.78/500,h*.70/350);
  // Include full quadratic control hulls, not just nodes, so the overview contains every bend.
  const hull=timeline.steps.flatMap((s,i)=>{const a=point(i?steps[i-1].node:s.node),b=point(s.node);return [a,b,{x:(a.x+b.x)/2-(b.y-a.y)*pathBend,y:(a.y+b.y)/2+(b.x-a.x)*pathBend}];});
  const left=Math.min(...boxes.map(n=>n.x-260),...hull.map(v=>v.x-40)),right=Math.max(...boxes.map(n=>n.x+260),...hull.map(v=>v.x+40));
  const top=Math.min(...boxes.map(n=>n.y-240),...hull.map(v=>v.y-40)),bottom=Math.max(...boxes.map(n=>n.y+180),...hull.map(v=>v.y+40));
  if(t>=timeline.overviewAt){const q=smooth((t-timeline.overviewAt)/zoomOutDuration);cx+=((left+right)/2-cx)*q;cy+=((top+bottom)/2-cy)*q;scale+=(Math.min(w*.84/(right-left),h*.82/(bottom-top))-scale)*q;}
  return <AbsoluteFill style={{overflow:'hidden',fontFamily}}>
    <HQBackground backgroundStyle={p.backgroundStyle} backgroundColor={p.backgroundColor} backgroundOpacity={p.backgroundOpacity} paperTone={p.paperTone} gridBackgroundColor={p.gridBackgroundColor} gridLineColor={p.gridLineColor}/>
    <div style={{position:'absolute',left:0,top:0,transformOrigin:'0 0',transform:`translate(${w/2}px,${h/2}px) scale(${scale}) translate(${-cx}px,${-cy}px)`}}>
      <svg style={{position:'absolute',overflow:'visible',width:1,height:1}}>
        {timeline.steps.map((s,i)=>{if(!i||s.connect===false||t<s.start)return null;
          if(s.from!==steps[i-1].node)throw new Error('No modo path, from deve ser o ponto anterior; use cards para ramificações.');
          const a=point(s.from!),b=point(s.node),q=s.move===0?1:smooth((t-s.start)/s.move),d=journeyCurve(a,b,q,pathBend).path;
          return <g key={i}><path d={d} stroke='#080A10' strokeWidth={15} fill='none' strokeLinecap='round'/><path d={d} stroke={lineColor} strokeWidth={8} fill='none' strokeLinecap='round'/><path d={d} stroke='#FFF5D7' strokeWidth={2} opacity={.7} fill='none' strokeLinecap='round'/></g>;
        })}
        {boxes.map(n=>{const debut=timeline.firstByNode.get(n.id)!;if(t<debut.arrival)return null;return <g key={n.id}><circle cx={n.x+4} cy={n.y+134} r={21} fill='#080A10'/><circle cx={n.x} cy={n.y+130} r={20} fill={p.backgroundColor??'#18243C'} stroke={lineColor} strokeWidth={6}/></g>;})}
      </svg>
      {boxes.map(n=>{const debut=timeline.firstByNode.get(n.id)!;if(t<debut.start)return null;const q=debut.move===0?1:smooth((t-debut.start)/debut.move);if(n.asset&&!assets[n.asset])throw new Error('Asset ausente: '+n.asset);
        let focus=steps[state.index].node===n.id?1:0;if(state.moving>=0){focus=steps[state.moving].node===n.id?state.progress:steps[state.moving-1].node===n.id?1-state.progress:0;}
        const dim=p.narrative?(.18+.82*focus)*(1-overview)+overview:1;
        const {title,subtitle}=fitted.get(n.id)!;
        return <div key={n.id} style={{position:'absolute',left:n.x-220,top:n.y-190,width:440,height:280,opacity:ready?q*dim:0,scale:.94+.06*q,display:'flex',flexDirection:'column',justifyContent:'flex-end',alignItems:'center',gap:p.narrative?14:18}}>
          {n.asset&&<Img src={assets[n.asset]} style={{width:310,height:p.narrative?90:145,objectFit:'contain'}}/>}
          {n.text&&<div style={{width:440,boxSizing:'border-box',padding:'0 14px',textAlign:'center',textTransform:'uppercase',fontSize:title?.size??Math.min(76,330/Math.sqrt(Math.max(1,n.text.length/2))),lineHeight:1.08,color:n.color??textColor,whiteSpace:p.narrative?'pre':undefined,overflowWrap:p.narrative?undefined:'anywhere',textShadow:fontFamily==='Anton'?'none':'4px 5px 0 #080A10',WebkitTextStroke:fontFamily==='Anton'?'0px transparent':'.7px #080A10'}}>{title?.text??n.text}</div>}
          {subtitle&&<div style={{width:412,whiteSpace:'pre',textAlign:'center',fontSize:subtitle.size,lineHeight:1.08,color:textColor,textShadow:fontFamily==='Anton'?'none':'1px 2px 0 #080A10'}}>{subtitle.text}</div>}
        </div>;
      })}
      <svg style={{position:'absolute',overflow:'visible',width:1,height:1}}><circle cx={dot.x+5} cy={dot.y+6} r={dotSize+5} fill='#080A10'/><circle cx={dot.x} cy={dot.y} r={dotSize+4} fill='#FFF5D7' stroke='#080A10' strokeWidth={3}/><circle cx={dot.x} cy={dot.y} r={dotSize} fill={dotColor}/><circle cx={dot.x-dotSize*.25} cy={dot.y-dotSize*.3} r={dotSize*.25} fill='white'/></svg>
    </div>
    {p.narrative&&<>
      <div style={{position:'absolute',left:w*.08,right:w*.08,top:h*.07,display:'flex',gap:20*u,alignItems:'flex-start',justifyContent:'space-between',color:textColor,opacity:ready?1:0}}>
        <div style={{maxWidth:'75%',borderLeft:`${8*u}px solid ${lineColor}`,paddingLeft:18*u,fontSize:Math.min(38*u,w*.035),lineHeight:1.15,textTransform:'uppercase',overflowWrap:'anywhere'}}>{p.heading}</div>
        <div style={{fontSize:34*u,whiteSpace:'nowrap'}}>{String(state.index+1).padStart(2,'0')} / {String(steps.length).padStart(2,'0')}</div>
      </div>
      <div style={{position:'absolute',left:w*.08,right:w*.08,bottom:h*.09,display:'flex',gap:12*u}}>{timeline.steps.map((s,i)=><div key={i} style={{height:8*u,flex:1,background:i<=state.index?lineColor:textColor,opacity:i<=state.index?1:.16}}/>)}</div>
    </>}
  </AbsoluteFill>;
}

type HQFont = 'Bangers' | 'Anton';
export function resolveHQFont(family:HQFont, assets:{bangers?:string;anton?:string}){
  if(family!=='Bangers'&&family!=='Anton')throw new Error('fontFamily deve ser Bangers ou Anton.');
  const key=family==='Anton'?'anton':'bangers';
  if(!assets[key])throw new Error(`Informe assets.${key} para a fonte ${family}.`);
  return assets[key]!;
}
