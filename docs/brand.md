# Brand assets and provenance / 品牌资源与来源

[English home](../README.md) · [中文首页](../README.zh-CN.md)

**Academic Paper Skills · 学术论文技能集** uses a folded manuscript page with four cells as its standalone mark. The README covers use an ivory-and-forest-green editorial composition: four manuscript sheets represent writing, figures and tables, author review, and requirements. The skills can be selected by task; their positions do not prescribe a mandatory sequence.

独立品牌标识以四格折角稿纸对应四个技能。README 封面采用米白与墨绿色的出版物版式，以四张稿纸对应论文写作、论文图表、作者侧审阅和论文要求。四个技能按任务选用，位置不表示固定顺序。

| Resource / 资源 | Purpose / 用途 |
|---|---|
| [logo.svg](assets/logo.svg) | Standalone transparent vector mark / 独立透明矢量标识 |
| [readme-cover-en.png](assets/readme-cover-en.png) | English editorial README cover / 英文 README 封面 |
| [readme-cover-zh.png](assets/readme-cover-zh.png) | Chinese editorial README cover / 中文 README 封面 |
| [readme-cover-prompts.md](assets/readme-cover-prompts.md) | Cover generation and localization prompts / 封面生成与本地化提示词 |
| [skills-overview-en.png](assets/skills-overview-en.png) | Earlier English module overview / 早期英文技能概览 |
| [skills-overview-zh.png](assets/skills-overview-zh.png) | Earlier Chinese module overview / 早期中文技能概览 |
| [overview-prompts.md](assets/overview-prompts.md) | Overview generation prompts / 技能概览生成提示词 |
| [hero-en.svg](assets/hero-en.svg) | Earlier editable English banner / 早期可编辑英文横幅 |
| [hero-zh-CN.svg](assets/hero-zh-CN.svg) | Earlier editable Chinese banner / 早期可编辑中文横幅 |
| [hero-design.png](assets/hero-design.png) | Original generated design reference / 原始生成设计稿 |
| [hero-prompt.txt](assets/hero-prompt.txt) | Exact generation prompt / 完整生成提示词 |
| [build_brand.py](../scripts/build_brand.py) | Reproducible SVG source generator / SVG 源文件生成程序 |

The editorial covers were created with the built-in ImageGen tool. Paragraph rules, margin annotations, empty tables, and unchecked boxes are conceptual motifs, not manuscript screenshots or research results. The English cover was generated and refined; the Chinese cover localizes its composition. Both editions have their own asset and text.

出版物风格的封面由内置 ImageGen 工具生成。段落线、页边批注、空白表格和未勾选清单属于概念示意，不是稿件截图或科研结果。英文封面经生成和细化，中文封面在同一构图上本地化。两个语言版本使用各自的图片和文字。

The earlier module overview PNGs were also created with the built-in ImageGen tool. They depict skill ownership and typical outputs without prescribing a sequence. No manuscript content or third-party logos were used in either set of assets.

早期模块概览 PNG 同样由内置 ImageGen 工具生成，表达技能职责与典型产物，不规定使用顺序。两组资源均未使用实际稿件内容或第三方 Logo。

The earlier design reference was created with the built-in ImageGen tool on 2026-09-29. Its SVG banners were reconstructed as editable text and geometry, preserving the folded-page mark, palette, four-sheet composition and editorial character. Their miniature charts are decorative, not experimental data. Leaves, books, pen props and soft shadows were simplified or omitted; labels and typography were set independently.

设计参考由内置 ImageGen 工具生成于 2026-09-29。最终 SVG 使用可编辑文字与几何对象重建，保留折角稿纸标识、配色、四页构图和编辑出版风格。为适应首页缩放，简化或省略了叶片、书本、钢笔和柔和阴影，文字与字体单独排版。输出资源未使用参考论文截图或第三方 Logo。

Regenerate the standalone logo and earlier SVG banners with `python scripts/build_brand.py`. This script does not generate or replace the PNG covers or module overviews. The SVGs are self-contained, with explicit backgrounds for consistent light/dark GitHub display. They use platform serif/sans-serif fallbacks rather than embedding a font; inspect both languages after typography changes. The logo has a transparent background.

运行 `python scripts/build_brand.py` 可重建独立 Logo 和早期 SVG 横幅，不会生成或替换 PNG 封面与模块概览。SVG 自包含，横幅使用明确背景。字体使用平台回退，不嵌入字体文件，修改排版后需检查两种语言。独立 Logo 背景透明。

These are project-owned visual assets under the repository license, not certification marks or evidence of affiliation. The workflow badge reports GitHub Actions status only; it does not certify scientific correctness or visual quality.

这些资源用于本项目，并适用仓库许可，不是认证标记或机构隶属证明。工作流徽章仅反映 GitHub Actions 状态，不证明科研正确性或视觉质量。
