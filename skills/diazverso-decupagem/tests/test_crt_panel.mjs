import test from 'node:test';
import assert from 'node:assert/strict';
import {planCrtPanel} from '../references/motion/crt-panel-math.mjs';

const valid=()=>({src:'assets/excerpt-approved.mp4',rightsStatus:'APPROVED',
  evidence:'Registro de autorização e finalidade editorial conferidos',
  startFrame:30,durationFrames:90,availableFrames:300,
  outputWidth:1920,outputHeight:1080,audioAllowed:false,audioVolume:0,
  scanlineOpacity:0.28});
test('approved silent CRT plan fits long frame',()=>{
  const r=planCrtPanel(valid());
  assert.ok(r.panel.width>0&&r.panel.height>0);
  assert.ok(r.panel.left>=0&&r.panel.top>=0);
  assert.equal(r.audioVolume,0);
  assert.equal(r.runtimeVerified,false);
  assert.equal(r.rightsVerifiedByCode,false);
});
test('Short frame has safely sized panel',()=>{
  const d=valid();d.outputWidth=1080;d.outputHeight=1920;
  const r=planCrtPanel(d);
  assert.ok(r.panel.top+r.panel.height<d.outputHeight);
  assert.ok(r.panel.left+r.panel.width<=d.outputWidth);
});
test('missing documented rights review rejected',()=>{
  const d=valid();d.rightsStatus='PENDING';
  assert.throws(()=>planCrtPanel(d));
  d.rightsStatus='APPROVED';d.evidence='  ';
  assert.throws(()=>planCrtPanel(d));
});
test('unauthorized clip sound is rejected',()=>{
  const d=valid();d.audioVolume=0.5;
  assert.throws(()=>planCrtPanel(d));
});
test('authorized clip sound is bounded and accepted',()=>{
  const d=valid();d.audioAllowed=true;d.audioVolume=0.3;
  assert.equal(planCrtPanel(d).audioVolume,0.3);
  d.audioVolume=1.1;assert.throws(()=>planCrtPanel(d));
});
test('duration must not extend beyond verified media',()=>{
  const d=valid();d.startFrame=250;d.durationFrames=90;
  assert.throws(()=>planCrtPanel(d));
});
test('remote and path-traversal media rejected',()=>{
  for(const src of ['https://example.com/x.mp4','../../secret.mp4',
    '/private/x.mp4','assets//clip.mp4','assets\\..\\clip.mp4']){
    const d=valid();d.src=src;
    assert.throws(()=>planCrtPanel(d));
  }
});
test('scanline strength is visible but bounded',()=>{
  const d=valid();d.scanlineOpacity=0;
  assert.throws(()=>planCrtPanel(d));
  d.scanlineOpacity=0.9;assert.throws(()=>planCrtPanel(d));
  d.scanlineOpacity=0.28;assert.ok(planCrtPanel(d));
});
test('invalid input dimensions rejected',()=>{
  const d=valid();d.outputHeight=-3;
  assert.throws(()=>planCrtPanel(d));
});
