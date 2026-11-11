import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {edgeTravelHQ, imageBoundsHQ} from './HQMotion';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill, Img, cancelRender, continueRender, delayRender, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Item = {asset: string; text: string; at?: number};
type Props = HQBackgroundOptions & {fontFamily?: HQFont; items: Item[]; title?: string; backgroundColor?: string; textColor?: string;
  startDelay?: number; stagger?: number; entryDuration?: number; textDuration?: number; assets?: Record<string, string>};
type Slot = {x: number; y: number; width: number; height: number; fromX: number; fromY: number};
type Bounds = {x: number; y: number; width: number; height: number; sourceWidth: number; sourceHeight: number};
type TextLayout = {lines: string[]; size: number};
const clamp = (v: number) => Math.max(0, Math.min(1, v));
const ease = (v: number) => {const p = clamp(v);return 1 - Math.pow(1 - p, 3);};

export function comparisonLayout(count: number, w: number, h: number, hasTitle = false): Slot[] {
  if (![2, 3, 4].includes(count)) throw new Error('Comparativo requer de 2 a 4 itens.');
  const horizontal = w > h;
  const top = hasTitle ? .20 : .09;
  const bottom = .91;
  const make = (x: number, y: number, width: number, height: number, fromX: number, fromY: number) => ({x: x * w, y: y * h, width: width * w, height: height * h, fromX, fromY});
  if (horizontal && count < 4) {
    const gap = .045;const width = (.86 - gap * (count - 1)) / count;
    return Array.from({length: count}, (_, i) => make(.07 + i * (width + gap), top, width, bottom - top,
      i === 0 ? -1 : i === count - 1 ? 1 : 0, count === 3 && i === 1 ? -1 : 0));
  }
  if (!horizontal && count === 2) {
    const height = (bottom - top - .045) / 2;
    return [make(.09, top, .82, height, 0, -1), make(.09, top + height + .045, .82, height, 0, 1)];
  }
  const height = (bottom - top - .055) / 2;
  if (!horizontal && count === 3) return [make(.20, top, .60, height, 0, -1),
    make(.07, top + height + .055, .40, height, -1, 1), make(.53, top + height + .055, .40, height, 1, 1)];
  return Array.from({length: 4}, (_, i) => make(i % 2 ? .53 : .07, top + Math.floor(i / 2) * (height + .055), .40, height,
    i % 2 ? 1 : -1, i < 2 ? -1 : 1));
}

function fitText(text: string, width: number, height: number, maximum: number, fontFamily:HQFont='Bangers'): TextLayout {
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
  let low = 1, high = maximum;
  for (let i = 0; i < 18; i++) {
    const size = (low + high) / 2;const lines = wrap(size);
    if (lines.length <= 3 && lines.length * size * 1.08 <= height && lines.every(line => ctx.measureText(line).width <= width)) low = size;
    else high = size;
  }
  return {lines: wrap(low), size: low};
}

const imageBounds=imageBoundsHQ;

export default function ComparativoIdeiasHQ({fontFamily='Anton', backgroundStyle="halftone", backgroundOpacity=100, paperTone="light", gridBackgroundColor="#10101A", gridLineColor="#858595", items, title = '', backgroundColor = '#D6AD42', textColor = '#FFFFFF',
  startDelay = .15, stagger = .45, entryDuration = .6, textDuration = .25, assets = {}}: Props) {
  const fontUrl=resolveHQFont(fontFamily,assets);
  const {width: w, height: h, fps, durationInFrames} = useVideoConfig();
  const t = useCurrentFrame() / fps;
  if (!Array.isArray(items) || ![2, 3, 4].includes(items.length)) throw new Error('Informe items com 2, 3 ou 4 imagens.');
  if (!fontUrl) throw new Error('Informe fontUrl.');
  if (![backgroundColor, textColor].every(c => /^#[a-f\d]{6}$/i.test(c))) throw new Error('Cores devem usar #RRGGBB.');
  if (![startDelay, stagger, entryDuration, textDuration].every(Number.isFinite) || startDelay < 0 || stagger < 0 || entryDuration <= 0 || textDuration <= 0) throw new Error('Tempos inválidos.');
  const starts = items.map((item, i) => item.at ?? startDelay + i * stagger);
  items.forEach((item, i) => {
    if (!item.text?.trim() || !assets[item.asset]) throw new Error('Cada item precisa de text e uma chave asset existente.');
    if (!Number.isFinite(starts[i]) || starts[i] < 0 || starts[i] + entryDuration + textDuration > durationInFrames / fps + 1e-8) throw new Error('Imagem e texto devem terminar de entrar antes do fim da cena.');
  });
  const slots = comparisonLayout(items.length, w, h, Boolean(title.trim()));
  const unit = Math.min(w, h) / 1080;
  const [prepared, setPrepared] = React.useState<{bounds: Bounds[]; labels: TextLayout[]; heading: TextLayout | null} | null>(null);
  const [handle] = React.useState(() => delayRender('Preparando comparativo de ideias'));
  const signature = JSON.stringify({items, assets, w, h, title});
  React.useEffect(() => {let live=true;
    Promise.all([loadFont({family: fontFamily, url: fontUrl}), Promise.all(items.map(item => imageBounds(assets[item.asset])))])
      .then(([, bounds]) => {if(!live)return;
        const labels = items.map((item, i) => fitText(item.text.normalize('NFC').toLocaleUpperCase('pt-BR').trim(), slots[i].width * .94, slots[i].height * .25,
          Math.min(88 * unit, slots[i].width * .16), fontFamily));
        const heading = title.trim() ? fitText(title.toLocaleUpperCase('pt-BR'), w * .84, h * .10, 94 * unit, fontFamily) : null;
        setPrepared({bounds, labels, heading});continueRender(handle);
      }).catch(error=>{if(live)cancelRender(error);});return()=>{live=false;};}, [signature, fontFamily, fontUrl, handle]);
  const textStyle: React.CSSProperties = {fontFamily: fontFamily, color: textColor, lineHeight: 1.08, whiteSpace: 'pre',
    WebkitTextStroke: fontFamily === 'Anton' ? '0px transparent' : `${1.5 * unit}px #080A11`, textShadow: fontFamily === 'Anton' ? 'none' : `${5 * unit}px ${7 * unit}px 0 #080A11`};
  return <AbsoluteFill style={{ overflow: 'hidden'}}>
    <HQBackground {...{backgroundStyle,backgroundColor,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor}}>
      <AbsoluteFill style={{opacity: .17, backgroundImage: `radial-gradient(#080A11 ${3.2 * unit}px, transparent ${3.8 * unit}px)`, backgroundSize: `${19 * unit}px ${19 * unit}px`}} />
    </HQBackground>
    {prepared?.heading && <div style={{...textStyle, position: 'absolute', left: '8%', top: '6%', width: '84%', textAlign: 'center', fontSize: prepared.heading.size}}>{prepared.heading.lines.join('\n')}</div>}
    {prepared && items.map((item, i) => {
      const slot = slots[i];const box = prepared.bounds[i];const label = prepared.labels[i];
      const progress = ease((t - starts[i]) / entryDuration);
      const labelP = ease((t - starts[i] - entryDuration) / textDuration);
      const imageH = slot.height * .69;
      const size = Math.min(slot.width * .92 / box.width, imageH / box.height);
      const imageW = box.width * size;const visibleH = box.height * size;
      return <React.Fragment key={i}>
        <div style={{position: 'absolute', left: slot.x + (slot.width - imageW) / 2, top: slot.y + (imageH - visibleH) / 2,
          width: imageW, height: visibleH, overflow: 'hidden', opacity: t < starts[i] ? 0 : 1,
          translate: `${slot.fromX * edgeTravelHQ(slot.x+(slot.width-imageW)/2,imageW,w,slot.fromX,30*unit) * (1 - progress)}px ${slot.fromY * edgeTravelHQ(slot.y+(imageH-visibleH)/2,visibleH,h,slot.fromY,30*unit) * (1 - progress)}px`}}>
          <Img src={assets[item.asset]} style={{position: 'absolute', left: -box.x * size, top: -box.y * size,
            width: box.sourceWidth * size, height: box.sourceHeight * size, maxWidth: 'none'}} />
        </div>
        <div style={{...textStyle, position: 'absolute', left: slot.x + slot.width * .03, top: slot.y + slot.height * .74,
          width: slot.width * .94, height: slot.height * .25, display: 'flex', justifyContent: 'center', alignItems: 'center',
          textAlign: 'center', fontSize: label.size, opacity: labelP, translate: `0 ${(1 - labelP) * 12 * unit}px`}}>{label.lines.join('\n')}</div>
      </React.Fragment>;
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
