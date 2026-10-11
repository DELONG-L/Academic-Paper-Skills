# Brand assets and provenance / 品牌资源与来源

[English home](../README.md) · [中文首页](../README.zh-CN.md)

**Academic Paper Skills · 学术论文技能集** uses a folded manuscript page with four cells as its standalone mark. The README overview uses a flat forest-green module diagram: shared manuscript evidence supports writing, figures and tables, author review, and requirements. The four skills can be selected by task; the diagram does not prescribe a mandatory sequence.

独立品牌标识以四格折角稿纸对应四个技能。README 主图使用墨绿色平面模块图，呈现稿件与证据如何支持写作、图表、作者侧审阅和论文要求。四个技能按任务选用，图中没有规定必须依次使用。

| Resource / 资源 | Purpose / 用途 |
|---|---|
| [logo.svg](assets/logo.svg) | Standalone transparent vector mark / 独立透明矢量标识 |
| [skills-overview-en.png](assets/skills-overview-en.png) | English README overview / 英文技能概览 |
| [skills-overview-zh.png](assets/skills-overview-zh.png) | Chinese README overview / 中文技能概览 |
| [overview-prompts.md](assets/overview-prompts.md) | Overview generation prompts / 技能概览生成提示词 |
| [hero-en.svg](assets/hero-en.svg) | Earlier editable English banner / 早期可编辑英文横幅 |
| [hero-zh-CN.svg](assets/hero-zh-CN.svg) | Earlier editable Chinese banner / 早期可编辑中文横幅 |
| [hero-design.png](assets/hero-design.png) | Original generated design reference / 原始生成设计稿 |
| [hero-prompt.txt](assets/hero-prompt.txt) | Exact generation prompt / 完整生成提示词 |
| [build_brand.py](../scripts/build_brand.py) | Reproducible SVG source generator / SVG 源文件生成程序 |

The current overview PNGs were created with the built-in ImageGen tool. They depict skill ownership and typical outputs, not scientific findings. The English and Chinese editions use separate assets. No manuscript content or third-party logos were used as output assets.

当前技能概览 PNG 由内置 ImageGen 工具生成，表达技能职责与典型产出，不表示科研结果。中英文分别使用独立图片，输出资源未使用稿件内容或第三方 Logo。

The earlier design reference was created with the built-in ImageGen tool on 2026-09-29. Its SVG banners were reconstructed as editable text and geometry, preserving the folded-page mark, palette, four-sheet composition and editorial character. Their miniature charts are decorative, not experimental data. Leaves, books, pen props and soft shadows were simplified or omitted; labels and typography were set independently.

设计参考由内置 ImageGen 工具生成于 2026-09-29。最终 SVG 使用可编辑文字与几何对象重建，保留折角稿纸标识、配色、四页构图和编辑出版风格。为适应首页缩放，简化或省略了叶片、书本、钢笔和柔和阴影，文字与字体单独排版。输出资源未使用参考论文截图或第三方 Logo。

Regenerate the standalone logo and earlier SVG banners with `python scripts/build_brand.py`. This script does not generate or replace the current PNG overviews. The SVGs are self-contained, with explicit backgrounds for consistent light/dark GitHub display. They use platform serif/sans-serif fallbacks rather than embedding a font; inspect both languages after typography changes. The logo has a transparent background.

运行 `python scripts/build_brand.py` 可重建独立 Logo 和早期 SVG 横幅，不会生成或替换当前 PNG 概览。SVG 自包含，横幅使用明确背景。字体使用平台回退，不嵌入字体文件，修改排版后需检查两种语言。独立 Logo 背景透明。

These are project-owned visual assets under the repository license, not certification marks or evidence of affiliation. The workflow badge reports GitHub Actions status only; it does not certify scientific correctness or visual quality.

这些资源用于本项目，并适用仓库许可，不是认证标记或机构隶属证明。工作流徽章仅反映 GitHub Actions 状态，不证明科研正确性或视觉质量。
