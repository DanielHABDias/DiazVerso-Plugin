import test from 'node:test';
import assert from 'node:assert/strict';
import {coverGeometry,cropAndPan,parallaxGeometry} from '../references/motion/motion-math.mjs';

function covered(g,w,h) {
  assert.ok(g.x<=1e-6, 'left edge blank');
  assert.ok(g.y<=1e-6, 'top edge blank');
  assert.ok(g.x+g.width>=w-1e-6, 'right edge blank');
  assert.ok(g.y+g.height>=h-1e-6, 'bottom edge blank');
}
test('cover preserves aspect ratio for both formats',()=>{
  for(const [iw,ih,w,h] of [[1200,800,1920,1080],[800,1200,1080,1920],[1408,768,1080,1920]]){
    const g=coverGeometry(iw,ih,w,h);
    covered(g,w,h);
    assert.ok(Math.abs(g.width/g.height-iw/ih)<1e-8);
  }
});
test('camera never exposes gaps for extreme pan requests',()=>{
  for(const [iw,ih,w,h] of [[1920,1080,1920,1080],[600,800,1080,1920],[4000,1200,1080,1920]]){
    for(let i=0;i<=20;i++){
      const g=cropAndPan(iw,ih,w,h,i/20,{zoomFrom:1,zoomTo:1.3,panFrom:[-5000,-5000],panTo:[5000,5000]});
      covered(g,w,h);
    }
  }
});
test('clamped progress and finite output',()=>{
  for(const p of [-1,0,0.5,1,2]){
    const g=cropAndPan(1408,768,1080,1920,p);
    covered(g,1080,1920);
    assert.ok([g.x,g.y,g.width,g.height].every(Number.isFinite));
  }
});
test('zero or invalid dimensions rejected',()=>{
  for(const dims of [[0,100,100,100],[100,0,100,100],[100,100,-1,100]]){
    assert.throws(()=>coverGeometry(...dims));
  }
  assert.throws(()=>cropAndPan(100,100,1080,1920,NaN));
});
test('parallax different depths move differently and preserve cover',()=>{
  for(let d of [0,0.4,1]){
    const a=parallaxGeometry(1408,768,1080,1920,0,d);
    const b=parallaxGeometry(1408,768,1080,1920,1,d);
    covered(a,1080,1920);covered(b,1080,1920);
    assert.notEqual(a.x,b.x);
  }
});
test('invalid depth and zoom rejected',()=>{
  assert.throws(()=>parallaxGeometry(1000,900,1080,1920,0.5,1.5));
  assert.throws(()=>cropAndPan(1000,900,1080,1920,0.5,{zoomFrom:0.8}));
});
