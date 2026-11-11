/** Original Diazverso procedural HQ background math (G06).
 * Historical reference: BackgroundHQ.tsx; no binary assets or Content Lab imports.
 */
const styles = new Set(['solid','halftone','grid','stars','film','paper']);
export function validateHQBackground(options = {}) {
  const {mode='halftone',baseColor='#162034',opacity=100,
    gridColor='#4A607A',paperTone='dark'}=options;
  if (!styles.has(mode)) throw new Error('Unsupported background mode');
  if (![baseColor,gridColor].every(x=>typeof x==='string'&&/^#[0-9a-fA-F]{6}$/.test(x))) {
    throw new Error('Color must be #RRGGBB');
  }
  if (!Number.isFinite(opacity)||opacity<0||opacity>100) throw new Error('Opacity must be 0..100');
  if (paperTone!=='light'&&paperTone!=='dark') throw new Error('Paper tone invalid');
  return {mode,baseColor,opacity,gridColor,paperTone};
}
export function backgroundMotion(frame,fps,mode) {
  if (!Number.isInteger(frame)||frame<0||!Number.isFinite(fps)||fps<=0||!styles.has(mode)) {
    throw new Error('Invalid background timing');
  }
  const seconds=frame/fps;
  return {
    gridOffset: ((seconds*28)%84+84)%84,
    paperPose:Math.floor(seconds*6)%8,
    filmTick:Math.floor(seconds*12),
    starPhase:(seconds*.025)%1
  };
}
export function stableNoise(index,seed=0) {
  if (!Number.isInteger(index)||!Number.isInteger(seed)) throw new Error('Noise seed must be integer');
  const value=Math.sin((index+seed)*127.1+311.7)*43758.5453;
  return value-Math.floor(value);
}
