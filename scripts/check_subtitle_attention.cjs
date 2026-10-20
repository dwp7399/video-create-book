const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {texts,variants,target,activeCue,overlap,boxAt}=require('../docs/demos/subtitle-attention/viewer.js');
const report={duration_seconds:12,canvas:[640,360],versions:{},scope:'Geometry and cue scheduling only; not rendered font bounds, audience reading speed or accessibility certification.'};
for(const [v,cfg] of Object.entries(variants)){
 const indices=cfg.cues.flatMap(c=>c[2]);assert.deepEqual(indices,[0,1]);
 for(const [start,end] of cfg.cues){assert(start>=0&&end<=12&&start<end);assert(activeCue(v,start));assert.equal(activeCue(v,end)?.[0]===start,false);}
 const {x,y,w,h}=cfg.box;assert(x>=0&&y>=0&&x+w<=640&&y+h<=360);
 const actionSamples=Array.from({length:48},(_,i)=>4+i/24);
 report.versions[v]={target_overlap_area:overlap(cfg.box,target),text_present_during_action_seconds:actionSamples.filter(t=>activeCue(v,t)).length/24,
 cues:cfg.cues.map(([start,end,ids])=>({start,end,characters_including_punctuation:ids.reduce((n,i)=>n+[...texts[i]].length,0),nominal_characters_per_second:ids.reduce((n,i)=>n+[...texts[i]].length,0)/(end-start)}))};
}
assert.equal(report.versions.P0.target_overlap_area,4900);
for(const v of ['P1','P2','P3'])assert.equal(report.versions[v].target_overlap_area,0);
assert.equal(report.versions.P2.text_present_during_action_seconds,2);
assert.equal(report.versions.P3.text_present_during_action_seconds,0);
assert.deepEqual(boxAt(4),{x:170,y:205});assert.deepEqual(boxAt(6),{x:470,y:205});
// Explicitly verify the adjacent comparisons isolate the intended data change.
assert.deepEqual(variants.P0.cues,variants.P1.cues);
assert.deepEqual(variants.P1.box,variants.P2.box);
assert.deepEqual(variants.P2.box,variants.P3.box);
assert.deepEqual(variants.P2.cues[0],variants.P3.cues[0]);
assert.equal(variants.P2.cues[1][1]-variants.P2.cues[1][0],variants.P3.cues[1][1]-variants.P3.cues[1][0]);
fs.writeFileSync(path.join(__dirname,'../docs/demos/subtitle-attention/verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
