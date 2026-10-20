# 音画同步：故意制造的错位与修复

用[声音对照](sound-priority.md)里的 S1 版本，故意把接触声整轨延后0.5秒，再演示怎样定位并修好。这是为了演示流程而人为制造的错误。

<figure class="vid"><video controls preload="metadata" src="../sync-repair/delayed.mp4"></video><figcaption>错位版：接触声晚了0.5秒</figcaption></figure>
<figure class="vid"><video controls preload="metadata" src="../sync-repair/repaired.mp4"></video><figcaption>修复版</figcaption></figure>
对照基线：[S1 原版](sound-priority/S1.mp4)。

## 改了什么

只对接触声这一轨加了0.5秒延迟，画面和其他声轨都不动，所以碰杯声和扶正时的摩擦声一起变晚。修复时只把这一轨挪回原位，不移动整条混音。

| 检查 | 错位版 | 修复版 |
|---|---|---|
| 画面第一次接触 | 5秒 | 5秒 |
| 接触声峰值 | 约5.50秒 | 约5.00秒 |
| 判定（允许误差一帧，1/24秒） | 失败 | 通过 |
| 画面 | 与基线相同 | 与基线相同 |

## 返修步骤

画面接触点已确定 → 检查独立的动作声轨 → 找出偏移量 → 只修这一轨 → 重新导出 → 和基线比较。不要把所有声轨一起前移，也不要用缩短片段来掩盖错位。

## 局限

这里靠合成接触声的峰值定位，方法不能直接用到对白、复杂音乐或真实录音的同步检测上。一帧的容差是本例的工作条件，不是通用的感知标准。

重建：先生成[声音对照](sound-priority.md)，再运行 `python3 scripts/build_additional_demos.py`。参数记录见[verification.json](sync-repair/verification.json)。
