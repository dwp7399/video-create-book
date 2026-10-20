// Check the exact timeline/state functions used by the standalone page.
const assert = require('node:assert/strict');
const {shots,viewAt,stateAt} = require('../docs/demos/dialogue-attention/viewer.js');
for (const [v,seq] of Object.entries(shots)) for (const [a,b,k] of seq) {
  assert.equal(viewAt(v,a),k);
  assert.equal(viewAt(v,b-0.001),k);
}
for (const v of Object.keys(shots)) assert.equal(viewAt(v,24),'A');
assert.equal(stateAt(12).paper,'甲将单据放向桌中央');
assert.equal(stateAt(14).paper,'单据留桌中央，乙不拿');
assert.equal(stateAt(22).camera,'相机在甲侧桌面');
for(let i=0;i<576;i++) {
  assert.equal(viewAt('D0',i/24) !== viewAt('D2',i/24), i < 96);
}
console.log('Dialogue viewer: segment boundaries, endpoint, object states and D2 isolation passed.');
