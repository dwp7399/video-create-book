
const shots = {"D0": [[0, 4, "A"], [4, 8, "B"], [8, 16, "A"], [16, 18, "B"], [18, 24, "A"]], "D1": [[0, 8, "B"], [8, 16, "W"], [16, 24, "A"]], "D2": [[0, 4, "B"], [4, 8, "B"], [8, 16, "A"], [16, 18, "B"], [18, 24, "A"]]};
const labels = {"A": "C甲：观察请求者", "B": "C乙：观察评估者", "W": "W：观察两人关系"};
function viewAt(version, t) {
  const a = shots[version];
  return a.find(s => t >= s[0] && t < s[1])?.[2] || a[a.length-1][2];
}
function stateAt(t) {
  const paper = t < 8 ? '甲右手持单据' : t < 12 ? '甲举单据' : t < 14 ? '甲将单据放向桌中央' : '单据留桌中央，乙不拿';
  const camera = t < 20 ? '相机在乙面前，背带平放' : t < 22 ? '乙沿桌推向甲，甲接住后乙松手' : '相机在甲侧桌面';
  const speech = t < 3 ? '甲：明天能借我相机吗？' : t < 4 ? '气口' : t < 6 ? '乙：上次的镜头呢？' : t < 8 ? '停顿' : t < 11 ? '甲：修好了，单据在这里。' : t < 12 ? '停顿' : t < 14 ? '单据摩擦声' : t < 16 ? '乙看单据后回看甲；无对白' : t < 18 ? '乙：这次别再弄坏。' : t < 20 ? '甲：我会小心。' : t < 22 ? '相机滑动声' : '只留环境声';
  return {paper, camera, speech};
}
if (typeof document !== 'undefined') {
  const slider = document.querySelector('#time');
  const version = document.querySelector('#version');
  function render() {
    const t = Number(slider.value), v = version.value, state = stateAt(t);
    document.querySelector('#clock').textContent = t.toFixed(1) + ' / 24.0 秒';
    document.querySelector('#selected').textContent = labels[viewAt(v,t)];
    document.querySelector('#state').textContent = state.paper + '；' + state.camera;
    document.querySelector('#speech').textContent = state.speech;
    document.querySelector('#compare').textContent = Object.keys(shots).map(k => k + '：' + labels[viewAt(k,t)]).join(' ｜ ');
  }
  slider.addEventListener('input', render); version.addEventListener('change', render);
  render();
}
if (typeof module !== 'undefined') module.exports = {shots, viewAt, stateAt};
