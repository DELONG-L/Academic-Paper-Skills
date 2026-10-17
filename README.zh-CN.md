# Academic Paper Skills

四个协同工作的 Codex 技能，支持论文写作、图表制作、稿件审阅与修订，以及论文要求核对。

**[选择技能](#choose-a-skill)** · [开始使用](#quick-start) · [使用指南](docs/getting-started.zh-CN.md) · [English](README.md)

<a href="#choose-a-skill"><img src="docs/assets/readme-cover-zh.png" alt="学术论文技能集：围绕稿件与证据，按需选用论文写作、论文图表、作者侧审阅和论文要求四个技能。" width="1942"></a>

[![自动校验](https://github.com/DELONG-L/Academic-Paper-Skills/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DELONG-L/Academic-Paper-Skills/actions/workflows/ci.yml) [![MIT 许可](https://img.shields.io/badge/license-MIT-173F35)](LICENSE) [![使用 Python 3.11 测试](https://img.shields.io/badge/tested_with-Python_3.11-526A5D)](docs/getting-started.zh-CN.md)

<a id="choose-a-skill"></a>
## 你现在要完成什么？

提供稿件、来源材料或实验结果，按当前任务选择技能。可以只改一个段落、制作一张图，也可以处理一次修回或整篇论文。

- [**论文写作**](paper-writing/SKILL.md)：清楚的论证、以证据为基础的段落，以及整合后的引用。
- [**论文图表**](paper-figures-tables/SKILL.md)：可编辑示意图、可复现数据图，以及适合论文内容的表格。
- [**作者侧审阅**](paper-review/SKILL.md)：按重要性排序的问题、审稿回复，以及对照审稿意见核验后的修订。
- [**论文要求**](paper-policy/SKILL.md)：适用的项目或投稿要求、来源检查，以及仍缺少的证据。

作者侧审阅用于自己的稿件和审稿回复。受邀为他人论文进行正式同行评审时，使用独立的评审流程。

<a id="quick-start"></a>
## 开始使用

在 macOS 或 Linux 上**首次安装**时，将四个技能目录复制到 Codex 的技能目录。保留它们的名称并放在同一层级，以便相互引用。

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
cd Academic-Paper-Skills
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_dir"
cp -R paper-policy paper-writing paper-review paper-figures-tables "$skills_dir/"
```

如果这些目录已经存在，请按照[升级指南](docs/getting-started.zh-CN.md#upgrade)保留本地改动。安装后新建一个 Codex 任务，提供来源材料，再调用对应技能。

<details>
<summary><strong>运行 Python 检查或绘图工具</strong></summary>

技能指令本身是 Markdown。配套 Python 工具使用独立环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-policy.txt
# 使用绘图与图像辅助工具时再安装：
python -m pip install -r requirements-figures.txt
```

建议使用 Python 3.10+；CI 使用 Python 3.11 测试。图像生成与 LaTeX 编译需要相应工具，具体要求见[环境配置与排错指南](docs/getting-started.zh-CN.md)。

</details>

<a id="try-it"></a>
## 试一个具体任务

**根据证据修改正文** · `paper-writing`

```text
使用 $paper-writing 修改这段引言。
保留研究问题，依据提供的结果表述贡献，
并指出证据不足的主张。
```

<details>
<summary><strong>制作一张图或表</strong> · paper-figures-tables</summary>

```text
使用 $paper-figures-tables
呈现这些实验结果中的比较。
根据研究问题选择图或表，保留不确定性，
并提供可编辑或可复现的源文件，
以及图表说明。
```

</details>

<details>
<summary><strong>核验稿件修订</strong> · paper-review</summary>

```text
使用 $paper-review
对照审稿意见和修订稿。
指出哪些问题已经解决，哪些还缺证据，
哪些仍需要修改。
```

</details>

<details>
<summary><strong>核对论文要求</strong> · paper-policy</summary>

```text
使用 $paper-policy 检查这份材料。
依据提供的投稿指南，核对适用要求。
区分已经验证的源文件检查，
以及仍需人工证据支持的判断。
```

</details>

<a id="how-it-works"></a>
## 共用证据，各有分工

四个技能无需按固定顺序使用。修回论文时，`paper-review` 可以定位论证问题，`paper-writing` 修改正文，`paper-figures-tables` 制作支撑论证的图表；需要确定适用要求及其依据时，再调用 `paper-policy`。

它们遵循三个共同原则：**以来源为依据**、**适应具体论文**、**让结果可以核查**。保留主张强度与不确定性，按需提供可编辑或可复现的源文件，并区分自动检查、科学判断与人工确认。

<a id="repository-map"></a>
<a id="contributing"></a>
## 指南与参与改进

[安装与升级](docs/getting-started.zh-CN.md) · [仓库指南](docs/architecture.zh-CN.md) · [参与贡献](CONTRIBUTING.zh-CN.md) · [更新记录](CHANGELOG.md) · [视觉资源](docs/brand.md)

欢迎纠错和有具体使用场景的工作流改进。请使用 Issue 模板说明预期行为，并提供最小示例。修改公开说明时，请同步中英文版本。

## 许可

项目采用 [MIT](LICENSE) 许可，独立维护，不表示与 OpenAI 存在隶属或背书关系。致谢与保留的第三方声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
