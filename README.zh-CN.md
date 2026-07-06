# Academic Paper Skills

[English](README.md) | 简体中文

Academic Paper Skills 是一组面向学术论文工作流的 Codex skills。仓库只包含三个主 skill：

- `paper-writing`：负责论文正文写作与改写，包括摘要、Introduction、RQ framing、Related Work、方法描述、结果叙事、Discussion、Limitations、Conclusion、贡献列表、claim calibration、引用整合和 academic prose cleanup。
- `paper-figures-tables`：负责论文图表，包括 LaTeX 表格、Related Work 对比表、实验结果表、由源数据驱动的数值图、概念图、caption、artifact spec 和视觉 QA。
- `paper-review`：负责论文审查，包括投稿前 audit、模拟审稿人、red-team review、rebuttal planning、rebuttal drafting、revision verification 和 submission readiness check。

这套 bundle 有意保持窄边界：不包含文献搜索、参考文献自动验证、实验执行或项目管理工作流。

## 设计原则

- 论文 claim 必须克制、可追溯、以证据为先。
- 大章节命名必须传统、简洁。
- 本地 `.bib` 和用户提供的 notes 是引用来源的唯一事实依据。
- 不虚构 citation、论文 claim、venue、年份、baseline、metric、p-value 或实验结果。
- 如果系统认为需要某篇文献，但本地 `.bib` 中没有对应条目，只提示用户手动更新 BibTeX。
- Related Work 默认必须规划对比表，除非用户明确豁免或 venue 禁止表格。
- 表格应该紧凑、服务论点，而不是塞满所有维度；默认使用 `booktabs`，并使用 `resizebox` 对齐目标栏宽，除非自然宽度已经足够美观。
- 数值实验图必须由源数据驱动，用 Python 绘制。
- 非数据类概念图默认使用生成式图像模型；对于 Figure 1、system overview、pipeline、architecture、threat model，先制作可编辑的 `structure.svg` 作为结构参考。
- Review 与 Writing、Figures/Tables 分离：review 先诊断问题；大段正文改写交给 `paper-writing`，图表制作或重排交给 `paper-figures-tables`。

## 安装

克隆仓库，并把三个 skill 文件夹复制到 Codex skills 目录：

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
mkdir -p ~/.codex/skills
cp -R Academic-Paper-Skills/paper-writing ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-figures-tables ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-review ~/.codex/skills/
```

安装后建议开启一个新的 Codex thread，让 skills 列表刷新。

## 使用示例

```text
Use $paper-writing to rewrite this introduction with clearer RQs and scoped claims.
```

```text
Use $paper-figures-tables to turn this related-work table spec into compact LaTeX.
```

```text
Use $paper-review to audit this manuscript before submission and produce a prioritized issue board.
```

## 目录结构

```text
Academic-Paper-Skills/
├── paper-writing/
├── paper-figures-tables/
├── paper-review/
├── README.md
├── README.zh-CN.md
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

每个 skill 文件夹都是自包含的，包含自己的 `SKILL.md`、按需加载的 `references/`、可选 `scripts/`，以及 `agents/` 下的 UI metadata。

## 依赖

- 支持本地 skills 的 Codex。
- Python 3，用于 figures/tables 相关辅助脚本。
- 根据具体任务，可能需要安装 `matplotlib`、`numpy`、`pandas`、`seaborn`、`Pillow`、`pypdf`。
- 只有在需要编译或视觉检查论文项目时，才需要 LaTeX 工具链。

## 引用策略

这套 bundle 不做自动文献验证。如果草稿中需要某个 citation，但本地 `.bib` 或用户 notes 中没有对应依据，工作流应该输出“请手动更新 BibTeX”的提示，而不是伪造参考文献。

## License

MIT。见 [LICENSE](LICENSE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
