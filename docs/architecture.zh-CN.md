# 仓库结构与命名

[English](architecture.md) · 简体中文 · [首页](../README.zh-CN.md)

## 稳定的技能边界

四个顶层 `paper-*` 目录是可分别发现、一起安装的技能。相邻目录路径是技能协作约定的一部分；将它们整体移到新的嵌套目录会破坏已有引用与安装方式。

| 目录 | 负责内容 | 转交范围 |
|---|---|---|
| `paper-writing/` | 正文、证据整合、段落修改 | 最终图表转交图表技能；批评与回复转交审阅技能。 |
| `paper-figures-tables/` | 表格、数据图、概念图、图注与图表检查 | 正文转交写作；正式要求通过规则技能确定。 |
| `paper-review/` | 作者侧自审、回复审稿人、修订核验 | 正文修改由写作技能实施，最终图表由图表技能制作。 |
| `paper-policy/` | 要求注册表、适用条件、源文件检查、证据评估 | 展示偏好保留在任务指南中，不升级为通用硬性规则。 |

每个技能以 `SKILL.md` 定义范围与路由，`references/` 按需提供详细指导，`agents/openai.yaml` 定义展示信息，仅在可执行工具确有价值时添加 `scripts/`。测试与对应程序放在一起，测试样例归属于相应程序的测试集。仅提供文字指导的技能无需空置的脚本目录。

## 仓库级内容

- `README.md` 与 `README.zh-CN.md`：内容对应、面向使用者的入口。
- `docs/`：安装、结构指南，以及品牌来源和资源。
- `docs/assets/`：可编辑 SVG、生成的设计参考图及其提示词。
- `scripts/`：仓库级检查与确定性的品牌源文件生成。
- `.github/`：CI、问题表单与拉取请求模板。
- `requirements-policy.txt` 与 `requirements-figures.txt`：分开的依赖组，保留已有文件名。
- `CONTRIBUTING.md` 与中文对应版本：参与改进的工作流程。
- `CHANGELOG.md`、`LICENSE`、`THIRD_PARTY_NOTICES.md`：变更与来源记录。

## 命名约定

| 对象 | 约定 | 示例 |
|---|---|---|
| 技能目录与前置元数据中的名称 | 相同的小写连字符标识 | `paper-figures-tables` |
| 参考文档 | 描述性名称，用连字符分隔 | `conceptual-vector-rebuild.md` |
| Python 模块与测试 | 可导入的下划线命名，测试以 `test_` 开头 | `check_artifacts.py`、`test_check_artifacts.py` |
| 双语文档 | 英文使用基础文件名，中文增加 `.zh-CN.md` | `getting-started.md`、`getting-started.zh-CN.md` |
| 本地化视觉资源 | 基础名称加语言代码 | `hero-en.svg`、`hero-zh-CN.svg` |
| 必需或约定俗成的文件 | 保留标准名称 | `SKILL.md`、`README.md`、`LICENSE`、`openai.yaml` |

项目名称统一为 **Academic Paper Skills**，中文描述名为 **学术论文技能集**。命令与路径使用现有技能标识。保留仓库地址，不为形式上的整齐而改名。

## 验证边界

`python scripts/check_repository.py` 检查公开文档的链接与锚点、双语互链、技能标识与展示信息，以及 SVG 是否安全且自包含。CI 还会校验规则注册表、检查跨技能引用、编译辅助程序并执行已有测试。

这些检查验证结构一致性与已测试行为，不能证明视觉质量、科学结论、ImageGen 端到端可靠性或投稿准备状态。视觉改动与实际稿件中的图表仍需单独检查。
