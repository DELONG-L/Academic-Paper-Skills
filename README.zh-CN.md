<p align="center">
  <img src="docs/assets/hero-zh-CN.svg" alt="Academic Paper Skills 学术论文技能集——从证据到论文" width="100%">
</p>

<h1 align="center">Academic Paper Skills · 学术论文技能集</h1>
<p align="center">四个协同工作的 Codex 技能，覆盖论文写作、图表、审阅与稿件要求。</p>

<p align="center">
  <a href="https://github.com/DELONG-L/Academic-Paper-Skills/actions/workflows/ci.yml"><img src="https://github.com/DELONG-L/Academic-Paper-Skills/actions/workflows/ci.yml/badge.svg" alt="自动校验状态"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-173F35" alt="MIT 许可"></a>
  <a href="docs/getting-started.zh-CN.md"><img src="https://img.shields.io/badge/tested_with-Python_3.11-526A5D" alt="使用 Python 3.11 测试"></a>
</p>

<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>
<p align="center"><a href="#choose-a-skill">选择技能</a> · <a href="#how-it-works">技能如何协作</a> · <a href="#quick-start">快速开始</a> · <a href="#try-it">使用示例</a> · <a href="docs/architecture.zh-CN.md">仓库指南</a></p>

Academic Paper Skills 帮助研究者使用 Codex 撰写和修订学术论文：组织论证、让主张与证据对应、呈现方法与结果、回复审稿意见，以及核对投稿要求。

这组技能包含可复用的指令、按任务组织的参考指南和辅助工具。提供稿件与来源材料，按当前任务选择技能，逐步形成可以检查和继续修改的产物。四个技能共享指导，使正文、图表、审稿回复与要求检查保持一致。

<a id="choose-a-skill"></a>
## 选择技能

| 当前任务 | 技能 | 典型产物 |
|---|---|---|
| 撰写或修改论文论证 | [paper-writing](paper-writing/SKILL.md) | 基于证据的段落、整合后的引文、与证据匹配的主张 |
| 解释方法或展示结果 | [paper-figures-tables](paper-figures-tables/SKILL.md) | 可编辑示意图、可复现数据图、可用于论文的表格 |
| 检查稿件或回复审稿人 | [paper-review](paper-review/SKILL.md) | 按重要性排序的问题、作者回复、修订闭环核验 |
| 确定稿件适用要求 | [paper-policy](paper-policy/SKILL.md) | 适用要求、源文件检查、依据证据的评估 |

本项目支持作者侧的自审与修订；受邀为他人论文进行正式同行评审不在这组技能的范围内。

<a id="how-it-works"></a>
## 技能如何协作

从当前任务进入即可：修改一个段落、制作一张表格、核验一条审稿意见，或者评估整篇稿件。无需按固定顺序依次运行四个技能。

较完整的修订中，`paper-review` 可以识别论证薄弱点和未解决的审稿问题，`paper-writing` 实施正文修改，`paper-figures-tables` 制作相应的视觉材料；`paper-policy` 在这些工作中确定适用要求并检查来源证据。各技能负责自己的任务范围，并在需要时使用其他技能的指导。

它们遵循三个共同原则：

- **以来源为依据。** 主张、引文、数值和图示机制来自提供或核实的材料，缺失证据应明确呈现。
- **适应具体论文。** 按研究问题、读者、作者偏好与适用的会议要求组织结构和表达。
- **让结果可以核查。** 保留必要的来源和修订证据，区分自动检查、科学判断与人工签核。

按任务查看上表链接的技能指南，了解具体方法、产物约定和详细检查。

<a id="quick-start"></a>
## 快速开始

在 macOS 或 Linux 上**首次安装**时，克隆仓库并将四个技能目录复制到 Codex 的技能目录：

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
cd Academic-Paper-Skills
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_dir"
cp -R paper-policy paper-writing paper-review paper-figures-tables "$skills_dir/"
```

如果这些目录已经存在，请按照[升级说明](docs/getting-started.zh-CN.md#upgrade)保留本地改动并避免遗留文件。安装后新建一个 Codex 任务。

技能指令本身是 Markdown。运行 Python 检查工具时，先创建独立环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-policy.txt
# 使用绘图与图像辅助工具时再安装：
python -m pip install -r requirements-figures.txt
```

建议使用 Python 3.10+；CI 使用 Python 3.11 测试。其他工具按具体任务准备，各工作流的环境要求见[安装、升级与排错指南](docs/getting-started.zh-CN.md)。

<a id="try-it"></a>
## 使用示例

**根据证据修改正文**

```text
使用 $paper-writing 修改这段 Introduction。保留研究问题，依据提供的结果
表述贡献，并指出证据不足的主张。
```

**呈现方法与结果**

```text
使用 $paper-figures-tables 呈现这些实验结果中的比较。
根据研究问题选择图或表，保留不确定性信息，
并提供可编辑或可复现的源文件与图表说明。
```

**核验修订是否闭环**

```text
使用 $paper-review 对照审稿意见和修订稿，指出哪些问题已经解决，
哪些还缺证据，哪些仍需要修改。
```

**检查适用要求**

```text
使用 $paper-policy 依据提供的会议指南检查这份投稿材料。
区分已经验证的源文件检查，以及仍需人工证据支持的判断。
```

<a id="repository-map"></a>
## 仓库结构

```text
Academic-Paper-Skills/
├── paper-writing/          # 正文与论证
├── paper-figures-tables/   # 示意图、数据图与表格
├── paper-review/           # 作者侧审阅与修订
├── paper-policy/           # 稿件要求与证据检查
├── docs/                  # 双语指南与品牌资源
├── scripts/               # 仓库检查与品牌资源生成
└── .github/               # CI 与协作模板
```

每个技能以 `SKILL.md` 为入口，`references/` 存放任务指导，按需提供的 `scripts/` 存放辅助程序，`agents/openai.yaml` 定义展示信息。[仓库指南](docs/architecture.zh-CN.md)说明目录职责与命名约定。

<a id="contributing"></a>
## 参与改进

欢迎纠错、可复现的问题报告和有具体使用场景的工作流改进。请阅读[贡献指南](CONTRIBUTING.zh-CN.md)，通过问题模板描述预期行为与最小示例。修改公开使用说明时，请同步中英文版本。

[变更记录](CHANGELOG.md) · [品牌资源与来源](docs/brand.md) · [第三方说明](THIRD_PARTY_NOTICES.md)

## 许可

采用 [MIT 许可](LICENSE)。本项目独立维护，不代表与 OpenAI 存在隶属或背书关系。工作流致谢与保留的第三方许可见[第三方说明](THIRD_PARTY_NOTICES.md)。
