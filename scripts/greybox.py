#!/usr/bin/env python3
"""程序渲染灰盒三维视频：用长方体搭场景、人物和道具，按设定机位渲染灰盒画面与深度图。

本机没有 Blender，这里用纯 Python 的 z-buffer 光栅化代替“白模动画→渲染”：
几何与运动由代码精确决定（例如周始终在门外、两只手停在伞柄前不接触），
渲染结果作为 wan3.0 的参考视频，让模型负责外观。只依赖标准库与 FFmpeg。

用法：python3 scripts/greybox.py Y|Z  → docs/assets/ai/greybox/<shot>-grey.mp4、<shot>-depth.mp4 与中间帧PNG
"""
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "ai" / "greybox"
W, H, FPS, SECONDS = 427, 240, 24, 5  # SECONDS 为默认时长，main() 可传入
LIGHT = (-0.4, -0.5, 0.75)


def norm(v):
    n = math.sqrt(sum(c * c for c in v)) or 1
    return tuple(c / n for c in v)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def box(lo, hi, color):
    """轴对齐长方体 → 12个三角形（顶点坐标、法线、颜色）。x东 y北 z上，单位米。"""
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    faces = [((0, 1, 2, 3), (0, 0, -1)), ((4, 5, 6, 7), (0, 0, 1)), ((0, 1, 5, 4), (0, -1, 0)),
             ((2, 3, 7, 6), (0, 1, 0)), ((1, 2, 6, 5), (1, 0, 0)), ((0, 3, 7, 4), (-1, 0, 0))]
    tris = []
    for (a, b, c, d), n in faces:
        tris.append(((v[a], v[b], v[c]), n, color))
        tris.append(((v[a], v[c], v[d]), n, color))
    return tris


def person(x, y, body_rgb, facing_h=0.0, height=1.75):
    """人物：躯干＋头部两个长方体（灰盒里只需要位置、尺度与朝向）。"""
    t = box((x - 0.22, y - 0.14, 0), (x + 0.22, y + 0.14, height - 0.28), body_rgb)
    t += box((x - 0.11, y - 0.11, height - 0.27), (x + 0.11, y + 0.11, height), tuple(min(255, c + 25) for c in body_rgb))
    return t


class Camera:
    def __init__(self, pos, target, fov_deg):
        self.p = pos
        self.f = norm(sub(target, pos))
        self.r = norm(cross(self.f, (0, 0, 1)))
        self.u = cross(self.r, self.f)
        self.k = (W / 2) / math.tan(math.radians(fov_deg) / 2)

    def project(self, q):
        d = sub(q, self.p)
        z = dot(d, self.f)
        if z <= 0.05:
            return None
        return (W / 2 + self.k * dot(d, self.r) / z, H / 2 - self.k * dot(d, self.u) / z, z)


def render(tris, cam, near_far):
    """z-buffer 光栅化：返回灰盒 RGB 字节与深度灰度字节（近亮远暗）。"""
    zb = [1e9] * (W * H)
    rgb = bytearray(b"\x2a" * (W * H * 3))
    L = norm(LIGHT)
    for (a, b, c), n, col in tris:
        pa, pb, pc = cam.project(a), cam.project(b), cam.project(c)
        if not (pa and pb and pc):
            continue
        shade = 0.45 + 0.55 * max(0.0, dot(n, L))
        if dot(n, sub(cam.p, a)) < 0:  # 背面剔除
            continue
        cr = tuple(int(min(255, ch * shade)) for ch in col)
        xs, ys = (pa[0], pb[0], pc[0]), (pa[1], pb[1], pc[1])
        x0, x1 = max(0, int(min(xs))), min(W - 1, int(max(xs)) + 1)
        y0, y1 = max(0, int(min(ys))), min(H - 1, int(max(ys)) + 1)
        den = (pb[1] - pc[1]) * (pa[0] - pc[0]) + (pc[0] - pb[0]) * (pa[1] - pc[1])
        if abs(den) < 1e-9:
            continue
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                w1 = ((pb[1] - pc[1]) * (x - pc[0]) + (pc[0] - pb[0]) * (y - pc[1])) / den
                w2 = ((pc[1] - pa[1]) * (x - pc[0]) + (pa[0] - pc[0]) * (y - pc[1])) / den
                w3 = 1 - w1 - w2
                if w1 < 0 or w2 < 0 or w3 < 0:
                    continue
                z = w1 * pa[2] + w2 * pb[2] + w3 * pc[2]
                i = y * W + x
                if z < zb[i]:
                    zb[i] = z
                    rgb[i * 3:i * 3 + 3] = bytes(cr)
    near, far = near_far
    depth = bytearray(int(255 * (1 - (min(max(z, near), far) - near) / (far - near))) if z < 1e8 else 0 for z in zb)
    return bytes(rgb), bytes(depth)


GREY, DARK, FLOOR, WALL = (175, 175, 175), (95, 95, 100), (130, 128, 125), (190, 188, 184)
YELLOW, SKY = (225, 190, 40), (40, 55, 80)


def store_static():
    """便利店：地面、门所在的东墙（留门洞）、门框、门外屋檐和街面、门内伞架与黄伞。"""
    t = box((-1, -3, -0.05), (6, 3, 0), FLOOR)                    # 店内地面
    t += box((4.0, -3, 0), (4.1, -0.7, 2.6), WALL)                 # 东墙南段
    t += box((4.0, 0.7, 0), (4.1, 3, 2.6), WALL)                   # 东墙北段
    t += box((4.0, -0.7, 2.2), (4.1, 0.7, 2.6), WALL)              # 门洞上方
    t += box((3.98, -0.72, 0), (4.12, -0.62, 2.2), DARK)           # 门框
    t += box((3.98, 0.62, 0), (4.12, 0.72, 2.2), DARK)
    t += box((4.1, -2, 2.4), (6.0, 2, 2.5), DARK)                  # 门外屋檐
    t += box((4.1, -6, -0.06), (14, 6, -0.01), (70, 75, 85))       # 门外地面
    t += box((14, -8, 0), (14.2, 8, 5), SKY)                       # 远处街景（暗面）
    t += box((3.4, -1.2, 0), (3.8, -0.8, 0.55), DARK)              # 伞架
    t += box((3.57, -1.03, 0.05), (3.63, -0.97, 0.95), YELLOW)     # 唯一一把黄伞（闭合）
    t += box((3.55, -1.06, 0.95), (3.65, -0.94, 1.02), (30, 30, 30))  # 黑色弯柄（简化）
    return t


def shot_Y(t):
    """周在门外等候：机位在店内西侧正对门；周站在门外1米，只做小幅重心摆动，永远不过门线 x=4.1。"""
    sway = 0.04 * math.sin(2 * math.pi * t / 2.5)
    tris = [tr for tr in store_static() if tr[2] not in (YELLOW, (30, 30, 30))]  # 门口灰盒不放伞架与伞：伞的位置交给参考图，避免两者矛盾
    tris = [tr for tr in tris if not (tr[2] == DARK and max(v[2] for v in tr[0]) <= 0.56)]
    tris += person(5.1 + sway * 0.3, sway, (120, 120, 125))
    cam = Camera((0.2, 0.0, 1.5), (5.0, 0.0, 1.3), 52)
    return tris, cam, (1.0, 10.0)


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def shot_Z(t):
    """手部近景：陈的右手（深蓝袖）从左侧伸向伞柄，林的左手（浅色袖）从上方挡住；
    两只手都停在伞柄左侧，彼此相隔约8厘米，也不碰伞。"""
    tris = box((3.2, -1.6, -0.02), (4.4, -0.4, 0), FLOOR)
    tris += box((3.4, -1.2, 0), (3.8, -0.8, 0.55), DARK)
    tris += box((3.57, -1.03, 0.05), (3.63, -0.97, 0.95), YELLOW)
    tris += box((3.55, -1.06, 0.95), (3.65, -0.94, 1.02), (30, 30, 30))
    tris += box((4.0, -1.8, 0), (4.1, 0, 2.2), WALL)
    # 陈：0—2.5秒沿x方向从左侧伸来，停在伞杆左侧约7厘米（伞杆x=3.57—3.63）
    u = ease(t / 2.5)
    cx, cy, cz = 3.10 + 0.34 * u, -1.0, 0.80
    tris += box((cx - 0.35, cy - 0.05, cz - 0.05), (cx - 0.08, cy + 0.05, cz + 0.05), (60, 70, 110))   # 前臂（深蓝袖）
    tris += box((cx - 0.08, cy - 0.045, cz - 0.03), (cx + 0.06, cy + 0.045, cz + 0.03), (215, 175, 150))  # 手
    # 林：1.0—3.0秒从上方落下，停在陈的手上方约8厘米、伞柄左侧
    v = ease((t - 1.0) / 2.0)
    lx, ly, lz = 3.46, -1.0, 1.32 - 0.30 * v
    tris += box((lx - 0.04, ly - 0.05, lz + 0.06), (lx + 0.04, ly + 0.05, lz + 0.40), (225, 222, 215))  # 前臂（浅色袖）
    tris += box((lx - 0.045, ly - 0.06, lz - 0.06), (lx + 0.045, ly + 0.06, lz + 0.06), (215, 175, 150))  # 手
    # 机位在南侧，视线朝北，手的运动方向与视线垂直，空隙在画面里可见
    cam = Camera((3.45, -2.25, 0.95), (3.48, -1.0, 0.88), 42)
    return tris, cam, (0.3, 2.5)


def store_wide():
    """全景用的店内布局：柜台东西向，林在北（画面左后），陈在南，伞架在柜台东端，东墙门洞外是屋檐与街面。"""
    t = box((-2, -3, -0.05), (4.0, 3, 0), FLOOR)
    t += box((0.3, 0.3, 0), (2.6, 0.9, 1.0), (205, 200, 190))      # 柜台
    t += box((-2, 2.2, 0), (4.0, 2.3, 2.8), WALL)                   # 北墙
    t += box((4.0, -3, 0), (4.1, -0.6, 2.8), WALL)                  # 东墙南段
    t += box((4.0, 0.6, 0), (4.1, 2.3, 2.8), WALL)                  # 东墙北段
    t += box((4.0, -0.6, 2.2), (4.1, 0.6, 2.8), WALL)
    t += box((3.98, -0.62, 0), (4.12, -0.52, 2.2), DARK)            # 门框
    t += box((3.98, 0.52, 0), (4.12, 0.62, 2.2), DARK)
    t += box((4.1, -2, 2.4), (6.0, 2, 2.5), DARK)                   # 屋檐
    t += box((4.1, -6, -0.06), (14, 6, -0.01), (70, 75, 85))        # 门外地面
    t += box((14, -8, 0), (14.2, 8, 5), SKY)
    t += box((3.0, 0.0, 0), (3.4, 0.4, 0.55), DARK)                 # 伞架
    t += box((3.17, 0.17, 0.05), (3.23, 0.23, 0.95), YELLOW)        # 唯一一把黄伞
    t += box((3.15, 0.14, 0.95), (3.25, 0.26, 1.02), (30, 30, 30))
    return t


def shot_wide(t, dur, zhou=True):
    """全景：林在柜台后、陈在柜台前，两人位置固定；周（若在场）始终在门外 x>4.6。"""
    tris = store_wide() + person(1.0, 1.4, (60, 110, 80)) + person(1.5, -0.3, (55, 65, 105))
    if zhou:
        sway = 0.04 * math.sin(2 * math.pi * t / 2.5)
        tris += person(5.0, 0.0 + sway, (120, 120, 125))
    cam = Camera((-2.6, -4.2, 1.6), (2.4, 0.4, 1.0), 58)
    return tris, cam, (1.5, 9.0)


def rack_closeup():
    t = box((3.2, -1.6, -0.02), (4.4, -0.4, 0), FLOOR)
    t += box((3.4, -1.2, 0), (3.8, -0.8, 0.55), DARK)
    t += box((3.57, -1.03, 0.05), (3.63, -0.97, 0.95), YELLOW)
    t += box((3.55, -1.06, 0.95), (3.65, -0.94, 1.02), (30, 30, 30))
    t += box((4.0, -1.8, 0), (4.1, 0, 2.2), WALL)
    return t


RACK_CAM = ((3.45, -2.25, 0.95), (3.48, -1.0, 0.88), 42)


def arm(x, y, z, sleeve, from_left=True):
    if from_left:
        return box((x - 0.35, y - 0.05, z - 0.05), (x - 0.08, y + 0.05, z + 0.05), sleeve) + \
               box((x - 0.08, y - 0.045, z - 0.03), (x + 0.06, y + 0.045, z + 0.03), (215, 175, 150))
    return box((x - 0.04, y - 0.05, z + 0.06), (x + 0.04, y + 0.05, z + 0.40), sleeve) + \
           box((x - 0.045, y - 0.06, z - 0.06), (x + 0.045, y + 0.06, z + 0.06), (215, 175, 150))


def shot_touch(t, dur):
    """单手触柄：林的浅色袖右手从左侧伸来，约到时长一半时指尖碰到弯柄并停住（允许接触），伞不动。"""
    u = ease(t / (dur * 0.5))
    tris = rack_closeup() + arm(3.12 + 0.44 * u, -1.0, 0.97, (225, 222, 215))
    return tris, Camera(*RACK_CAM), (0.3, 2.5)


def shot_approach(t, dur):
    """手停在柄前：林的浅色袖右手从左侧伸来，约到时长一半时停在弯柄左侧约7厘米，不接触。"""
    u = ease(t / (dur * 0.5))
    tris = rack_closeup() + arm(3.12 + 0.36 * u, -1.0, 0.97, (225, 222, 215))
    return tris, Camera(*RACK_CAM), (0.3, 2.5)


def shot_block(t, dur):
    """两手挡伞：陈从左侧伸来停在伞杆左侧约7厘米；林从上方落下停在陈的手上方约8厘米；彼此不接触、都不碰伞。"""
    u = ease(t / (dur * 0.5))
    v = ease((t - dur * 0.2) / (dur * 0.4))
    tris = rack_closeup() + arm(3.10 + 0.34 * u, -1.0, 0.80, (60, 70, 110)) + \
        arm(3.46, -1.0, 1.32 - 0.30 * v, (225, 222, 215), from_left=False)
    return tris, Camera(*RACK_CAM), (0.3, 2.5)


def shot_pick(t, dur):
    """陈取伞：陈的深蓝袖右手伸到弯柄、握住，把伞向上提起约12厘米（林的轻触由提示词描述）。"""
    u = ease(t / (dur * 0.4))
    lift = 0.12 * ease((t - dur * 0.45) / (dur * 0.35))
    tris = box((3.2, -1.6, -0.02), (4.4, -0.4, 0), FLOOR) + box((3.4, -1.2, 0), (3.8, -0.8, 0.55), DARK)
    tris += box((4.0, -1.8, 0), (4.1, 0, 2.2), WALL)
    tris += box((3.57, -1.03, 0.05 + lift), (3.63, -0.97, 0.95 + lift), YELLOW)
    tris += box((3.55, -1.06, 0.95 + lift), (3.65, -0.94, 1.02 + lift), (30, 30, 30))
    tris += arm(3.08 + 0.46 * u, -1.0, 0.98 + lift * (t > dur * 0.45), (60, 70, 110))
    return tris, Camera(*RACK_CAM), (0.3, 2.5)


# 模板名 → 函数(t, dur)。door 即原Y；block 即原Z的两手挡伞。
SHOTS = {"Y": lambda t, d: shot_Y(t), "Z": lambda t, d: shot_block(t, d), "door": lambda t, d: shot_Y(t),
         "wide": lambda t, d: shot_wide(t, d, True), "wide_nozhou": lambda t, d: shot_wide(t, d, False),
         "touch": shot_touch, "approach": shot_approach, "block": shot_block, "pick": shot_pick}


def main(name, seconds=SECONDS, out_name=None, out_dir=None):
    out = Path(out_dir) if out_dir else OUT
    out.mkdir(parents=True, exist_ok=True)
    out_name = out_name or name
    fn = SHOTS[name]
    n = int(FPS * seconds)
    enc = lambda dst, fmt: subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", fmt, "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-vf", "scale=854:480:flags=bicubic", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(dst)],
        stdin=subprocess.PIPE)
    pg, pd = enc(out / f"{out_name}-grey.mp4", "rgb24"), enc(out / f"{out_name}-depth.mp4", "gray")
    for i in range(n):
        tris, cam, nf = fn(i / FPS, seconds)
        rgb, depth = render(tris, cam, nf)
        pg.stdin.write(rgb)
        pd.stdin.write(depth)
        if i == n // 2:
            mid = (rgb, depth)
    for p in (pg, pd):
        p.stdin.close()
        p.wait()
    for tag, data, fmt in (("grey", mid[0], "rgb24"), ("depth", mid[1], "gray")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", fmt, "-s", f"{W}x{H}", "-i", "-",
                        "-vf", "scale=854:480", str(out / f"{out_name}-{tag}-mid.png")], input=data, check=True)
    print(name, n, "帧")


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else SECONDS)
