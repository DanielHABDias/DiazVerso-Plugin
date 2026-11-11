import {SceneBackground as HQBackground,type SceneBackgroundProps as HQBackgroundOptions} from './SceneBackground';
import {progressHQ, fitLabelHQ} from './HQMotion';
import {HQComicPage, type HQComicPageOptions} from './HQComicPage';
import React from 'react';
import {AbsoluteFill, Freeze, OffthreadVideo, useCurrentFrame, useVideoConfig, delayRender, continueRender, cancelRender} from 'remotion';
import {loadFont} from './load-font';

type Clip = {asset: string; title?: string; subtitle?: string; sourceStart?: number; hold?: number; crt?: boolean};
type Props = HQBackgroundOptions & {fontFamily?: HQFont; clips: Clip[]; direction?: 'forward' | 'reverse'; backgroundColor?: string; accentColor?: string; textColor?: string;
  startDelay?: number; moveDuration?: number; enterDuration?: number; enterLast?: boolean; assets?: Record<string, string>};
const clamp = (v: number) => Math.max(0, Math.min(1, v));
const ease = (v: number) => {const p = clamp(v); return p*p*p*(p*(p*6-15)+10);};
const mix = (a: number, b: number, p: number) => a + (b - a) * p;

export default function LinhaDoTempoHQ({fontFamily='Anton', backgroundStyle="halftone", backgroundOpacity=100, paperTone="light", gridBackgroundColor="#10101A", gridLineColor="#858595", clips, direction = 'forward', backgroundColor = '#E8C64F', accentColor = '#2676E8', textColor = '#FFFFFF',
  startDelay = .3, moveDuration = .8, enterDuration = 1.05, enterLast = true, assets = {}}: Props) {
  const fontUrl=resolveHQFont(fontFamily,assets);
  const {width: w, height: h, fps, durationInFrames} = useVideoConfig();
  const t = useCurrentFrame() / fps;
  const horizontal = w > h;
  const u = Math.min(w, h) / 1080;
  if (!Array.isArray(clips) || !clips.length) throw new Error('Informe pelo menos um clip.');
  if (!['forward', 'reverse'].includes(direction)) throw new Error('direction deve ser forward ou reverse.');
  if (![backgroundColor, accentColor, textColor].every(c => /^#[a-f\d]{6}$/i.test(c))) throw new Error('Use cores #RRGGBB.');
  if (!Number.isFinite(startDelay) || startDelay < 0 || !Number.isFinite(moveDuration) || moveDuration <= 0 || !Number.isFinite(enterDuration) || enterDuration <= 0) throw new Error('Tempos de movimento inválidos.');
  clips.forEach(c => {
    if (!assets[c.asset]) throw new Error(`Asset ausente: ${c.asset}`);
    if (!Number.isFinite(c.hold ?? 2) || (c.hold ?? 2) < .35 || !Number.isFinite(c.sourceStart ?? 0) || (c.sourceStart ?? 0) < 0) throw new Error('hold deve ser >= .35 e sourceStart >= 0.');
  });
  if (!fontUrl) throw new Error('Informe fontUrl.');
  const [labels,setLabels]=React.useState<{title:ReturnType<typeof fitLabelHQ>;subtitle:ReturnType<typeof fitLabelHQ>}[]|null>(null);
  const [fontHandle] = React.useState(() => delayRender('Carregando Bangers da linha do tempo'));
  React.useEffect(() => {loadFont({family: fontFamily, url: fontUrl})
    .then(() => {setLabels(clips.map(c=>({title:fitLabelHQ(c.title??'',fontFamily,w*(horizontal?.55:.84),h*.13,(horizontal?72:94)*u),subtitle:fitLabelHQ(c.subtitle??'',fontFamily,w*(horizontal?.55:.84),h*.07,(horizontal?38:49)*u)})));continueRender(fontHandle);}).catch(cancelRender);}, [fontUrl,fontFamily,JSON.stringify(clips),w,h,fontHandle]);
  const indices = clips.map((_, i) => i);
  if (direction === 'reverse') indices.reverse();
  let cursor = startDelay;
  const schedule = indices.map((index, order) => {
    const at = cursor;
    const end = at + (clips[index].hold ?? 2);
    cursor = end + (order < clips.length - 1 ? moveDuration : 0);
    return {index, at, end};
  });
  const last = schedule[schedule.length - 1];
  const minimum = last.end + (enterLast ? enterDuration : 0);
  if (minimum > durationInFrames / fps + 1 / fps) throw new Error(`Cena curta: requer pelo menos ${minimum.toFixed(3)} segundos.`);
  const activeOrder = Math.max(0, schedule.findLastIndex(c => t >= c.at));
  const current = schedule[activeOrder];
  const next = schedule[activeOrder + 1];
  const spacing = w * (horizontal ? .78 : 1.08);
  const travel = next ? ease((t - current.end) / moveDuration) : 0;
  const camera = mix(current.index * spacing, (next?.index ?? current.index) * spacing, travel);
  const zoom = enterLast ? ease(progressHQ(t,last.end,enterDuration,fps)) : 0;
  const lineY = h * (horizontal ? .72 : .59);
  const cw = w * (horizontal ? .55 : .84);
  const ch = h * (horizontal ? .55 : .30);
  const top = lineY - ch - h * .055;
  const origin = w / 2 - camera;
  const progressStart = direction === 'forward' ? 0 : camera;
  const progressEnd = direction === 'forward' ? camera : (clips.length - 1) * spacing;

  return <AbsoluteFill style={{overflow: 'hidden', fontFamily: fontFamily}}>
    <HQBackground {...{backgroundStyle,backgroundColor,backgroundOpacity,paperTone,gridBackgroundColor,gridLineColor}}>
      <AbsoluteFill style={{opacity: .24 * (1 - zoom), backgroundImage: `radial-gradient(#080A11 ${3 * u}px, transparent ${3.8 * u}px)`, backgroundSize: `${19 * u}px ${19 * u}px`}} />
    </HQBackground>
    <AbsoluteFill style={{translate: `${Math.sin(t * .8) * 3 * u * (1 - zoom)}px ${Math.sin(t) * 4 * u * (1 - zoom)}px`, rotate: `${Math.sin(t * .6) * .18 * (1 - zoom)}deg`}}>
      <div style={{position: 'absolute', left: origin - w, top: lineY - 8 * u, width: (clips.length - 1) * spacing + 2 * w, height: 16 * u, background: '#FAF7E9', border: `${4 * u}px solid #080A11`, boxSizing: 'border-box', opacity: 1 - zoom}} />
      <div style={{position: 'absolute', left: origin + progressStart, top: lineY - 4 * u, width: Math.max(0, progressEnd - progressStart), height: 8 * u, background: accentColor, opacity: 1 - zoom}} />
      {schedule.map((cue, order) => {
        const c = clips[cue.index];
        const final = order === schedule.length - 1;
        const expanding = final ? zoom : 0;
        const revealDuration=Math.min(.3,(c.hold??2)*.3),dimDuration=Math.min(.24,(c.hold??2)*.3);
        const reveal = ease((t - cue.at) / revealDuration);
        const leave = !final ? ease((t - (cue.end - dimDuration)) / dimDuration) : 0;
        const light = reveal * (1 - leave);
        const elapsed = Math.max(0, Math.min(t, final && enterLast ? durationInFrames / fps : cue.end - (final ? 0 : dimDuration)) - cue.at);
        const x = origin + cue.index * spacing;
        return <React.Fragment key={cue.index}>
          <div style={{position: 'absolute', left: x - 18 * u, top: lineY - 18 * u, width: 36 * u, height: 36 * u, borderRadius: '50%', background: t >= cue.at ? accentColor : '#FAF7E9', border: `${5 * u}px solid #080A11`, boxSizing: 'border-box', opacity: 1 - zoom}} />
          <div style={{position: 'absolute', left: x - cw / 2, top: lineY + 43 * u, width: cw, textAlign: 'center', opacity: reveal * (1 - zoom), color: textColor,
            fontFamily: fontFamily, textTransform: 'uppercase', background: 'transparent',
            textShadow: fontFamily === 'Anton' ? 'none' : `${4 * u}px ${5 * u}px 0 #080A11, ${7 * u}px ${9 * u}px ${2 * u}px #080A1180`}}>
            <div style={{fontSize: labels?.[cue.index].title.size??(horizontal?72:94)*u, lineHeight:1.08,whiteSpace:'pre'}}>{labels?.[cue.index].title.lines.join('\n')??c.title}</div>
            <div style={{fontSize:labels?.[cue.index].subtitle.size??(horizontal?38:49)*u, marginTop:14*u,lineHeight:1.08,whiteSpace:'pre'}}>{labels?.[cue.index].subtitle.lines.join('\n')??c.subtitle}</div>
          </div>
          <div style={{position: 'absolute', left: mix(x - cw / 2, 0, expanding), top: mix(top + (1 - reveal) * 40 * u, 0, expanding), width: mix(cw, w, expanding), height: mix(ch, h, expanding), boxSizing: 'border-box', border: `${8 * u * (1 - expanding)}px solid ${accentColor}`, background: '#080A11', overflow: 'hidden', opacity: reveal * (final ? 1 : 1 - zoom), zIndex: final && zoom > 0 ? 20 : 2, boxShadow: `${11 * u * (1 - expanding)}px ${13 * u * (1 - expanding)}px 0 #080A11`}}>
            <AbsoluteFill style={{filter: `grayscale(${1 - light}) brightness(${.32 + .68 * light})`}}>
              {(Math.abs(x-w/2)<w+cw || expanding>0)&&<Freeze frame={Math.round(elapsed * fps)}><OffthreadVideo src={assets[c.asset]} muted trimBefore={Math.round((c.sourceStart ?? 0) * fps)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'center'}} /></Freeze>}
              {c.crt && <AbsoluteFill style={{backgroundImage: `radial-gradient(circle, transparent 45%, #0006 100%), repeating-linear-gradient(to bottom, #0004 0px, #0004 ${u}px, #FFFFFF08 ${2 * u}px, transparent ${4 * u}px)`}} />}
            </AbsoluteFill>
          </div>
        </React.Fragment>;
      })}
      <div style={{position: 'absolute', left: w / 2 - 9 * u, top: lineY - 9 * u, width: 18 * u, height: 18 * u, borderRadius: '50%', background: '#FFFFFF', opacity: (1 - zoom) * ease((t - startDelay) / .2), zIndex: 5}} />
    </AbsoluteFill>
  </AbsoluteFill>;
}

type HQFont = 'Bangers' | 'Anton';
export function resolveHQFont(family:HQFont, assets:{bangers?:string;anton?:string}){
  if(family!=='Bangers'&&family!=='Anton')throw new Error('fontFamily deve ser Bangers ou Anton.');
  const key=family==='Anton'?'anton':'bangers';
  if(!assets[key])throw new Error(`Informe assets.${key} para a fonte ${family}.`);
  return assets[key]!;
}
