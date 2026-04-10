# dreamlover-skill

> *"搞出来大模型的简直是码神，使用 AI 编码创造了雷电将军，还要创造玛奇玛，创造喜多川海梦，创造薇尔莉特，创造蕾姆，创造霞之丘诗羽，创造中野二乃，创造樱岛麻衣，最后创造一个只有美少女的完美世界。"*
>
> 把动漫 / 游戏虚拟角色的原材料蒸馏成一个真正能长期使用的 Agent Skill。
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
> [![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
> [![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)
>
> 提供角色设定、剧情摘要、台词摘录、百科整理，或者你的主观描述，生成一个可持续演化的角色 Skill。
>
> 仓库地址：[tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)
>
> [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [项目结构](#项目结构) · [注意事项](#注意事项) · [English](README_EN.md)
## 安装

### Claude Code

Claude Code 会从 Skill 目录中发现本仓库。

```bash
# 安装到全局
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill

# 或安装到当前项目
git clone https://github.com/tobemorelucky/dreamlover-skill .claude/skills/dreamlover-skill
```

### Codex

如果你也想在 Codex 环境中使用：

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### 环境要求

- Python 3.9+
- 支持 Skill 目录加载的 Agent 环境
- 第一版仅处理文本资料
- 不需要 GPU，不需要本地模型，不需要 Docker

---

## 使用

### 1. 准备原材料

第一版支持：

- 官方角色设定
- 剧情摘要
- 台词摘录
- wiki / 百科式介绍
- 用户自己的补充描述

### 2. 做来源审计

推荐按照以下优先级处理：

1. 官方资料
2. 原作剧情 / 台词摘录
3. 社区 wiki / 百科整理
4. 用户主观总结

### 3. 生成角色 Skill

推荐流程：

1. 录入角色名、作品名、目标用途
2. 做 source audit
3. 先写 `canon`
4. 再写 `persona`
5. 最后写 `style_examples`
6. 组合成角色子 `SKILL.md`
7. 生成版本快照

### 4. 使用工具辅助

```bash
python tools/slugify.py "雷电将军"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/version_manager.py --action snapshot --slug raiden-shogun
```

---

## 效果示例

仓库内置了一个最小 demo：

- `characters/demo-hero/`

它包含：

- `canon.md`：事实层示例
- `persona.md`：行为层示例
- `style_examples.md`：表达层示例
- `SKILL.md`：最终角色入口
- `sources/normalized.json`：示例输入资料
- `versions/`：快照记录

你可以直接把这个 demo 当作模板，再替换成真实角色。

---

## 功能特性

### 当前能力

- 文本资料归一化
- 来源可信度分层
- `canon / persona / style_examples` 严格拆分
- 角色包生成
- 版本快照与回滚基础设施

---

## 项目结构

```text
dreamlover-skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── AGENTS.md
├── docs/
│   ├── PRD.md
│   ├── evidence-model.md
│   ├── canon-persona-boundary.md
│   ├── safety.md
│   ├── input-contract.md
│   └── output-contract.md
├── prompts/
│   ├── intake.md
│   ├── source_audit.md
│   ├── canon_builder.md
│   ├── persona_builder.md
│   ├── style_examples_builder.md
│   ├── skill_composer.md
│   ├── correction_handler.md
│   └── evolution_merge.md
├── tools/
│   ├── slugify.py
│   ├── source_normalizer.py
│   ├── evidence_indexer.py
│   ├── style_extractor.py
│   ├── skill_writer.py
│   └── version_manager.py
├── characters/
│   └── demo-hero/
└── versions/
```

---

## 注意事项

- 资料质量决定还原度
- `canon` 只允许直接支持的内容，不能写推断
- `persona` 只允许行为归纳，不能新增设定
- `style_examples` 只负责表达质感，不负责制造 lore
- 这个项目的目标是蒸馏角色，不是复制原文数据库

---
