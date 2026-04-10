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

---

## 这是什么

`dreamlover-skill` 是一个角色 skill 生成器。

它负责把角色资料整理成三层结构：

- `canon.md`：事实层，只保留事实、设定、明确事件、关系
- `persona.md`：行为层，只保留行为模式、互动策略、边界
- `style_examples.md`：表达层，只保留表达风格和短句样例

生成完成后，会把角色安装成一个可直接被 Codex 发现和调用的子 skill：

- 主输出目录：`./.agents/skills/{slug}/`
- 归档镜像：`characters/{slug}/`
- 显式调用：`$slug`
- 检查是否被发现：`/skills`

---

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

生成出的角色子 skill 默认安装到：

```text
./.agents/skills/{slug}/
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

1. 使用 `$dreamlover-skill` 调用生成器
2. 录入角色名、作品名、目标用途
3. 做 source audit
4. 先写 `canon`
5. 再写 `persona`
6. 最后写 `style_examples`
7. 组合成角色子 `SKILL.md`
8. 安装到 `./.agents/skills/{slug}/`
9. 如有需要，同时镜像到 `characters/{slug}/`
10. 生成版本快照

### 4. 使用工具辅助

```bash
python tools/slugify.py "雷电将军"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/version_manager.py --action snapshot --slug raiden-shogun --scope codex
```

### 5. 在 Codex 中直接调用

生成完成后：

1. 在 Codex 中执行 `/skills`
2. 确认看到了对应 slug
3. 直接输入 `$slug` 开始对话

例如：

```text
/skills
$raiden-shogun
$rem
```

---

## 效果示例

仓库内置了一个最小 demo：

- `characters/demo-hero/`

并且角色也可以被安装为真正可调用的子 skill：

- `./.agents/skills/demo-hero/`

生成后的角色 skill 至少包含：

- `SKILL.md`：最终角色入口
- `canon.md`：事实层
- `persona.md`：行为层
- `style_examples.md`：表达层
- `meta.json`
- `sources/normalized.json`
- `versions/`

你可以直接把这个 demo 当作模板，再替换成真实角色。

最小端到端流程是：

1. 生成角色
2. 在 `/skills` 中看到它
3. 使用 `$slug` 开始对话

---

## 功能特性

### 当前能力

- 文本资料归一化
- 来源可信度分层
- `canon / persona / style_examples` 严格拆分
- 角色包生成
- 角色安装到 `./.agents/skills/{slug}/`
- 归档镜像到 `characters/{slug}/`
- 版本快照与回滚基础设施

### 当前不包含

- 图片解析
- 音频解析
- 视频解析
- 自动联网抓取资料
- 高级语义审查器

---

## 项目结构

```text
dreamlover-skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── AGENTS.md
├── .agents/
│   └── skills/
│       └── {slug}/
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
│   └── {slug}/
└── versions/
```

---

## 注意事项

- 资料质量决定还原度
- `canon` 只允许直接支持的内容，不能写推断
- `persona` 只允许行为归纳，不能新增设定
- `style_examples` 只负责表达质感，不负责制造 lore
- Codex 实际发现的是 `./.agents/skills/{slug}/`，不是 `characters/{slug}/`
- 如果 `/skills` 没刷新，重启或刷新 Codex 后再检查
- 这个项目的目标是蒸馏角色，不是复制原文数据库

---

## License

MIT
