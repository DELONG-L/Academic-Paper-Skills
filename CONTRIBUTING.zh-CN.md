# 参与改进

[English](CONTRIBUTING.md) · 简体中文 · [首页](README.zh-CN.md)

改动应服务于具体科研写作任务，保留来源追溯，并区分自动检查与科学判断。

## 提出范围清晰的修改

可复现错误使用问题报告，新增行为使用工作流提议。说明用户任务、现有限制和一个简短示例。公开报告应移除保密材料；合成复现样例应明确标注。

在负责该任务的技能内修改。详细指导放在 `references/` 并从入口引用，不要把内容重复塞入所有技能。不要从某篇论文或某个会议推导通用要求。详见[仓库与命名指南](docs/architecture.zh-CN.md)。

## 本地验证

在仓库根目录，激活已经安装两组依赖的环境，执行：

```bash
python scripts/check_repository.py
python -m unittest discover -s scripts -p 'test_*.py'
python paper-policy/scripts/validate_registry.py
python paper-policy/scripts/audit_skill_integration.py .
python -m py_compile scripts/*.py paper-policy/scripts/*.py paper-figures-tables/scripts/*.py paper-review/scripts/*.py
python -m unittest discover -s paper-policy/scripts -p 'test_*.py'
python -m unittest discover -s paper-figures-tables/scripts -p 'test_*.py'
```

修改可执行行为时添加行为测试。仅修改文档时，检查路由、相对链接、命名以及指令是否会产生预期行动。视觉修改必须检查实际渲染；XML 合法不代表视觉正确。品牌 SVG 使用 `python scripts/build_brand.py` 重建，来源见[品牌说明](docs/brand.md)。

## 保持文档一致

公开行为发生变化时，同步中英文首页和对应指南。两种语言中的技能标识与命令路径保持一致。共享技术参考默认保留英文，只有在维护责任明确时才增加翻译，避免形成不完整的双份技能目录。

拉取请求中说明问题、修改后的行为、验证和剩余限制。面向用户的变化在 `CHANGELOG.md` 的 `Unreleased` 下简要记录。保留第三方声明；不要提交私密稿件、参考论文原始截图、凭证或本地验证输出。
