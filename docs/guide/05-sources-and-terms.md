# 来源、术语约定与时效边界

本手册主要是自创实践设计，来源用于核对特定定义和边界，不代表全部建议经实验验证。没有使用真实影片台词或复制影视分镜。具体导演/作品的深入分析应以实际观看和可回溯片段为依据，不用导演姓名替代取景与声音指令。

| 来源 | 支撑范围 | 使用边界 |
|---|---|---|
| [Adobe：J/L cut 操作定义](https://helpx.adobe.com/in/premiere/desktop/edit-projects/trim-clips/perform-j-cuts-and-l-cuts.html) | 下场声音先于画面、上场声音延续到下场画面 | 支撑术语，不证明某个切法必然改善情绪 |
| [ARRI Signature 镜头材料](https://www.arri.com/resource/blob/225644/c83fcb0e41b5a241e75cdc399ade586e/signature-brochure-data.pdf) | 焦距对照示例通过改变相机位置保持主体大小 | 对照须交代机位变化，避免误归因；非产品推荐 |
| [Blender 2.90：关键帧基础](https://docs.blender.org/manual/en/2.90/animation/keyframes/introduction.html) | 关键值及中间插值的基本概念 | 稳定原理参考；不是当前软件界面操作指南。最新地址本次抓取失败，未据此描述当期UI |
| [W3C WAI：字幕](https://www.w3.org/WAI/media/av/captions/) | 必要语言和非语言声信息的同步文字表达、人工校对自动字幕 | 不把字幕等同于解决全部观看需求 |
| [W3C WAI：视觉信息描述](https://www.w3.org/WAI/media/av/description/) | 用描述提供理解所需的视觉信息 | 按内容与观看要求设计，不在本书作具体法律判断 |
| [NFB：纪录创作伦理讨论](https://blog.nfb.ca/blog/2014/09/17/documentary-ethics/) | 创作者与被摄者关系、责任及纪实实践反思 | 支撑研究视角，不当作各地统一法律规则 |

## 本书术语约定

- **结构**：段落、事件、信息或感知模式的整体安排；不只指三幕。
- **节拍**：一次有意义的动作、信息或关系变化；音乐节拍按音乐语境另行说明。
- **交叉剪辑**：交替呈现有关联、可能趋于汇合的行动线；是否同时发生需有片内线索。
- **平行剪辑**：以比较、对照或主题联系并置镜头；不默认同一时间。这是本书约定，其他教材可能不同。
- **镜内运动**：人物、物体、光或相机导致的画面变化；相机运动与主体运动分开记录。
- **风格**：跨镜头重复且有表达意义的选择集合；不是滤镜、画幅或工具名。
- **基础/变化版**：针对同一目标比较的方案，不声称后者对所有作品更好。
- **静默**：按需要撤去或减少部分声部，可能保留底噪；并非总是数字静音。
- **AI 控制要求**：创作希望实现的条件，不代表任意模型都支持或保证满足。

## 工具能力与交付规格核对卡

每次实际制作填写：工具/版本、核对日期、官方文档URL、支持的输入/参考/时长/分辨率/帧率/声音、输出限制、成本及本次测试结果。发布端另填画幅、分辨率、字幕、音频与封面要求。方法论不写死跨平台通用的钩子秒数、码率、响度或安全区。

参数未核实就留“待核”，并采用工具无关的替代方案。不要把模型宣传中的能力、提示词中的愿望和本次素材实际通过的检查写在同一列。

## 作品方法分析补充来源

- [Wes Anderson本人访谈，Filmmaker，2014-03-08](https://filmmakermagazine.com/84877-wes-anderson-on-using-throwback-ratios-romantic-worldviews-and-european-reconnaissance-to-craft-the-grand-budapest-hotel/)：04章用于区分创作者所述选择与本书迁移分析。
- [Helga Cranston制作回忆，BFI，2016-05-10](https://www.bfi.org.uk/features/tales-film-editor-making-olivier-hamlet)：04章用于讨论持续表演、语言节奏与剪辑的关系。

仅摘述相关决定，没有伪造影片镜头时间码；自创练习与原片分开。

## 厂商教程：Higgsfield

以下页面用于[操作备忘](../ai/higgsfield.md)核对入口、限额和版本差异。它们是 Higgsfield 自己的产品说明，带订阅和积分引导。本书没有复现其中的一致性、同步或成本说法；页面之间的数字冲突在备忘里并列，不取平均。

| 来源 | 支撑范围 | 使用边界 |
|---|---|---|
| [影视制作指南，2026-10-23](https://higgsfield.ai/blog/how-to-master-ai-filmmaking) | 参考先进视频、多镜时间码示例、一镜一个运镜的排错、成片修补按钮、外部剪辑 | 示例提示不是控制字段；5 秒标价未见同一天的完整价目表 |
| [分镜与镜头表，2026-08-28](https://higgsfield.ai/blog/script-to-ai-storyboard-shot-list) | 镜头表字段、Popcorn 一次最多 4 张参考和 8 帧、跨批用已有帧 | 自称五个要素却列出七项，只作写作顺序 |
| [Cinema Studio 4.0 指南，2026-10-27](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide) | 4.0 参数、30 秒/1080p、50 份参考、2026-10-24 的积分表、API 限额 | 价目含原生声音和 16:9；Unlimited 套餐是否免扣，该文未写 |
| [运镜，2026-10-09](https://higgsfield.ai/blog/ai-video-camera-control) | 速度与起止构图、推/变焦要分开写、4.0 参数表 | “30+ 运镜、50+ 调色”没有完整名单；参考写成 50 张图，与 10-27 的混合参考不一致 |
| [Cinema Studio 3.5 教程，2026-07-15](https://higgsfield.ai/blog/cinema-studio-3.5-full-tutorial) | 3.5 的类型、调色、运镜风格、光、机身、镜头、五档焦距、三档光圈 | 不能填进 4.0；比较文里的 85mm 等是手动提示，不是这张表 |
| [图生视频，2026-08-02](https://higgsfield.ai/blog/photo-to-ai-video) | 3.5 一次最多 9 张参考图 | 与帮助中心 3.0 的“9 份参考”不是同一篇 |
| [短片流水线，2026-07-29](https://higgsfield.ai/blog/ai-short-film-pipeline) | 早期的 4/6/8 帧和 3.5 计数方式 | 积分和“自动收片”与 2026 年 9–10 月页面冲突 |
| [动画短片，2026-09-26](https://higgsfield.ai/blog/ai-animated-short-film-2026) | 外部剪辑、口型语言数的另一种说法、Genjutsu 的另一套限额 | 与 10-23 的 Genjutsu 限额并列，未登录分辨哪套仍有效 |
| [把自己放进视频，2026-10-23](https://higgsfield.ai/blog/how-to-put-yourself-in-ai-video) | Soul ID 20–80 张、约 3–5 分钟、960px、滤镜与合影 | 不包含“重影”；口型路径是先克隆声音再对口型，帮助中心允许直接打字 |
| [YouTube 提示词库，2026-03-12](https://higgsfield.ai/blog/ai-short-film-youtube-guide) | 角色转面和场景转面的排版模板 | 模板不是验收标准；没有单独核对视频字幕 |
| [Soul ID 帮助中心](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)（修改 2026-09-02） | 训练照片、不能导出、非像素级一致、Elements | 优先于博客的跨模型免上传承诺 |
| [Popcorn 帮助中心](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-popcorn)（修改 2026-09-12） | 上限 8 帧、4 张参考、画幅、提示五段 | 未写死只能 4/6/8 |
| [Cinema Studio 帮助中心](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio)（修改 2026-09-01） | 2.5–4.0 的能力边界、上传时长、情绪滑杆、Unlimited 可能不扣积分 | 早于 10 月博客，具名列表以较新博客为准并注明差异 |
| [口型与画幅帮助中心](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-lipsync-voiceover-and-aspect-ratios)（修改 2026-09-01） | Audio 与 Lipsync Studio 分开；翻译 18 种语言 | “完美对齐”是卖点，不作为同步实测 |
| [Academy 课程索引](https://higgsfield.ai/academy)；[角色表一课](https://higgsfield.ai/academy/courses/santiago-cinematic/character-sheets-in-soul-cinema) | 课程存在、该课约 2 分钟 | 口播未取得。[Prompt Bank](https://higgsfield.ai/academy/apps/prompt-bank) 于 2026-10-28 为 404 |
