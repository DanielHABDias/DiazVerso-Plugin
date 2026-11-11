import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {imageBoundsHQ} from './HQMotion';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill, Img, cancelRender, continueRender, delayRender, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from './load-font';

type Phrase = {text: string; at: number; color?: string; size?: number};
type Props = HQBackgroundOptions & {fontFamily?: HQFont; phrases: Phrase[]; imageSide?: 'left' | 'right'; label?: string;
  backgroundColor?: string; textColor?: string; mutedColor?: string; accentColor?: string; glowColor?: string;
  glowIntensity?: number; imageScale?: number; assets?: {image?: string; bangers?: string; anton?: string}};
type Line = {text: string; size: number; height: number};
type Bounds = {x: number; y: number; width: number; height: number; sourceWidth: number; sourceHeight: number};

export function phraseVisible(at: number, frame: number, fps: number) {
  return frame >= Math.ceil(at * fps - 1e-8);
}
export function phraseColor(index: number, muted: string, white: string, accent: string) {
  return [muted, white, accent][index % 3];
}

function wrap(text: string, size: number, width: number, ctx: CanvasRenderingContext2D, fontFamily:HQFont='Bangers') {
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
}
function textLayout(phrases: Phrase[], width: number, height: number, maximum: number, gap: number, fontFamily:HQFont='Bangers'): Line[] {
  const ctx = document.createElement('canvas').getContext('2d');if (!ctx) throw new Error('Canvas indisponível.');
  const calculate = (base: number) => phrases.map(phrase => {
    const size = base * (phrase.size ?? 1);
    const lines = wrap(phrase.text.normalize('NFC').toLocaleUpperCase('pt-BR').trim(), size, width, ctx, fontFamily);
    return {text: lines.join('\n'), size, height: lines.length * size * 1.04};
  });
  let low = 1, high = maximum;
  for (let i = 0; i < 18; i++) {
    const base = (low + high) / 2;
    const lines = calculate(base);
    if (lines.reduce((sum, line) => sum + line.height, 0) + Math.max(0, phrases.length - 1) * gap <= height) low = base;
    else high = base;
  }
  return calculate(low);
}
const imageBounds=imageBoundsHQ;

export default function ImagemFrasesHQ({fontFamily='Anton', backgroundStyle="halftone", backgroundOpacity=100, paperTone="light", gridBackgroundColor="#10101A", gridLineColor="#858595", phrases, imageSide = 'right', label = '', backgroundColor = '#111522',
  textColor = '#FFFFFF', mutedColor = '#A6A9B1', accentColor = '#EF3F49', glowColor,
  glowIntensity = .65, imageScale = 1, assets = {}}: Props) {
  const fontUrl=resolveHQFont(fontFamily,assets);
  const {width: w, height: h, fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();const horizontal = w > h;const u = Math.min(w, h) / 1080;
  if (!Array.isArray(phrases) || !phrases.length) throw new Error('Informe ao menos uma frase.');
  if (!assets.image || !fontUrl) throw new Error('Informe assets.image e fontUrl.');
  if (!['left', 'right'].includes(imageSide)) throw new Error('imageSide deve ser left ou right.');
  const glow = glowColor ?? accentColor;
  if (![backgroundColor, textColor, mutedColor, accentColor, glow, ...phrases.map(p => p.color ?? textColor)].every(c => /^#[a-f\d]{6}$/i.test(c))) throw new Error('Cores devem usar #RRGGBB.');
  if (!Number.isFinite(imageScale) || imageScale < .25 || imageScale > 1 || !Number.isFinite(glowIntensity) || glowIntensity < 0 || glowIntensity > 1) throw new Error('imageScale deve ser 0.25–1; glowIntensity 0–1.');
  phrases.forEach((phrase, i) => {
    if (!phrase.text?.trim() || !Number.isFinite(phrase.at) || phrase.at < 0 || Math.ceil(phrase.at * fps - 1e-8) >= durationInFrames || (i > 0 && phrase.at < phrases[i - 1].at)) throw new Error('Frases precisam de text e at ordenado dentro da cena.');
    if (!Number.isFinite(phrase.size ?? 1) || (phrase.size ?? 1) < .4 || (phrase.size ?? 1) > 1.5) throw new Error('size relativo da frase deve ser 0.4–1.5.');
  });
  const picture = horizontal ? {x: w * (imageSide === 'right' ? .59 : .07), y: h * .16, width: w * .34, height: h * .69}
    : {x: w * .16, y: h * .13, width: w * .68, height: h * .35};
  const textBox = horizontal ? {x: w * (imageSide === 'right' ? .07 : .47), y: h * .23, width: w * .46, height: h * .57}
    : {x: w * .10, y: h * .55, width: w * .80, height: h * .34};
  const gap = Math.min(18 * u, textBox.height * .18 / phrases.length);
  const [prepared, setPrepared] = React.useState<{bounds: Bounds; lines: Line[]; label: Line[]} | null>(null);
  const [handle] = React.useState(() => delayRender('Preparando imagem e frases HQ'));
  const signature = JSON.stringify({phrases, assets, w, h, label, imageSide});
  React.useEffect(() => {let live=true;
    Promise.all([loadFont({family: fontFamily, url: fontUrl}), imageBounds(assets.image!)]).then(([, bounds]) => {if(!live)return;
      setPrepared({bounds, lines: textLayout(phrases, textBox.width, textBox.height, horizontal ? 140 * u : 122 * u, gap, fontFamily),
        label: label.trim() ? textLayout([{text: label, at: 0}], w * .86, h * .04, 34 * u, 0, fontFamily) : []});
      continueRender(handle);
    }).catch(error=>{if(live)cancelRender(error);});return()=>{live=false;};}, [signature, fontFamily, fontUrl, handle]);
  const scale = prepared ? Math.min(picture.width / prepared.bounds.width, picture.height / prepared.bounds.height) * imageScale : 1;
  const iw = prepared ? prepared.bounds.width * scale : 0, ih = prepared ? prepared.bounds.height * scale : 0;
  let lineY = 0;
  return <AbsoluteFill style={{ overflow: 'hidden', fontFamily: fontFamily}}>
    <HQBackground {...{backgroundStyle,backgroundColor,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor}}>
      <AbsoluteFill style={{opacity: .10, backgroundImage: `radial-gradient(#FFFFFF ${2.3 * u}px, transparent ${3 * u}px)`, backgroundSize: `${18 * u}px ${18 * u}px`}} />
    </HQBackground>
    <div style={{position: 'absolute', left: picture.x - picture.width * .12, top: picture.y - picture.height * .08,
      width: picture.width * 1.24, height: picture.height * 1.16, opacity: glowIntensity,
      background: `radial-gradient(ellipse at center, ${glow}70 0%, ${glow}30 38%, ${glow}00 72%)`}} />
    {prepared && <>
      {prepared.label.length > 0 && <div style={{position: 'absolute', left: '7%', top: '6%', color: accentColor, fontSize: prepared.label[0].size, whiteSpace: 'pre', lineHeight: 1.04}}>{prepared.label[0].text}</div>}
      <div style={{position: 'absolute', left: picture.x + (picture.width - iw) / 2, top: picture.y + (picture.height - ih) / 2, width: iw, height: ih, overflow: 'hidden'}}>
        <Img src={assets.image} style={{position: 'absolute', left: -prepared.bounds.x * scale, top: -prepared.bounds.y * scale,
          width: prepared.bounds.sourceWidth * scale, height: prepared.bounds.sourceHeight * scale, maxWidth: 'none'}} />
      </div>
      <div style={{position: 'absolute', left: textBox.x, top: textBox.y, width: textBox.width, height: textBox.height}}>
        {phrases.map((phrase, i) => {
          const line = prepared.lines[i];const top = lineY;lineY += line.height + gap;
          return <div key={i} style={{position: 'absolute', top, left: 0, width: '100%', height: line.height,
            fontSize: line.size, whiteSpace: 'pre', lineHeight: 1.04, color: phrase.color ?? phraseColor(i, mutedColor, textColor, accentColor),
            textShadow: fontFamily === 'Anton' ? 'none' : `${4 * u}px ${6 * u}px 0 #080A11`, opacity: phraseVisible(phrase.at, frame, fps) ? 1 : 0}}>{line.text}</div>;
        })}
      </div>
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
