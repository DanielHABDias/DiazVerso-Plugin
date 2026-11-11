import test from 'node:test';
import assert from 'node:assert/strict';
import {contrastRatio,verifyPalette,validateWords,wordAtFrame,entranceProgress} from '../references/motion/kinetic-text-math.mjs';

const words=[{text:'Por',startFrame:0,durationFrames:12},
             {text:'quê?',startFrame:12,durationFrames:18}];
test('black-white gives 21:1 contrast',()=>{
  assert.ok(Math.abs(contrastRatio('#000000','#FFFFFF')-21)<1e-8);
  assert.equal(verifyPalette('#FFFFFF','#000000').passes,true);
});
test('weak contrast is blocked',()=>{
  const r=verifyPalette('#888888','#999999');
  assert.equal(r.passes,false);
  assert.equal(r.minimum,4.5);
});
test('contrast input must be RGB hex',()=>{
  assert.throws(()=>contrastRatio('white','#000000'));
  assert.throws(()=>contrastRatio('#FFF','#000000'));
});
test('word windows are exclusive and deterministic',()=>{
  assert.equal(wordAtFrame(words,60,0).text,'Por');
  assert.equal(wordAtFrame(words,60,11).text,'Por');
  assert.equal(wordAtFrame(words,60,12).text,'quê?');
  assert.equal(wordAtFrame(words,60,30),null);
});
test('invalid and overlapping word timing is rejected',()=>{
  assert.throws(()=>validateWords([{text:'a',startFrame:0,durationFrames:12},
                                   {text:'b',startFrame:11,durationFrames:10}],60));
  assert.throws(()=>validateWords([{text:'a',startFrame:0,durationFrames:61}],60));
  assert.throws(()=>validateWords([{text:'a',startFrame:0,durationFrames:0}],60));
});
test('frames must be integers; missing text is rejected',()=>{
  assert.throws(()=>wordAtFrame(words,60,2.5));
  assert.throws(()=>validateWords([{text:'  ',startFrame:0,durationFrames:10}],60));
});
test('entrance animation bounded to one',()=>{
  const w=validateWords(words,60)[0];
  assert.ok(entranceProgress(w,0)<1);
  assert.equal(entranceProgress(w,10),1);
  assert.throws(()=>entranceProgress(w,0,0));
});
