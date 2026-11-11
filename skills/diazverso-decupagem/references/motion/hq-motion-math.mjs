/** Deterministic HQ motion primitives: frame progress and edge geometry. */
export const clampHQ = (v) => Math.max(0,Math.min(1,v));

export function progressHQ(time,start,duration,fps) {
  if (![time,start,duration,fps].every(Number.isFinite) || duration<=0 || fps<=0) {
    throw new Error('Invalid HQMotion time/duration/fps');
  }
  if (time >= start + duration - 1/fps - 1e-8) return 1;
  return clampHQ((time - start)/Math.max(1/fps,duration-1/fps));
}

export function edgeTravelHQ(position,size,viewport,direction,margin=30) {
  if (![position,size,viewport,direction,margin].every(Number.isFinite) ||
      size<0 || viewport<=0 || margin<0 || ![-1,0,1].includes(direction)) {
    throw new Error('Invalid HQMotion edge geometry');
  }
  return direction<0?position+size+margin:direction>0?viewport-position+margin:0;
}
