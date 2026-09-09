# Academic Paper Skills

[English](README.md) | 简体中文

一套协同工作的 Codex 技能，支持严谨的学术写作、论文审阅与出版级图表制作。

| 技能 | 用途 |
|---|---|
| [paper-writing](paper-writing/SKILL.md) | 撰写和修改正文、强化论证、整合引文。 |
| [paper-review](paper-review/SKILL.md) | 审阅作者论文、起草审稿回复、核验修改。 |
| [paper-figures-tables](paper-figures-tables/SKILL.md) | 制作表格、可复现的数据图和概念图。 |
| [paper-policy](paper-policy/SKILL.md) | 应用论文要求，依据证据评估提交准备状态。 |

工作流以证据为基础，并根据论文、作者与投稿场所调整结构和表达。

## 安装

四个技能一起安装：

```bash
git clone https://github.com/DELONG-L/Academic-Paper-Skills.git
cd Academic-Paper-Skills
mkdir -p ~/.codex/skills
cp -R paper-policy paper-writing paper-review paper-figures-tables ~/.codex/skills/
python3 -m pip install -r requirements-policy.txt
```

建议使用 Python 3.10+。使用绘图工具时另行安装 `requirements-figures.txt` 中的依赖；编译论文需要 LaTeX 环境。

升级时先备份，再完整替换已有的四个技能目录。安装后新建 Codex 任务。

## 使用

提供论文、数据或审稿意见，并指定所需技能：

```text
使用 $paper-writing 修改这段 Introduction，让贡献表述更清楚。
```

```text
使用 $paper-review 检查论文的论证结构，并给出具体修改建议。
```

详细工作流与工具说明见上表链接的各技能指南。

## 许可与致谢

本项目使用 MIT 许可，详见 [LICENSE](LICENSE)。

工作流参考与第三方来源记录在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)，包括对 [claude-scholar](https://github.com/OniReimu/claude-scholar) 和 [scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) 的致谢。
