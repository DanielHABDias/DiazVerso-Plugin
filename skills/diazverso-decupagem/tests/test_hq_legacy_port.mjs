import test from 'node:test';
import assert from 'node:assert/strict';
import {clampHQ,progressHQ,edgeTravelHQ} from '../references/motion/hq-legacy-port.mjs';

test('HQ progress reaches the final visible frame without overshooting',()=>{
  assert.equal(progressHQ(0,0,2,30),0);
  assert.equal(progressHQ(59/30,0,2,30),1);
  assert.equal(progressHQ(20/30,0,2,30)>0,true);
  assert.equal(progressHQ(-1,0,2,30),0);
  assert.equal(clampHQ(2),1);
});
test('HQ edge travel respects left/right and zero direction',()=>{
  assert.equal(edgeTravelHQ(20,100,1920,-1),150);
  assert.equal(edgeTravelHQ(20,100,1920,1),1930);
  assert.equal(edgeTravelHQ(20,100,1920,0),0);
});
test('HQ port rejects invalid timing and geometry',()=>{
  assert.throws(()=>progressHQ(0,0,0,30));
  assert.throws(()=>edgeTravelHQ(0,100,1080,2));
});
