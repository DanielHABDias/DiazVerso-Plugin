/** Diazverso camera/parallax: portable image cover & camera/parallax geometry.
 * Pure ESM; can be unit-tested without React/Remotion or assets.
 * Coordinates refer to output frame pixels; never distort image aspect ratio.
 */
export const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

export function coverGeometry(imageW, imageH, frameW, frameH, extraScale = 1) {
  for (const x of [imageW,imageH,frameW,frameH,extraScale]) {
    if (!Number.isFinite(x) || x <= 0) throw new Error('positive finite dimensions required');
  }
  const cover = Math.max(frameW/imageW, frameH/imageH);
  const scale = cover * extraScale;
  const width = imageW * scale, height = imageH * scale;
  return {width, height, x:(frameW-width)/2, y:(frameH-height)/2, scale};
}

/** A pan requests displacement of image center measured in output pixels.
 * Clamp to existing crop; guarantees image covers the whole canvas.
 */
export function cropAndPan(imageW, imageH, frameW, frameH, progress, opts = {}) {
  if (!Number.isFinite(progress)) throw new Error('invalid progress');
  const t=clamp(progress,0,1);
  const zoomFrom=opts.zoomFrom ?? 1.04, zoomTo=opts.zoomTo ?? 1.12;
  const panFrom=opts.panFrom ?? [0,0], panTo=opts.panTo ?? [0,0];
  if (![zoomFrom,zoomTo].every(x=>Number.isFinite(x)&&x>=1)) throw new Error('zoom must be >=1');
  if (![panFrom,panTo].every(p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite))) throw new Error('pan invalid');
  const z=zoomFrom+(zoomTo-zoomFrom)*t;
  const geom=coverGeometry(imageW,imageH,frameW,frameH,z);
  const slackX=(geom.width-frameW)/2, slackY=(geom.height-frameH)/2;
  const reqX=panFrom[0]+(panTo[0]-panFrom[0])*t;
  const reqY=panFrom[1]+(panTo[1]-panFrom[1])*t;
  const dx=clamp(reqX,-slackX,slackX), dy=clamp(reqY,-slackY,slackY);
  return {...geom,x:geom.x+dx,y:geom.y+dy,zoom:z,
    panClamped:Math.abs(reqX-dx)>1e-6||Math.abs(reqY-dy)>1e-6};
}

/** Parallax layers all cover the canvas (layer depth affects movement).
 * depth=0 background; depth=1 foreground. Positive overscan affords movement.
 */
export function parallaxGeometry(imageW,imageH,frameW,frameH,progress,depth=0.5) {
  if (!Number.isFinite(depth)||depth<0||depth>1) throw new Error('depth must be 0..1');
  const maxMovement=0.07*Math.min(frameW,frameH)*(0.25+0.75*depth);
  return cropAndPan(imageW,imageH,frameW,frameH,progress,{
    zoomFrom:1.08+0.04*depth,zoomTo:1.10+0.04*depth,
    panFrom:[-maxMovement,0],panTo:[maxMovement,0]
  });
}
