# dreamlover-skill

> *"搞出来大模型的简直是码神，使用 AI 编码创造了雷电将军，还要创造玛奇玛，创造喜多川海梦，创造薇尔莉特，创造蕾姆，创造霞之丘诗羽，创造中野二乃，创造樱岛麻衣，最后创造一个只有老婆的完美世界。"*
>
> 把动漫 / 游戏虚拟角色的原材料蒸馏成一个真正能长期使用、并且能直接被 Codex 调用的 Agent Skill。
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
> [![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
> [![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)
>
> 仓库地址：[tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)
>
> [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [项目结构](#项目结构) · [注意事项](#注意事项) · [English](README_EN.md)

---

## 这是什么

`dreamlover-skill` 是一个“生成器 skill”。

它负责把角色资料整理成三层：

- `canon.md`：只保留事实、设定、明确事件、关系
- `persona.md`：只保留行为模式、互动策略、边界
- `style_examples.md`：只保留表达风格和短句样例

生成完成后，会把角色安装成一个可直接被 Codex 发现和调用的“子 skill”：

- 主输出目录：`./.agents/skills/{slug}/`
- 归档镜像：`characters/{slug}/`
- 显式调用：`$slug`
- 检查是否被发现：`/skills`

---

## 安装

### Claude Code

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill
```

### Codex

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### 环境要求

- Python 3.9+
- 支持 Skill 目录加载的 Agent 环境
- 第一版只处理文本资料

---

## 使用

### 1. intake 先行

当你只说：

```text
$dreamlover-skill
帮我创建雷姆这个角色 skill
```

生成器不应该直接乱写，而应该先进入 intake，至少问你：

- 角色名
- 作品名
- 目标用途
- 资料类型：官方设定 / 剧情摘要 / 台词摘录 / wiki / 用户描述
- 是否允许基于不足资料做低置信度 persona 归纳

只有 intake 补齐之后，才继续生成。

### 2. 生成角色 skill

推荐流程：

1. 使用 `$dreamlover-skill`
2. 回答 intake 提问
3. 做 source audit
4. 先写 `canon`
5. 再写 `persona`
6. 最后写 `style_examples`
7. 组合成角色子 `SKILL.md`
8. 安装到 `./.agents/skills/{slug}/`
9. 如有需要，同时镜像到 `characters/{slug}/`
10. 生成版本快照

### 3. 使用工具辅助

```bash
python tools/slugify.py "雷电将军"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/skill_linter.py --slug raiden-shogun --scope codex
python tools/version_manager.py --action snapshot --slug raiden-shogun --scope codex
```

`skill_writer.py --interactive` 会逐项提问，并把 intake 信息写入：

- `canon.md`
- `persona.md`
- `style_examples.md`
- `sources/normalized.json`
- 子 `SKILL.md`

### 4. 在 Codex 中直接调用

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

### 5. 最小端到端示例

```text
$dreamlover-skill
帮我创建雷姆这个角色 skill
```

接下来先回答几轮 intake，例如：

```text
角色名：雷姆
作品名：Re:从零开始的异世界生活
目标用途：日常角色对话
资料类型：wiki,用户描述
允许低置信度 persona：是
```

生成后：

```text
/skills
$rem
```

这样就能直接按角色口吻开始对话。

---

## 效果示例

仓库内置了一个最小 demo：

- `characters/demo-hero/`
- `./.agents/skills/demo-hero/`

生成后的角色 skill 至少包含：

- `SKILL.md`
- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`

最小端到端流程就是：

1. 生成角色
2. 在 `/skills` 里看到它
3. 使用 `$slug` 开始对话

---

## 功能特性

### 当前能力

- 文本资料归一化
- 来源可信度分层
- `canon / persona / style_examples` 严格拆分
- intake-first 生成流程
- CLI 交互式创建：`python tools/skill_writer.py --action create --interactive`
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
├── prompts/
├── tools/
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
