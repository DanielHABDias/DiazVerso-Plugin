/** kinetic-text — pure word timing and contrast checks for kinetic typography.
 * This is a pre-render mathematical gate, not a visual or audio QA result.
 */
const RGB = /^#[0-9a-fA-F]{6}$/;
export function luminance(hex) {
  if (typeof hex !== 'string' || !RGB.test(hex)) throw new Error('Use #RRGGBB');
  const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255)
    .map(v=>v<=0.04045?v/12.92:((v+0.055)/1.055)**2.4);
  return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
}
export function contrastRatio(a,b) {
  const x=luminance(a),y=luminance(b);
  return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);
}
export function verifyPalette(foreground,background,{largeText=false}={}) {
  const ratio=contrastRatio(foreground,background);
  const minimum=largeText?3:4.5;
  return {ratio:Number(ratio.toFixed(3)),minimum,passes:ratio+1e-9>=minimum,
    scope:'opaque solid background only; does not inspect rendered pixels'};
}
/** Word timings are scene-relative integer frames, sourced from verified cues.
 * Non-overlap and scene bounds protect deterministic Remotion frame selection.
 */
export function validateWords(words,sceneDurationFrames) {
  if (!Number.isSafeInteger(sceneDurationFrames)||sceneDurationFrames<1) throw new Error('Invalid scene duration');
  if (!Array.isArray(words)||words.length===0) throw new Error('At least one word required');
  let end=0;
  return words.map((word,i)=>{
    if (!word||typeof word.text!=='string'||!word.text.trim()) throw new Error('Invalid text');
    const start=word.startFrame, duration=word.durationFrames;
    if (!Number.isSafeInteger(start)||!Number.isSafeInteger(duration)||start<end||duration<1
        ||start+duration>sceneDurationFrames) throw new Error('Invalid or overlapping word frames');
    end=start+duration;
    return {index:i,text:word.text.trim(),startFrame:start,durationFrames:duration,endFrame:end};
  });
}
export function wordAtFrame(words,sceneDurationFrames,frame) {
  const ordered=validateWords(words,sceneDurationFrames);
  if (!Number.isSafeInteger(frame)) throw new Error('Frame must be integer');
  return ordered.find(w=>frame>=w.startFrame&&frame<w.endFrame)??null;
}
export function entranceProgress(word,frame,entranceFrames=5) {
  if (!Number.isSafeInteger(entranceFrames)||entranceFrames<1) throw new Error('Invalid entrance');
  return Math.max(0,Math.min(1,(frame-word.startFrame+1)/Math.min(entranceFrames,word.durationFrames)));
}
