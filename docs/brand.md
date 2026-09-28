# Brand assets and provenance / 品牌资源与来源

[English home](../README.md) · [中文首页](../README.zh-CN.md)

**Academic Paper Skills · 学术论文技能集** uses a folded manuscript page with four cells to represent its four coordinated skills. Forest ink, warm paper, sage, blue and terracotta carry the identity. The banners depict writing, visual artifacts, review and requirements as four manuscript sheets. Their miniature charts are decorative, not experimental data.

品牌标识以四格折角稿纸对应四个技能，使用墨绿、暖纸色、灰绿、浅蓝与赭色。主图的四张稿纸分别表达写作、图表、审阅与要求检查。小型图表仅用于品牌示意，不代表实验结果。

| Resource / 资源 | Purpose / 用途 |
|---|---|
| [logo.svg](assets/logo.svg) | Standalone transparent vector mark / 独立透明矢量标识 |
| [hero-en.svg](assets/hero-en.svg) | English README banner / 英文主图 |
| [hero-zh-CN.svg](assets/hero-zh-CN.svg) | Chinese README banner / 中文主图 |
| [hero-design.png](assets/hero-design.png) | Original generated design reference / 原始生成设计稿 |
| [hero-prompt.txt](assets/hero-prompt.txt) | Exact generation prompt / 完整生成提示词 |
| [build_brand.py](../scripts/build_brand.py) | Reproducible SVG source generator / SVG 源文件生成程序 |

The design reference was created with the built-in ImageGen tool on 2026-09-29. The final SVGs were reconstructed as editable text and geometry, preserving the folded-page mark, palette, four-sheet composition and editorial character. Leaves, books, pen props and soft shadows were simplified or omitted for smaller README rendering; labels and typography were set independently. No reference-paper screenshots or third-party logos were used as output assets.

设计参考由内置 ImageGen 工具生成于 2026-09-29。最终 SVG 使用可编辑文字与几何对象重建，保留折角稿纸标识、配色、四页构图和编辑出版风格。为适应首页缩放，简化或省略了叶片、书本、钢笔和柔和阴影，文字与字体单独排版。输出资源未使用参考论文截图或第三方 Logo。

Regenerate with `python scripts/build_brand.py`. The SVGs are self-contained, with explicit backgrounds for consistent light/dark GitHub display. They use platform serif/sans-serif fallbacks rather than embedding a font; inspect both languages after typography changes. The logo has a transparent background.

运行 `python scripts/build_brand.py` 可重建。SVG 自包含；主图使用明确背景，保证 GitHub 明暗主题下的整体一致性。字体使用平台回退，不嵌入字体文件，修改排版后需检查两种语言。独立 Logo 背景透明。

These are project-owned visual assets under the repository license, not certification marks or evidence of affiliation. The workflow badge reports GitHub Actions status only; it does not certify scientific correctness or visual quality.

这些资源用于本项目，并适用仓库许可，不是认证标记或机构隶属证明。工作流徽章仅反映 GitHub Actions 状态，不证明科研正确性或视觉质量。
