# Higgsfield 影视流程备忘

本页只记录 [Higgsfield](https://higgsfield.ai/) 官方博客、帮助中心和 Academy 页面上写过的操作。这些页面由厂商发布，用来介绍自己的产品和积分，不是独立测试。本书没有用这些工具复现过任何一条；下文的数字只在所引页面、所引日期上成立。换版本或改套餐后，先重填[工具能力核对卡](../guide/05-sources-and-terms.md#工具能力与交付规格核对卡)，再决定能否执行。

一致性、镜头表、声音职责的判断仍以 A1–A4 和上篇为准。本页不把厂商的提示词模板当成已经生效的控制。

核对日期：2026-10-28。页面若同时给出 `datePublished` 与 `dateModified`，表中写的是发布日，帮助中心另注修改日。

## 和本书章节的分工

| 要决定的事 | 写在哪 | 本页只补充 |
|---|---|---|
| 角色、场景、道具怎样做成可复用参考 | [A3](A3-consistency-yield.md)、[04章](../methods/04-world-style.md) | Soul ID 的张数、像素、训练时间和不能导出 |
| 镜头表、景别、运镜、一次生成里的硬切 | [05章](../methods/05-staging.md)、[06章](../methods/06-camera.md)、[08章](../methods/08-time-editing.md)、[A1](A1-content-design.md)、[A2](A2-control-evolution.md) | Popcorn 限额；Cinema Studio 3.5 / 4.0 的参数表 |
| 环境声、对白、口型、拼接 | [09章](../methods/09-sound.md)、[A4](A4-post-review.md) | 原生声音、Seed Audio、Lipsync Studio、后期按钮各在哪 |
| 资产台账 | [12章](../methods/12-production.md) | 训好的身份不是可下载文件 |

## 厂商流程，以及它没有替你做的事

2026-10-23 的[影视制作指南](https://higgsfield.ai/blog/how-to-master-ai-filmmaking)把一条 10 秒场景写成：一句话事件 → 镜头表 → 角色表和空场景图 → 在提示词里用 @ 标这两张参考 → Cinema Studio 4.0 一次生成多镜并打开声音 → 再用 Relight、调色、Trim、Extend、Edit、Reframe、Upscale 改成片。多场片子要分开生成，再到任意剪辑软件里接。

更早的页面把流水线写得更满，而且和后来的说法不一致：

| 说法 | 出处 | 和后来页面的差别 |
|---|---|---|
| Popcorn 出分镜，Soul ID 锁脸，Cinema Studio 出镜头，Seed Audio 出对白/环境/配乐，Supercomputer 把成片收齐 | [2026-07-29 短片流水线](https://higgsfield.ai/blog/ai-short-film-pipeline) | 2026-10-23 指南和 [2026-09-26 动画短片](https://higgsfield.ai/blog/ai-animated-short-film-2026)都写明：平台按条导出，长片要在外部剪辑软件里接。7 月那篇让 Supercomputer“收成一条”没有操作步骤 |
| 分镜帧可以直接交给 Cinema Studio 4.0 | [2026-08-28 分镜与镜头表](https://higgsfield.ai/blog/script-to-ai-storyboard-shot-list) | 帮助中心的 [Popcorn 文](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-popcorn)（修改于 2026-09-12）写的是：帧可以作为 Kling 或 Veo 的起始帧/参考，并建议用上一镜末帧接下一镜。没有写“一键进入 4.0” |

因此本书采用的操作顺序是：镜头表 → 批准的参考 → 分镜静帧 → 按镜或按短多镜生成 → 外部剪辑。不把“一个账号里工具彼此交接”写成连续性已经解决。

## 素材：角色、场景、道具

### 角色转面表

[2026-03-12 的提示词库](https://higgsfield.ai/blog/ai-short-film-youtube-guide)给了一条给 Nano Banana Pro 用的模板，不是测量过的验收标准。它要求：干净中性背景；上排四张全身站姿，正面、左侧面、右侧面、背面；下排三张面部近景，正面、左侧面、右侧面；各格同一身份、同一尺度、放松的 A 姿态、同一套光。页面没有给出像素、边距或“必须 A 姿态模型才会认人”的测试。

同一页的场景表模板是：上排正面、左斜、右斜、反打全景；下排三张环境局部；风格、光和比例跟原参考走。2026-10-23 指南另要求场景先做一张空镜，再把这张空镜当作每镜的地点参考。道具没有单独的张数规定；分镜文的例子是把道具参考和人物、地点一起交给同一次生成。

Academy 课程 [Character sheets in Soul Cinema](https://higgsfield.ai/academy/courses/santiago-cinematic/character-sheets-in-soul-cinema) 只有课名和约 2 分钟的时长标记，课文和口播这次没有拿到，不根据课名补内容。

### Soul ID

帮助中心 [How do I create and use a Soul ID character?](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)（发布 2026-08-01，修改 2026-09-02）是操作边界，优先于博客上的效果承诺。

| 项目 | 帮助中心 | 博客上的不同说法 |
|---|---|---|
| 照片数量 | 同一人 20 张起，最多 80 张 | [2026-10-23 把自己放进视频](https://higgsfield.ai/blog/how-to-put-yourself-in-ai-video)同为 20–80；[2026-07-29 流水线](https://higgsfield.ai/blog/ai-short-film-pipeline)只写 20+ |
| 训练时间 | “几分钟” | 2026-10-23 文写约 3–5 分钟 |
| 全身 | 至少一张全身高度；只有头像不够 | 2026-10-23 文写至少一张全身 |
| 照片质量 | 清楚、光线均匀、多角度多表情；不要墨镜、重阴影、裁掉的脸、重复同姿态、合影；近 4–5 个月的近照 | 2026-10-23 文另写建议不低于 960px，并避开美颜、磨皮、改脸滤镜。原文没有“重影”这一条 |
| 费用 | 本页未标价 | 多篇写训练一次 25 积分。美元换算见下节，各篇算法不同 |
| 用在哪里 | Soul 家族；Seedance 里通过 Elements，用 @ 调用。身份文件不能导出 | 2026-07-29 流水线写可跨 Kling 3.0、Veo 3.1、Seedance 2.0、WAN 2.6 且不用再上传。帮助中心没有这份名单 |
| 效果边界 | 目标是“看得出是同一人”，不是像素级同一张脸；极端风格和少见角度仍会漂。一个人一个 Soul ID，两个以上的人用 Elements | 流水线把训练写成“从第一场到第十场不再漂”。这是营销句，帮助中心自己否定了像素级锁定 |

[2026-09-26 动画短片](https://higgsfield.ai/blog/ai-animated-short-film-2026)的价目行是 “Soul ID，1 character，1188px，25 积分”。它没有说明 1188px 是训练照片下限还是某张输出的尺寸，不能拿来替换 960px 那条建议。

发明的角色可以先生成一组肖像再训练。只出现一次的人，厂商自己也说不必训练。

### 场景、道具和换装

地点和道具在 Cinema Studio 帮助中心里做成 Elements，和角色一样复用。这是平台内资产，台账要记名称、日期和已批准的静帧，不能只写“已训练”。

换装和换道具被放在 Genjutsu，两篇官方文的限额对不上，不能合成一条：

| 日期与页面 | 输入视频 | 参考图 | 其他 |
|---|---|---|---|
| [2026-10-23 影视指南](https://higgsfield.ai/blog/how-to-master-ai-filmmaking) | 4–15 秒 | 最多 10 张人物、产品或衣服 | 15 秒、720p 标为 32 积分（按该文 Plus 换算约 $1.57） |
| [2026-09-26 动画短片](https://higgsfield.ai/blog/ai-animated-short-film-2026) | 4–30 秒 | 最多 30 张 | 输出最高 1080p；并区分换物件和把动作挪到另一个角色。30 秒、720p 标为 217 积分 |

两篇都要求只用有权使用的脸和产品。哪一套是当前界面，本次未登录核对。

## 镜头：镜头表、分镜、机位

### 先写镜头表，再出分镜帧

[2026-08-28 分镜文](https://higgsfield.ai/blog/script-to-ai-storyboard-shot-list)把镜头表和分镜分开：分镜是每一镜的画面，镜头表写景别、角度、运动、用途和参考。示例列是 Scene、Shot、Shot Size、Camera Movement、Reference、Notes。短场它认为通常 4–8 格；对白可以少，动作节拍多就用满。超过一次生成的格数就拆批。下一批用上一批里最稳的那一帧当参考，减轻漂移。这些是制作顺序，不是模型保证。

### Popcorn 的限额

| 项目 | 写在哪 | 数字 |
|---|---|---|
| 一次参考图 | 帮助中心 Popcorn 文；2026-08-28 分镜文 | 最多 4 张，按编号写各自职责（人、景、服装或道具） |
| 一次帧数 | 帮助中心（2026-09-12）：Auto 自选，上限 8。2026-07-29 流水线和 [2026-08-02 图生视频](https://higgsfield.ai/blog/photo-to-ai-video)写成 4、6 或 8 | 是否允许 5 或 7，两套文档没有统一。执行前看生成按钮 |
| 模式 | 帮助中心 | Auto：一条提示加帧数。Manual：逐帧写。另有 Instadump（风格包套到一张照片上），与分镜不是同一任务 |
| 画幅 | 帮助中心列出 3:4、2:3、3:2、4:3、16:9、1:1、9:16，外加 Auto。2026-08-28 文有同样七种但没写 Auto。2026-07-29 文少了 4:3 和 16:9 | 以帮助中心较新的一览为准，旧博文的缺项不当成“不支持” |
| 提示结构 | 帮助中心五段：主体、场景、风格、动作、气氛。2026-08-28 文自称“五个要素”，紧接着却列出景别、运镜、主体、动作、场景、光/风格、参考共七项 | 两边都只是写作顺序 |

帮助中心没有承诺 Popcorn 帧会自动变成 Cinema Studio 4.0 的镜头。

### Cinema Studio：3.5 和 4.0 不是同一套旋钮

帮助中心 [How do I use Cinema Studio?](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio)（修改于 2026-09-01）概括各版：2.5 最多 3 个 Soul Cast；3.0 最多 9 份参考、7 种类型，并有速度曲线（Linear、Auto、Flash In、Flash Out、Slow-mo、Bullet Time、Impact、Ramp Up）；3.5 有 Claude 对话草拟提示和参数，但生成仍须人点；4.0 为默认，称基于 Seedance 2.5，最多 50 份参考、单条最多 30 秒。视频上传：2.5 不接受，3.0 和 3.5 最长 15 秒，4.0 最长 30 秒。该页把 4.0 的表演控制写成“情绪滑杆”，没有列出八个情绪名。

3.5 的具名选项以 [2026-07-15 教程](https://higgsfield.ai/blog/cinema-studio-3.5-full-tutorial) 的表为准：

| 设置 | 2026-07-15 列出的选项 |
|---|---|
| 类型 | General、Action、Epic、Drama、Comedy、Horror、Noir |
| 调色 | Auto，以及 Naturalistic Clean、Bleached Warm、Hyper Neon、Teal & Orange Epic、Sodium Decay、Cold Steel、Bleach Bypass、Classic B&W |
| 运镜风格 | Auto，以及 Classic Static、Silent Machine、One Take、Epic Scale、Intimate Observer、Impossible Camera、Documentary Snap、Raw Chaos、Dreamy Flow |
| 光 | Auto，以及 Soft Cross、Overhead Fall、Contre-jour、Window、Practicals、Silhouette |
| 机身 | Raw 16mm、Fine Film、Clean Digital |
| 镜头 | Auto，以及 Clinical Sharp、Extreme Macro、Anamorphic、Warm Halation、Vintage Haze |
| 焦距 | 8mm、14mm、35mm、50mm、75mm 五档，不是 8–75 之间任意值 |
| 光圈 | f/1.4、f/4、f/11 |

[2026-08-02 图生视频](https://higgsfield.ai/blog/photo-to-ai-video)的问答写 Cinema Studio 3.5 一次最多 9 张参考图，和帮助中心里 3.0 的“最多 9 份参考”数字相同，但是两篇不同的页面。2026-07-29 流水线把 3.5 记成“调色 9、光 7、运镜风格 10、镜头 6、焦距 8–75mm、光圈 3”。和 7 月 15 日的表对照：光的 6 个具名预设加 Auto 可以数成 7；调色 8 个具名加 Auto 可以数成 9；运镜风格是 9 个具名加 Auto。帮助中心只说“8 套调色、10 种运镜风格、6 个灯光预设”，没有逐项名单。另外，[一篇同月的模型比较](https://higgsfield.ai/blog/most-reliable-ai-video-generators-2026)在 3.5 例子里出现 85mm、f/2.8、f/2.0 和表上没有的灯光名，并声明其中一部分是手动写进提示词的，不能当成下拉菜单。

4.0 的具名选项以 [2026-10-09 运镜文](https://higgsfield.ai/blog/ai-video-camera-control) 和 [2026-10-27 指南](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide) 为准。两篇一致的部分：

| 设置 | 选项 |
|---|---|
| 类型 | General、Action、Epic、Drama、Comedy、Horror、Noir |
| 年代 | 10-09 文含 Auto、60s、80s、90s、2000s、2020s。10-27 文只列五个年代。10-23 的示例用过 Era: Auto |
| 节奏 Tempo | Auto、Chaotic、Dynamic、Calm、Single shot。它管的是剪辑切得多快，不是主体动作速度 |
| 情绪 | 两篇博客写八项：Hope、Anger、Joy、Trust、Fear、Surprise、Sadness、Disgust，用 @ 标到角色。帮助中心写的是滑杆。是否同一控件，页面没有对照 |
| 调色 | 称 50 套以上，只举例，没有完整名单 |
| 运镜 | 称 30 种以上。公开例子有 POV、Robot arm、Pan left、Dolly in、Helicopter。完整名单未列出 |
| 光 | Auto 或 Soft Cross、Overhead Fall、Contre-jour、Window、Practicals、Silhouette；也可手调颜色、亮度、散射、角度 |
| 机身 | Auto、Modern、35mm Film、8mm Film、DV Camcorder |
| 镜头 | Auto、Clean Sharp、Anamorphic、Vintage Anamorphic、Warm Vintage、Halation Vintage |
| 光圈 | Auto、f/1.4、f/4、f/11 |
| 时长与分辨率 | 网页单次最长 30 秒、最高 1080p。API 时长 4–30 秒，分辨率只写 480p 和 720p |
| 参考 | 网页：10-27 文写一次最多 50 份；API 为最多 30 张图、10 段视频、10 段音频，合计不超过 50。10-09 文写成“最多 50 张图”，没有提视频和音频 |

4.0 相对 3.5 拿掉了分档焦距和 MoveSet Style 那一组名字，换成年代、节奏、另一套机身/镜头名，以及更多参考和更长的单条。不要把 3.5 的 14mm、Clinical Sharp 填进 4.0 的表，也不要反过来。

10-09 文还有一条和 10-23 排错表不完全相同的说法：运镜预设定的是这一镜的运动气质，具体路径仍要写在提示词里，并写明速度、起幅和落幅；推和变焦要用文字互相排除。10-23 排错表则写“一镜只用 Camera → Movement 里的一个运动”。两句都留着：预设不能代替起止构图，一句提示里叠两个运镜会漂。

### 一次生成里的多镜

10-23 指南的示例提示用时间码写三段，并在 2.5 秒和 5.0 秒写 HARD CUT，同时用文字锁参考职责、火车停稳、光和声音。这是一篇示例，不是帮助中心列出的字段。Tempo 若设为 Single shot，10-27 文明确说不要再要求快速多角度硬切。

单条不够长时，Extend 分 Sequel（往后）和 Prequel（往前）。帮助中心 4.0 的说法是 Forward / Backward Extend，上传视频最长 30 秒。续写只加长一条素材，不决定场与场怎么剪。

## 声音、口型与后期

三条路不要并成一句“Higgsfield 会配音”：

| 路 | 官方怎么写 | 适合放进本书的哪一步 |
|---|---|---|
| 生成时打开声音 | 10-27 文：Cinema Studio 可在同一次生成原生声音。帮助中心称 2.5 到 4.0 都会带效果、语音和音乐。Lipsync 帮助页把“物理上对齐”写成卖点 | 只把环境声和必须跟画面一起发生的动作声写进该镜。本书自己的同步误差见 A4，不采用“完美对齐” |
| 单独的声音 | 10-23 文：需要独立的人声或背景时用 Audio 里的 Seed Audio 1.0。帮助中心 [口型与画幅](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-lipsync-voiceover-and-aspect-ratios)（修改于 2026-09-01）把语音合成、换声、翻译放在 Audio，和口型分开 | 对白、环境床、音乐分轨制作。翻译模式写明 18 种语言 |
| 后期口型 | 同一帮助页：Lipsync Studio 吃图片或视频，台词可以打字，也可以用已经生成的音频。列出的模型包括若干图生说话和两条视频对口型（Kling Lipsync、Sync Lipsync 3，后者写最高 4K）。2026-10-23 文的路径是：先在 Audio 克隆声音并生成语音，再送进 Lipsync Studio | 对白轨已经确定之后。帮助中心没有写“必须正面脸”或“必须先导出音频” |

[2026-09-26 动画短片](https://higgsfield.ai/blog/ai-animated-short-film-2026)正文写 Lipsync Studio 覆盖 “18+” 种语言，同页问答又写成 18 种。帮助中心把“18 种语言”记在 Audio 的翻译上，没有记在每一个口型模型上。口型能覆盖哪些语言，本次没有逐个模型核对。

10-23 指南的成片修补按钮：光线用 Relight，颜色用 Edit Color Palette，局部物体或脸用 Edit video，头尾多余帧用 Trim，加长用 Extend，画幅用 Reframe（称最高 4K），分辨率用 Upscale（称最高 4K）。生成本身最高 1080p，4K 是后期步骤，不是生成档。

## 积分：同一条片子有多份报价

各篇都用积分，并常按 “$49 / 1000 积分” 估算美元（约 $0.049）。7 月和 9 月的一些表按约 $0.05 估算（25 积分写成约 $1.25）。帮助中心又写：若该模型在当前套餐的 Unlimited 列表里，网页生成不扣积分。所以下面的表是厂商在该日写下的标价，不是成交价。

Cinema Studio 4.0、原生声音、16:9，[2026-10-27 指南](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide) 称价目核于 2026-10-24：

| 时长 | 480p | 720p | 1080p |
|---|---|---|---|
| 10 秒 | 30 | 70 | 160 |
| 15 秒 | 45 | 105 | 240 |
| 30 秒 | 90 | 210 | 480 |

单位是积分。按该文 $0.049，30 秒 1080p 约为 $23.52。同月 [2026-10-23 指南](https://higgsfield.ai/blog/how-to-master-ai-filmmaking) 另写 5 秒 1080p 为 80 积分，约 $3.92；10-27 的表没有 5 秒这一行。一次出 4 个版本按 4 次计。该文称失败生成通常自动退还，文本请求进 Supercomputer 也扣积分，且 Unlimited 不覆盖 Supercomputer。

互相打架、不要拿来做预算的旧数字：

- 2026-07-29：Cinema Studio 15 秒 1080p 约 150 积分；8 秒 720p 约 75 积分。与上表的 15 秒 1080p = 240 不符。
- 2026-09-26：30 秒 720p 标 210 积分，和上表的 720p 行一致，但美元按约 $10.50 而不是 $10.29。同页 Popcorn 8 帧标 5 积分，Soul Cinema 一张 2K 标 0.125 积分，并写价目核于 2026 年 9 月。
- 2026-10-23：Seedance 2.5、10 秒、1080p 的一条示例为 160 积分。那是另一个模型的示例，不是 Cinema Studio 价目表。

生成按钮上的当次积分才是下单依据。本书不采用任何一篇里的“五分钟短片约一百五十美元”或“几天做完”作为成本或工期。

## 这次没有写成事实的内容

- Academy 各课的口播，包括角色表那一课。课程索引能打开，[Prompt Bank](https://higgsfield.ai/academy/apps/prompt-bank) 于 2026-10-28 返回 404。
- YouTube 上的独立字幕。3 月 12 日那篇是视频的提示词库，页面没有给出视频编号，本次没有另拉字幕轨。
- 帖子 `https://x.com/higgsfield_ai/status/2115094837796257917` 未打开，不用它支持任何数字。
- “重影不能训练”“口型必须正面清晰脸”“先有音频再有画面”这三句。照片规则里有遮挡、合影、滤镜和同角度连拍；口型帮助页允许文本或音频、图片或视频。
- 跨模型免上传、像素级同一张脸、原生声音物理对齐、分镜自动等于成片、Supercomputer 自动出长片。
- 30 种运镜、50 套调色的完整名单。
- 厂商展示片和节展映的完成度。页面点到片名，本次没有核片。
