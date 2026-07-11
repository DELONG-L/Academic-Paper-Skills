# Academic Paper Skills

[English](README.md) | 简体中文

Academic Paper Skills 是一组面向学术论文工作流的 Codex skills。仓库包含四个必须保持版本一致的同级 skill：

- `paper-policy`：负责共享 hard/soft 规则解析、确定性 lint、证据支持的合规评估与 readiness 报告。
- `paper-writing`：负责论文正文写作与改写，包括摘要、Introduction、RQ framing、Related Work、方法描述、结果叙事、Discussion、Limitations、Conclusion、贡献列表、claim calibration、引用整合和 academic prose cleanup。
- `paper-figures-tables`：负责论文图表，包括 LaTeX 表格、Related Work 对比表、实验结果表、由源数据驱动的数值图、概念图、caption、artifact spec 和视觉 QA。
- `paper-review`：负责论文审查，包括投稿前 audit、模拟审稿人、red-team review、rebuttal planning、rebuttal drafting、revision verification 和 submission readiness check。

这套 bundle 有意保持窄边界：不包含文献搜索、参考文献自动验证、实验执行或项目管理工作流。

公开默认配置强调可移植性，而不是强制个人写作偏好。默认启用
`integrity-core` 与 `academic-defaults`；格式和结构方面的严格偏好位于
默认关闭的 `strict-house-style` 中。

## 规则集

`paper_context.yaml` 不填写 `policy_sets` 时使用公开默认：

```yaml
policy_sets: [integrity-core, academic-defaults]
```

需要严格格式和结构规范时显式启用：

```yaml
policy_sets: [strict-house-style]
```

严格规则集会自动包含两个公开默认规则集。启用后，其中的 hard 规则仍然
是 hard；可靠的 venue 强制要求仍可覆盖冲突的 house 格式或结构偏好。

## 设计原则

- 论文 claim 必须克制、可追溯、以证据为先。
- 只有启用严格规则集时才强制传统、简洁的大章节命名；公开默认按论文和 venue 调整。
- 用户声明的引用和证据来源是事实依据。
- 不虚构 citation、论文 claim、venue、年份、baseline、metric、p-value 或实验结果。
- 如果系统认为需要某篇文献，但本地 `.bib` 中没有对应条目，只提示用户手动更新 BibTeX。
- 只有启用严格规则时才强制 Related Work 规划对比表；公开默认在确实改善论证时提出。
- 表格应该紧凑、服务论点；`booktabs`、marker、placement 和 resize 规范仅在对应规则启用时强制。
- 数值实验图必须由源数据驱动，用 Python 绘制。
- 概念图工具根据拓扑、可编辑性、venue 与启用规则选择；生成式渲染属于可选 house default。
- Review 与 Writing、Figures/Tables 分离：review 先诊断问题；大段正文改写交给 `paper-writing`，图表制作或重排交给 `paper-figures-tables`。

## 安装

克隆仓库，并把四个 skill 文件夹作为同一版本 bundle 复制到 Codex skills 目录：

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
mkdir -p ~/.codex/skills
cp -R Academic-Paper-Skills/paper-policy ~/.codex/skills/
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
├── paper-policy/
├── paper-writing/
├── paper-figures-tables/
├── paper-review/
├── README.md
├── README.zh-CN.md
├── requirements-policy.txt
├── requirements-figures.txt
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

每个 skill 文件夹都是自包含的，包含自己的 `SKILL.md`、按需加载的 `references/`、可选 `scripts/`，以及 `agents/` 下的 UI metadata。

## 依赖

- 支持本地 skills 的 Codex。
- Python 3.10 或更高版本。
- `paper-policy` 需要 `PyYAML`：`python3 -m pip install -r requirements-policy.txt`。
- 图表辅助脚本的可选依赖：`python3 -m pip install -r requirements-figures.txt`。
- 只有在需要编译或视觉检查论文项目时，才需要 LaTeX 工具链。

## 引用策略

这套 bundle 不做自动文献验证。引用用户或项目声明的 citation/evidence
来源；本地 `.bib` 与用户 notes 是默认来源。如果缺少支持材料，工作流应
输出人工更新提示，而不是伪造参考文献。

## License

MIT。见 [LICENSE](LICENSE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
