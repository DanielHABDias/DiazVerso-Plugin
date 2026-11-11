import test from 'node:test';
import assert from 'node:assert/strict';
import {validateHQBackground,backgroundMotion,stableNoise} from '../references/motion/hq-background-math.mjs';
import {validateHQOverlay,overlayMotion,tagInk} from '../references/motion/hq-overlay-math.mjs';

test('HQ background validates supported modes and colors',()=>{
  assert.equal(validateHQBackground({mode:'grid',opacity:85}).mode,'grid');
  assert.throws(()=>validateHQBackground({mode:'comic_page'}));
  assert.throws(()=>validateHQBackground({opacity:120}));
  assert.throws(()=>validateHQBackground({baseColor:'transparent'}));
});
test('HQ grid, paper and film timing are deterministic',()=>{
  assert.equal(backgroundMotion(30,30,'grid').gridOffset,28);
  assert.equal(backgroundMotion(30,30,'paper').paperPose,6);
  assert.equal(backgroundMotion(30,30,'film').filmTick,12);
  assert.equal(stableNoise(8,11),stableNoise(8,11));
  assert.throws(()=>backgroundMotion(-1,30,'grid'));
});
test('HQ overlay respects widescreen compact and vertical scale',()=>{
  const props=validateHQOverlay({upperText:'A',lowerText:'Uma ideia',compactAt:1});
  const wide=overlayMotion(45,30,1920,1080,props);
  const vertical=overlayMotion(45,30,1080,1920,props);
  assert.equal(wide.isWide,true);
  assert.equal(vertical.isWide,false);
  assert.ok(wide.scale<1);
  assert.equal(vertical.scale,1);
  assert.ok(wide.tagReveal<=1&&wide.tagReveal>=0);
});
test('HQ overlay requires real text, legal color and bounded scale',()=>{
  assert.throws(()=>validateHQOverlay({upperText:'',lowerText:'x'}));
  assert.throws(()=>validateHQOverlay({upperText:'x',lowerText:'y',compactScale:0}));
  assert.throws(()=>validateHQOverlay({upperText:'x',lowerText:'y',tagColor:'red'}));
  assert.throws(()=>overlayMotion(0,0,1920,1080,{upperText:'x',lowerText:'y'}));
});
test('HQ tag foreground chooses legible black or white',()=>{
  assert.equal(tagInk('#FFFFFF'),'#090C12');
  assert.equal(tagInk('#111111'),'#FFFFFF');
});
