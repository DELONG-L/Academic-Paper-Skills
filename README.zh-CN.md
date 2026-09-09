# Academic Paper Skills

[English](README.md) | 简体中文

面向严谨学术写作的四个协作技能：

| 技能 | 职责 |
|---|---|
| `paper-writing` | 修改正文、整合已核实引文、校准论断，减少模板化与过度防御性写作，制作审阅节选，迁移 LaTeX 模板。 |
| `paper-review` | 审查作者论文的论证与段落结构，模拟审稿疑问，撰写作者回复，核验修改是否完成。 |
| `paper-figures-tables` | 制作有来源的表格、可复现的数值图和忠实的概念图，检查最终尺寸下的实际输出。 |
| `paper-policy` | 解析适用规则，以真实证据进行正式合规评估。 |

受邀承担的正式同行评审、实验执行和项目管理由独立工作流负责。
本套技能支持写作或审阅任务授权范围内的引文核验与补全，不承担文献库管理。

## 统一工作流

本地与公开安装使用相同的两个策略集：

```yaml
policy_sets: [integrity-core, academic-defaults]
```

省略 `policy_sets` 即使用上述默认值，不再设置独立的
`strict-house-style` 模式。注册表包含 50 条硬规则与 49 条软偏好。
硬规则按声明的范围和条件生效，约束学术诚信、证据与适用要求。
标题、段落形状、比较表、字体、源画布比例和绘图工具等偏好可随论文调整；
调整偏好不会阻断提交准备状态。

- 直接陈述有证据支持的结论。保留实质负面结果与必要条件，删除重复的预先辩护。
- 需要结构修改时，先检查论证顺序和段落功能，再润色句子；不强制统一段落模板。
- 诊断具体文字问题，不通过文风判断 AI 作者身份，不优化检测器分数。
- 遵守封闭语料与保密约束。公开引文补全请求允许必要的一手来源核验和有依据的
  参考文献更新；无法获取的来源保持待核实。
- 跨技能继续完成已授权修改。普通文字和图表任务不需要完整合规运行或空白台账。
- 数值图来自已有数据或明确提供的数值，并具有可复现的生成过程。
  工具和导出格式服从内容与实际交付要求，最终导出须按论文放置尺寸检查。

## 安装

四个同级目录须保持同一版本。首次安装：

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
mkdir -p ~/.codex/skills
cp -R Academic-Paper-Skills/paper-policy ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-writing ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-review ~/.codex/skills/
cp -R Academic-Paper-Skills/paper-figures-tables ~/.codex/skills/
```

升级时先备份并完整替换已有的四个目录，再复制新版本；直接合并目录可能留下已退役的
规则或参考文件。如有自行定制内容，保存在备份中供检查。安装后新建 Codex 任务，
使技能列表刷新。

建议 Python 3.10+。策略工具依赖 PyYAML，图表工具使用可选绘图依赖。
源码编译与视觉检查需要 LaTeX、PDF 渲染工具；纯文字写作不需要。

```bash
python3 -m pip install -r requirements-policy.txt
python3 -m pip install -r requirements-figures.txt
```

## 使用示例

```text
使用 $paper-writing 根据给定数值修改 Results 段落，保持结论直接，删除重复的预先辩护。
```

```text
使用 $paper-review 检查段落必要性、论证顺序和跨段重复。
说明需要修改和可以保留的部分，并给出具体替换文本。
```

```text
使用 $paper-figures-tables 将这些测量值绘成图，并检查最终导出。
```

```text
使用 $paper-review 回复这些审稿意见，并逐条核验承诺的修改。
```

明确的提交准备评估使用项目上下文和证据记录。缺少语义或人工检查证据时保持
`UNVERIFIED`。Agent 的语义 PASS 必须绑定当前来源快照，Agent 检查不能替代规则
要求的人工评估。确定性失败具有优先级。`review_hint` 表示需要检查的线索，既不等于
违规，也不构成通过证据。

命令和权限模型见 [策略入口](paper-policy/SKILL.md) 与
[证据契约](paper-policy/references/compliance-schema.md)。
编辑完成和论文达到提交要求是两种不同判断。

## 维护与验证

```bash
python3 paper-policy/scripts/validate_registry.py
python3 paper-policy/scripts/audit_skill_integration.py .
python3 -m unittest discover -s paper-policy/scripts -p 'test_*.py'
python3 -m unittest discover -s paper-figures-tables/scripts -p 'test_*.py'
```

CI 执行这些检查并编译 Python 辅助脚本。整合检查覆盖明确引用与规则 ID，不能证明
语义一致性或论文质量。维护时应同时检查注册表措辞、任务指南、示例和检查器的实际行为。
参见 [规则维护](paper-policy/references/rule-maintenance.md) 和 [更新说明](CHANGELOG.md)。

## 来源与许可

工作流参考了 [OniReimu/claude-scholar](https://github.com/OniReimu/claude-scholar)
中的论证架构、段落审查、引文核验、修改收尾和文字诊断等思路，并独立编写适配指南。
相关参考文件标注了具体来源。图表工具保留 `Haojae/scipilot-figure-skill` 的来源说明。

MIT，详见 [LICENSE](LICENSE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
