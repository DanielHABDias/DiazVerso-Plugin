import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {imageBoundsHQ} from './HQMotion';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill, Img, cancelRender, continueRender, delayRender, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Card = {asset: string; title: string; caption?: string; at?: number; cardColor?: string; accentColor?: string};
type Props = HQBackgroundOptions & {fontFamily?: HQFont; title: string; subtitle?: string; items: Card[]; columns?: number;
  backgroundColor?: string; cardColor?: string; textColor?: string; cardTextColor?: string; accentColor?: string;
  startDelay?: number; stagger?: number; entryDuration?: number; textDuration?: number; stackOffset?: number;
  assets?: Record<string, string>};
type Bounds = {x: number; y: number; width: number; height: number; sourceWidth: number; sourceHeight: number};
type TextLayout = {lines: string[]; size: number};
const clamp = (v: number) => Math.max(0, Math.min(1, v));
const ease = (v: number) => 1 - Math.pow(1 - clamp(v), 3);

export function gallerySlot(index: number, columns: number) {
  return {column: index % columns, layer: Math.floor(index / columns)};
}
export function galleryDepth(index: number, columns: number, starts: number[], time: number, entryDuration: number) {
  let depth = 0;
  for (let next = index + columns; next < starts.length; next += columns) depth += ease((time - starts[next]) / entryDuration);
  return Math.min(3, depth);
}
export function galleryDepths(columns:number,starts:number[],time:number,entryDuration:number){
  const totals=Array(columns).fill(0),depths=Array(starts.length).fill(0);
  for(let i=starts.length-1;i>=0;i--){const col=i%columns;depths[i]=Math.min(3,totals[col]);totals[col]+=ease((time-starts[i])/entryDuration);}
  return depths;
}

function fit(text: string, width: number, height: number, max: number, fontFamily:HQFont='Bangers'): TextLayout {
  const ctx = document.createElement('canvas').getContext('2d');if (!ctx) throw new Error('Canvas indisponível.');
  const wrap = (size: number) => {
    ctx.font = `${size}px ${fontFamily}`;
    const lines: string[] = [];let line = '';
    for (const word of text.split(/\s+/)) {
      if (ctx.measureText(word).width > width) {
        if (line) {lines.push(line);line = '';}
        for (const char of Array.from(word)) {
          if (line && ctx.measureText(line + char).width > width) {lines.push(line);line = '';}
          line += char;
        }
      } else if (line && ctx.measureText(line + ' ' + word).width > width) {lines.push(line);line = word;}
      else line += (line ? ' ' : '') + word;
    }
    if (line) lines.push(line);return lines;
  };
  let low = 1, high = max;
  for (let i = 0; i < 18; i++) {
    const size = (low + high) / 2;const lines = wrap(size);
    if (lines.length <= 2 && lines.length * size * 1.08 <= height && lines.every(line => ctx.measureText(line).width <= width)) low = size;
    else high = size;
  }
  return {lines: wrap(low), size: low};
}
const boundsFor=imageBoundsHQ;

export default function GaleriaCartasHQ({fontFamily='Anton', backgroundStyle="halftone", backgroundOpacity=100, paperTone="light", gridBackgroundColor="#10101A", gridLineColor="#858595", title, subtitle = '', items, columns,
  backgroundColor = '#1B2943', cardColor = '#F6EDD8', textColor = '#FFFFFF', cardTextColor = '#111723', accentColor = '#F4C542',
  startDelay = .25, stagger = 1.1, entryDuration = .65, textDuration = .2, stackOffset = 16, assets = {}}: Props) {
  const fontUrl=resolveHQFont(fontFamily,assets);
  const {width: w, height: h, fps, durationInFrames} = useVideoConfig();
  const t = useCurrentFrame() / fps;const horizontal = w > h;const u = Math.min(w, h) / 1080;
  if (!title?.trim() || !Array.isArray(items) || !items.length) throw new Error('Informe title e ao menos um item.');
  if (!fontUrl) throw new Error('Informe fontUrl.');
  const requestedColumns = columns ?? (horizontal ? 3 : 2);
  if (!Number.isInteger(requestedColumns) || requestedColumns < 1 || requestedColumns > 4) throw new Error('columns deve ser de 1 a 4.');
  const count = Math.min(requestedColumns, items.length);
  if (![backgroundColor, cardColor, textColor, cardTextColor, accentColor, ...items.flatMap(item => [item.cardColor ?? cardColor, item.accentColor ?? accentColor])].every(color => /^#[a-f\d]{6}$/i.test(color))) throw new Error('Cores devem usar #RRGGBB.');
  if (![startDelay, stagger, entryDuration, textDuration, stackOffset].every(Number.isFinite) || startDelay < 0 || stagger < 0 || entryDuration <= 0 || textDuration <= 0 || stackOffset < 0 || stackOffset > 24) throw new Error('Tempos inválidos ou stackOffset fora de 0–24.');
  const starts = items.map((item, i) => item.at ?? startDelay + i * stagger);
  items.forEach((item, i) => {
    if (!item.title?.trim() || !assets[item.asset]) throw new Error('Cada carta requer title e uma chave asset existente.');
    if (!Number.isFinite(starts[i]) || starts[i] < 0 || starts[i] + entryDuration + textDuration > durationInFrames / fps + 1e-8) throw new Error('A entrada da carta e de seu texto precisa caber na cena.');
    if (i && starts[i] < starts[i - 1]) throw new Error('Os horários at devem seguir a ordem dos itens.');
    if (i >= count && starts[i] < starts[i - count] + entryDuration + textDuration - 1e-8) throw new Error('Uma carta não pode encobrir outra antes de sua entrada e texto terminarem.');
  });
  const gap = w * .035;
  const cw = (w * .86 - gap * (count - 1)) / count;
  const ch = Math.min(h * .58, cw * 1.95);
  const top = h * (subtitle.trim() ? .29 : .25);
  const [prepared, setPrepared] = React.useState<{bounds: Bounds[]; labels: TextLayout[]; captions: TextLayout[]; heading: TextLayout; sub: TextLayout} | null>(null);
  const [handle] = React.useState(() => delayRender('Preparando galeria de cartas HQ'));
  const signature = JSON.stringify({items, assets, title, subtitle, cw, ch, w, h});
  React.useEffect(() => {let live=true;
    Promise.all([loadFont({family: fontFamily, url: fontUrl}), Promise.all(items.map(item => boundsFor(assets[item.asset])))])
      .then(([, bounds]) => {if(!live)return;
        setPrepared({bounds,
          labels: items.map(item => fit(item.title.normalize('NFC').toLocaleUpperCase('pt-BR'), cw * .86, ch * .15, 65 * u, fontFamily)),
          captions: items.map(item => fit((item.caption ?? '').toLocaleUpperCase('pt-BR'), cw * .86, ch * .08, 32 * u, fontFamily)),
          heading: fit(title.toLocaleUpperCase('pt-BR'), w * .86, h * .105, 100 * u, fontFamily),
          sub: fit(subtitle.toLocaleUpperCase('pt-BR'), w * .86, h * .045, 38 * u, fontFamily)});
        continueRender(handle);
      }).catch(error=>{if(live)cancelRender(error);});return()=>{live=false;};}, [signature, fontFamily, fontUrl, handle]);
  const depths=galleryDepths(count,starts,t,entryDuration);
  return <AbsoluteFill style={{overflow: 'hidden',  fontFamily: fontFamily}}>
    <HQBackground {...{backgroundStyle,backgroundColor,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor}}>
      <AbsoluteFill style={{opacity: .18, backgroundImage: `radial-gradient(#080A11 ${3.2 * u}px, transparent ${3.8 * u}px)`, backgroundSize: `${19 * u}px ${19 * u}px`}} />
    </HQBackground>
    {prepared && <>
      <div style={{position: 'absolute', zIndex: 2, left: '7%', top: '6%', width: '86%', color: textColor,
        textShadow: fontFamily === 'Anton' ? 'none' : `${4 * u}px ${6 * u}px 0 #080A11`, fontSize: prepared.heading.size, lineHeight: 1.08, whiteSpace: 'pre'}}>{prepared.heading.lines.join('\n')}</div>
      {subtitle.trim() && <div style={{position: 'absolute', zIndex: 2, left: '7%', top: '17.5%', width: '86%', color: textColor,
        fontSize: prepared.sub.size, lineHeight: 1.08, opacity: .8, whiteSpace: 'pre'}}>{prepared.sub.lines.join('\n')}</div>}
      <div style={{position: 'absolute', left: '7%', top: subtitle.trim() ? '24%' : '20%', width: '86%', height: 4 * u, background: accentColor}} />
      <AbsoluteFill style={{zIndex: 1}}>{items.map((item, i) => {
        if (t < starts[i] || (i+count*4<items.length && t>=starts[i+count*4]+entryDuration)) return null;
        const {column} = gallerySlot(i, count);const progress = ease((t - starts[i]) / entryDuration);
        const depth = depths[i];
        const bx = w * .07 + column * (cw + gap);
        const dx = depth * stackOffset * u * (column % 2 ? 1 : -1);
        const dy = depth * stackOffset * u;
        const color = item.accentColor ?? accentColor;
        const bounds = prepared.bounds[i];const pictureW = cw * .86, pictureH = ch * .65;
        const size = Math.min(pictureW / bounds.width, pictureH / bounds.height);
        const iw = bounds.width * size, ih = bounds.height * size;
        const next=starts[i+count];
        const occlusion=next===undefined?0:ease((t-next-entryDuration*.45)/(entryDuration*.55));
        const contentOpacity = 1 - clamp(occlusion);
        const labelP = ease((t - starts[i] - entryDuration) / textDuration);
        return <div key={i} style={{position: 'absolute', left: bx + dx, top: top + dy, width: cw, height: ch, zIndex: i + 1,
          translate: `0 ${(1 - progress) * (h-top+30*u)}px`, scale: 1 - depth * .025, rotate: `${depth * (column % 2 ? .8 : -.8)}deg`,
          boxSizing: 'border-box', background: item.cardColor ?? cardColor, border: `${6 * u}px solid #080A11`, boxShadow: `${10 * u}px ${12 * u}px 0 #080A11`, transformOrigin: 'center'}}>
          <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 8 * u, background: color}} />
          <AbsoluteFill style={{opacity: .08, backgroundImage: `radial-gradient(#080A11 ${2 * u}px, transparent ${2.5 * u}px)`, backgroundSize: `${15 * u}px ${15 * u}px`}} />
          <AbsoluteFill style={{opacity: contentOpacity}}>
            <div style={{position: 'absolute', left: 14 * u, top: 16 * u, background: color, color: '#080A11', padding: `${3 * u}px ${9 * u}px`, fontSize: 27 * u}}>{String(i + 1).padStart(2, '0')}</div>
            <div style={{position: 'absolute', left: (cw - iw) / 2, top: ch * .07 + (pictureH - ih) / 2, width: iw, height: ih, overflow: 'hidden'}}>
              <Img src={assets[item.asset]} style={{position: 'absolute', left: -bounds.x * size, top: -bounds.y * size,
                width: bounds.sourceWidth * size, height: bounds.sourceHeight * size, maxWidth: 'none'}} />
            </div>
            <div style={{position: 'absolute', left: '7%', top: '75%', width: '86%', opacity: labelP, color: cardTextColor,
              fontSize: prepared.labels[i].size, lineHeight: 1.08, whiteSpace: 'pre', textShadow: fontFamily === 'Anton' ? 'none' : `${1.5 * u}px ${2 * u}px 0 #00000022`}}>{prepared.labels[i].lines.join('\n')}</div>
            {item.caption && <div style={{position: 'absolute', left: '7%', top: '91%', width: '86%', color: cardTextColor, opacity: labelP * .8,
              fontSize: prepared.captions[i].size, lineHeight: 1.08, whiteSpace: 'pre'}}>{prepared.captions[i].lines.join('\n')}</div>}
          </AbsoluteFill>
        </div>;
      })}</AbsoluteFill>
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
