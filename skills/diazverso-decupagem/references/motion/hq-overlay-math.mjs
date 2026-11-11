/** hq-components part 2: pure geometry/contrast for an optional HQ text overlay.
 * Inspired by the editorial behavior of QuadroHQSobreCena, not copied from it.
 */
const clamp=(v)=>Math.max(0,Math.min(1,v));
export function validateHQOverlay(input={}) {
  const {upperText,lowerText,tagColor='#5CA5AD',compactAt=2,
    compactDuration=.65,compactScale=.58}=input;
  if(typeof upperText!=='string'||!upperText.trim()||
     typeof lowerText!=='string'||!lowerText.trim()) throw new Error('Overlay text required');
  if(upperText.length>100||lowerText.length>180) throw new Error('Overlay text too long');
  if(typeof tagColor!=='string'||!/^#[0-9a-fA-F]{6}$/.test(tagColor)) throw new Error('Tag color invalid');
  if(![compactAt,compactDuration,compactScale].every(Number.isFinite)||
     compactAt<0||compactDuration<=0||compactScale<.2||compactScale>1) {
    throw new Error('Invalid compact timing/scale');
  }
  return {upperText,lowerText,tagColor,compactAt,compactDuration,compactScale};
}
export function overlayMotion(frame,fps,width,height,params={}) {
  if(!Number.isInteger(frame)||frame<0||!Number.isFinite(fps)||fps<=0||
     !Number.isFinite(width)||!Number.isFinite(height)||width<=0||height<=0) {
    throw new Error('Invalid overlay frame/geometry');
  }
  const {compactAt,compactDuration,compactScale}=validateHQOverlay(params);
  const time=frame/fps;
  const smooth=(x)=>{const t=clamp(x);return t*t*(3-2*t);};
  const compact=width>height?smooth((time-compactAt)/compactDuration):0;
  return {
    reveal:smooth(time/.24),
    tagReveal:smooth((time-.2)/.3),
    titleReveal:smooth((time-.08)/.4),
    scale:1-(1-compactScale)*compact,
    unit:Math.min(width,height)/1080,
    isWide:width>height
  };
}
export function tagInk(color) {
  if(typeof color!=='string'||!/^#[0-9a-fA-F]{6}$/.test(color))throw new Error('Color invalid');
  const [r,g,b]=[1,3,5].map(i=>parseInt(color.slice(i,i+2),16));
  return (r*299+g*587+b*114)/1000>=135?'#090C12':'#FFFFFF';
}
