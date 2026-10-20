#!/usr/bin/env python3
"""Build original dialogue planning diagrams; no footage or audio synthesis."""
import json
import math
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/demos/dialogue-attention'
SHOTS = {
    'D0': [[0, 4, 'A'], [4, 8, 'B'], [8, 16, 'A'], [16, 18, 'B'], [18, 24, 'A']],
    'D1': [[0, 8, 'B'], [8, 16, 'W'], [16, 24, 'A']],
    'D2': [[0, 4, 'B'], [4, 8, 'B'], [8, 16, 'A'], [16, 18, 'B'], [18, 24, 'A']],
}
# D2 retains edit segments at 4s but continuous same-take B has no visible cut there.
CAMERAS = {'A': (2, -4), 'B': (-2, -4), 'W': (0, -6)}
ACTORS = {'A': (-2, 0), 'B': (2, 0)}
LABELS = {'A': 'C甲：观察请求者', 'B': 'C乙：观察评估者', 'W': 'W：观察两人关系'}
COLORS = {'A': '#155e75', 'B': '#9a3412', 'W': '#475569'}

def svg(body, height):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" role="img"><style>text{{font-family:system-ui,sans-serif;fill:#172033;font-size:18px}}.small{{font-size:14px}}</style><rect width="1000" height="{height}" fill="#f8fafc"/>{body}</svg>'

def layout():
    b = '<text x="35" y="38">对话空间：北在上，所有摄影机在甲—乙轴线南侧</text>'
    b += '<rect x="260" y="115" width="480" height="115" rx="20" fill="#e2e8f0"/>'
    b += '<path d="M100 160H900" stroke="#64748b" stroke-dasharray="8 6"/><text x="750" y="148" class="small">甲—乙轴线 / y=0</text>'
    points = {'A': (240, 160), 'B': (760, 160)}
    cams = {'A': (760, 390), 'B': (240, 390), 'W': (500, 510)}
    for k, (x, y) in cams.items():
        target = points.get(k, (500, 160))
        b += f'<path d="M{x} {y}L{target[0]} {target[1]}" stroke="{COLORS[k]}" stroke-width="2"/>'
        b += f'<rect x="{x-26}" y="{y-16}" width="52" height="32" rx="6" fill="{COLORS[k]}"/><text x="{x-100}" y="{y+45}">{LABELS[k]}</text>'
    for k, (x, y) in points.items():
        b += f'<circle cx="{x}" cy="{y}" r="28" fill="{COLORS[k]}"/><text x="{x-9}" y="{y+6}" style="fill:white">{"甲" if k=="A" else "乙"}</text>'
    b += '<text x="410" y="205" class="small">单据 → 中央；相机 乙 → 甲</text><text x="35" y="620">屏幕关系：双人镜甲左乙右；甲看画右，乙看画左。</text><text x="35" y="652" class="small">俯视位置图不表示焦距、视锥或取景下缘；手、单据及接物区仍须在分镜中另行保留。</text>'
    return svg(b, 680)

def timeline():
    b = '<text x="30" y="35">同一24秒事件底稿，不同观察对象</text>'
    for t in range(0, 25, 2):
        x = 125+t*34
        b += f'<path d="M{x} 55V280" stroke="#cbd5e1"/><text x="{x-6}" y="75" class="small">{t}s</text>'
    for i, (version, shots) in enumerate(SHOTS.items()):
        y = 100+i*62
        b += f'<text x="35" y="{y+25}">{version}</text>'
        for start, end, view in shots:
            x = 125+start*34
            b += f'<rect x="{x}" y="{y}" width="{(end-start)*34}" height="40" fill="{COLORS[view]}" stroke="white"/><text x="{x+8}" y="{y+26}" style="fill:white">{view}</text>'
    b += '<text x="30" y="320">A=C甲，B=C乙，W=双人；D2只替换D0的0—4秒。</text><text x="30" y="350" class="small">D2在4秒保留编辑段边界；同一连续B素材无画面切换。不能把编辑段数当可见切镜数。</text>'
    return svg(b, 380)

JS = r'''
const shots = __SHOTS__;
const labels = __LABELS__;
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
'''

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, content in [('layout.svg', layout()), ('timeline.svg', timeline())]:
        ElementTree.fromstring(content)
        (OUT/name).write_text(content)
    script = JS.replace('__SHOTS__', json.dumps(SHOTS)).replace('__LABELS__', json.dumps(LABELS, ensure_ascii=False))
    (OUT/'viewer.js').write_text(script)
    (OUT/'interactive.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>对话观察对象与空间图解</title>
<style>body{max-width:1000px;margin:30px auto;padding:0 20px;background:#f8fafc;color:#172033;font:18px/1.7 system-ui}img{width:100%}label,output{display:block}input{width:100%}select{font:inherit}section{padding:20px;background:white;border:1px solid #cbd5e1;border-radius:10px}#selected{font-size:24px;font-weight:700}</style>
<h1>谁说话，此刻看谁？</h1><p>原创24秒对话的交互式分镜索引。拖动时间、切换版本，对照公共事件与画面选择；本页无音频、表演视频或模拟微表情。</p>
<section><label>版本 <select id="version"><option>D0</option><option>D1</option><option>D2</option></select></label><label for="time">公共时间</label><input id="time" type="range" min="0" max="24" step="0.1" value="0"><output id="clock"></output><p id="selected"></p><p id="speech"></p><p id="state"></p><p id="compare"></p></section>
<h2>空间与视线</h2><img src="layout.svg" alt="甲在西、乙在东，三机位均在南侧；C甲在东南，C乙在西南，W在南侧中央。"><h2>剪辑时间线</h2><img src="timeline.svg" alt="D0按发言轮次，D1按判断过程，D2只替换D0的开头四秒。"><p>D0/D1同时改变观看对象、景别和镜头时长，不能只归因于切镜次数；D2缩小变量但不证明观众效果。24秒处显示最后镜头的结束状态，剪辑区间采用左闭右开。</p><noscript>交互需启用JavaScript；空间图和时间线仍可阅读。</noscript><script src="viewer.js"></script></html>''')
    def view_at(v, t):
        return next(s[2] for s in SHOTS[v] if s[0] <= t < s[1])
    for v, seq in SHOTS.items():
        assert seq[0][0] == 0 and seq[-1][1] == 24
        assert all(s < e for s, e, _ in seq)
        assert all(a[1] == b[0] for a, b in zip(seq, seq[1:]))
    times = [i/24 for i in range(576)]
    different = [t for t in times if view_at('D0', t) != view_at('D2', t)]
    assert different == times[:96]
    # Horizontal screen coordinate: dot(relative vector, camera right).
    # Camera right for a northward view has a positive eastward component.
    signs = {}
    for name, cam in CAMERAS.items():
        target = ACTORS.get(name, (0, 0))
        dx, dy = target[0]-cam[0], target[1]-cam[1]
        right = (dy/math.hypot(dx, dy), -dx/math.hypot(dx, dy))
        assert cam[1] < 0
        signs[name] = right[0]
        assert right[0] > 0
    report = {'duration_seconds': 24, 'sample_rate_for_timeline_checks': 24,
              'samples_checked': 576, 'd2_changed_samples': len(different),
              'd2_change_interval': '[0,4)', 'all_cameras_south_of_axis': True,
              'eastward_screen_projection': signs,
              'visible_view_changes': {v: sum(a[2] != b[2] for a,b in zip(seq,seq[1:])) for v,seq in SHOTS.items()},
              'svg_xml_valid': True, 'scope': 'Planning geometry and timeline only; no performance, audio, browser visual or audience validation.'}
    (OUT/'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
