---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# 视频创作手册

**从构思到成片的视频创作方法，配可直接拆解的案例；以及用 AI 生成视频时，哪些做法真的有效。**

全书分两部分。**视频创作方法**讲视频本身怎么做——目标、结构、表演、调度、镜头、光色、剪辑、声音、字幕、动画、制作与评估，不论你实拍、做动画还是用 AI，这些原理都适用。**AI 视频方法**讲生成视频特有的问题：怎样设计适合生成的内容、怎样控制画面、怎样保持一致、怎样核对结果，结论来自约一百个镜头的实测。

[从这里开始](guide/04-reading-paths.md){ .md-button .md-button--primary } [遇到问题查这里](guide/10-problem-technique-index.md){ .md-button }

</div>

<figure class="vid"><video controls preload="metadata" src="assets/films/ex01-A1.mp4"></video><figcaption>综合案例 A《最后一把伞》的 AI 参考成片（30 秒，有声）：同一套分镜，改变观众先知道什么，体验就不同。</figcaption></figure>

## 内容导航

<div class="grid cards" markdown>

-   :material-movie-open-outline:{ .lg } **视频创作方法**

    ---

    13 章，每章是“方法 + 案例”。分镜精确到秒，写明机位、动作、声音和剪辑；每章附一部开放电影作为现成作品案例。

    [:octicons-arrow-right-24: 01 目标、研究与创意](methods/01-goals-research.md)

-   :material-robot-outline:{ .lg } **AI 视频方法**

    ---

    4 章：为 AI 设计内容 → 生成控制方式的演进（文生、首帧、全能参考、灰盒结构控制、声画同生）→ 一致性与抽卡率 → 后期与核对。厂商操作参数另见[备忘](ai/higgsfield.md)，未经本书实测。

    [:octicons-arrow-right-24: A2 生成控制方式的演进](ai/A2-control-evolution.md)

-   :material-play-box-multiple-outline:{ .lg } **案例**

    ---

    剧情、产品、纪录、对话、声音、音乐、科普、剪辑、字幕，10 个可直接照着做的完整案例。

    [:octicons-arrow-right-24: 最后一把伞](cases/01-umbrella.md)

-   :material-television-play:{ .lg } **示范与作品**

    ---

    可交互的图解、程序生成的对照视频，以及 9 部 Blender 开放电影的逐段观察。

    [:octicons-arrow-right-24: 现成作品观察](works.md)

</div>

## AI 生成：控制方式的演进

每一代都在上一代控制不住的地方加入新的输入。

| 阶段 | 控制从哪里来 | 解决了什么 | 还管不住什么 |
|---|---|---|---|
| ① 文生视频 | 文字提示词 | 氛围和大致动作 | 人物、店面每次都不同 |
| ② 首帧／首尾帧 | 一两张静帧 | 构图、起始和终止状态 | 手部接触、背景里冒出的东西 |
| ③ 全能参考 | 多张参考图、参考音频 | 跨镜头的人物与场景一致 | 空间位置与动作状态 |
| ④ 结构控制 | 灰盒／深度参考视频 | 站位与运动轨迹 | 动作停住后的状态 |
| ⑤ 声画同生 | 声音与画面一起生成 | 口型、碰撞声同步 | 跨镜嗓音、偶尔多说话 |

[:octicons-arrow-right-24: 每个阶段的实测与示例视频](ai/A2-control-evolution.md)

## 许可

文字以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 发布，代码以 MIT 发布，欢迎转载、改编和用于教学，请署名。书中分析的开放电影版权归 Blender 基金会，以 CC BY 协议发布。
