// Fixed SVG viewBox coordinates make overlap calculations reproducible.
const texts=['把蓝色方块移到右侧框内。','边框变绿后，表示已经到位。'];
const variants={
  P0:{box:{x:100,y:170,w:440,h:88},cues:[[0,8,[0,1]]]},
  P1:{box:{x:100,y:25,w:440,h:88},cues:[[0,8,[0,1]]]},
  P2:{box:{x:100,y:25,w:440,h:88},cues:[[0,4,[0]],[4,8,[1]]]},
  P3:{box:{x:100,y:25,w:440,h:88},cues:[[0,4,[0]],[6,10,[1]]]}
};
const target={x:445,y:170,w:70,h:70};
function activeCue(v,t){return variants[v].cues.find(c=>t>=c[0]&&t<c[1])||null;}
function overlap(a,b){return Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y));}
function boxAt(t){return {x:170+300*Math.max(0,Math.min(1,(t-4)/2)),y:205};}
function render(){
 const t=Number(document.querySelector('#time').value),v=document.querySelector('#variant').value;
 const cue=activeCue(v,t),cfg=variants[v],pos=boxAt(t);
 document.querySelector('#clock').textContent=t.toFixed(1)+' / 12.0 秒';
 document.querySelector('#block').setAttribute('x',pos.x-20);
 document.querySelector('#target').setAttribute('stroke',t>=6?'#15803d':'#475569');
 const group=document.querySelector('#caption'); group.setAttribute('visibility',cue?'visible':'hidden');
 const bg=document.querySelector('#caption-bg');for(const [key,val] of Object.entries(cfg.box))bg.setAttribute({w:'width',h:'height'}[key]||key,val);
 for(let i=0;i<2;i++){
   const e=document.querySelector('#line'+i);e.setAttribute('x',cfg.box.x+20);e.setAttribute('y',cfg.box.y+32+i*32);e.textContent=cue&&cue[2][i]!==undefined?texts[cue[2][i]]:'';
 }
 document.querySelector('#status').textContent='动作阶段：'+(t<4?'预备':t<6?'移动':'到位')+'；字幕框与目标框相交面积：'+(cue?overlap(cfg.box,target):0)+' SVG平方单位。';
}
if(typeof document!=='undefined'){
 document.querySelector('#time').addEventListener('input',render);
 document.querySelector('#variant').addEventListener('change',render);render();
}
if(typeof module!=='undefined')module.exports={texts,variants,target,activeCue,overlap,boxAt};
