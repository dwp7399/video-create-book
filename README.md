# 视频创作手册

从构思到成片的视频创作方法，配可直接拆解的案例；以及用 AI 生成视频时，哪些做法真的有效。

**在线阅读：** https://dwp7399.github.io/video-create-book/

## 内容

- **视频创作方法（13 章）**：目标与研究、结构、表演、世界与风格、调度、镜头、光色、剪辑、声音、字幕与图形、动画、制作、评估与交付。每章是“方法 + 案例”，分镜精确到秒，并附 Blender 开放电影的逐段观察。
- **AI 视频方法（4 章）**：为 AI 设计内容、生成控制方式的演进（文生 → 首帧 → 全能参考 → 灰盒结构控制 → 声画同生）、一致性与抽卡率、后期与核对。结论来自用 wan3.0 实测的约一百个镜头。
- **案例（10 个）**：剧情、产品、纪录、对话、声音、音乐、科普、剪辑、字幕。
- **示范**：交互图解、程序生成的对照视频，以及案例的 AI 参考成片。

## 本地预览

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

然后打开 http://127.0.0.1:8000 。

## 目录

```
docs/
  methods/   视频创作方法 01—13
  ai/        AI 视频方法 A1—A4
  cases/     案例
  guide/     阅读路径、问题索引、大纲、工作表、模板
  demos/     可播放示范与交互图解
  assets/    AI 参考成片与实验视频
  works.md   现成作品观察
scripts/     示范视频与灰盒参考的生成脚本（Python 标准库 + FFmpeg）
```

## 参与贡献

欢迎修正错误、补充案例或现成作品观察。新增技法和案例请按 [技法条目模板](docs/guide/03-technique-template.md) 编写；提交前运行 `mkdocs build --strict` 确认没有坏链。

## 许可

- 文字与图片：[CC BY 4.0](LICENSE)
- 代码（`scripts/`、站点脚本）：[MIT](LICENSE-CODE)
- 书中分析的开放电影（Sintel、Spring、Big Buck Bunny 等）版权归 Blender 基金会，以 CC BY 发布；本仓库只链接官方视频，不包含其片段。
