# dreamlover-skill

> 面向动漫 / 游戏虚拟角色蒸馏的 Agent Skill Meta-Repo
>
> 提供角色设定、剧情摘要、台词摘录、百科整理或你的主观描述，生成一个可持续演化的角色 Skill。
>
> 第一版是 **文本优先**、**分层蒸馏**、**Claude Code 优先兼容** 的 Skill 仓库骨架。

[安装](#安装) · [使用](#使用) · [生成结果](#生成结果) · [项目结构](#项目结构) · [设计原则](#设计原则)

---

## 这是什么

`dreamlover-skill` 不是单个角色 Skill，而是一个 **meta-skill**：

- 输入角色资料
- 区分资料可信度
- 把内容拆成 `canon / persona / style_examples`
- 生成一个新的角色子 Skill
- 支持后续纠错、增量更新和版本快照

它适合这样的目标：

- 想把动漫 / 游戏角色蒸馏成长期可复用的 Agent Skill
- 想明确区分“官方事实”和“行为归纳”
- 想避免把口癖、语气、二创理解和世界观设定混成一团

---

## 核心分层

每个角色 Skill 都由三层组成：

| 层 | 作用 | 允许内容 |
|------|------|------|
| `canon` | 事实层 | 客观事实、明确剧情事件、明确身份关系、明确设定属性、明确官方口径 |
| `persona` | 行为层 | 行为模式、情绪反应倾向、互动方式、关系推进逻辑、禁忌和偏好 |
| `style_examples` | 表达层 | 称呼习惯、句式节奏、语气词、短样例句 |

运行逻辑建议是：

`先读 canon 判断什么是真的 -> 再读 persona 判断 ta 会怎么反应 -> 最后用 style_examples 决定怎么说`

---

## 安装

### Claude Code

Claude Code 会从 Git 仓库中的 `.claude/skills/` 发现 Skill。

```bash
mkdir -p .claude/skills
git clone https://github.com/YOUR_NAME/dreamlover-skill .claude/skills/dreamlover-skill
```

也可以安装到全局：

```bash
git clone https://github.com/YOUR_NAME/dreamlover-skill ~/.claude/skills/dreamlover-skill
```

### Codex

如果你也想在 Codex 环境里使用，可以放到 `$CODEX_HOME/skills/` 下：

```bash
git clone https://github.com/YOUR_NAME/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### 环境要求

- Python 3.9+
- Claude Code 或其他支持 Skill 目录加载的 Agent 环境
- 不需要 GPU
- 不需要本地模型
- 第一版默认只处理文本资料

---

## 使用

### 1. 安装 Skill

把本仓库放进你的 Skill 目录后，让 Agent 读取 [SKILL.md](./SKILL.md)。

### 2. 准备原材料

第一版支持这些文本资料：

- 角色设定整理
- 剧情摘要
- 台词摘录
- wiki / 百科式角色介绍
- 你自己的主观补充说明

### 3. 执行蒸馏流程

推荐流程：

1. 录入角色名、作品名、目标用途
2. 做 source audit，区分资料可信度
3. 先写 `canon`
4. 再写 `persona`
5. 最后写 `style_examples`
6. 组合成角色子 Skill
7. 为结果做版本快照

### 4. 使用工具辅助

本仓库内置了 6 个文本工具：

```bash
python tools/slugify.py "雷电将军"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/version_manager.py --action snapshot --slug raiden-shogun
```

---

## 生成结果

每个角色子 Skill 都会生成到：

```text
characters/{slug}/
├── SKILL.md
├── canon.md
├── persona.md
├── style_examples.md
├── meta.json
├── sources/
│   └── normalized.json
└── versions/
```

其中：

- `canon.md` 是事实层，不允许写推断
- `persona.md` 是归纳层，不允许新增设定
- `style_examples.md` 是表达层，不负责事实判断

---

## 项目结构

```text
dreamlover-skill/
├── SKILL.md
├── AGENTS.md
├── README.md
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
└── versions/
```

---

## 设计原则

### 1. Canon 和 Persona 必须分开

- `canon` 只保留可直接支持的内容
- `persona` 只保留归纳出的行为与互动规律
- 任何会被理解为事实设定的话，都不应该写进 `persona`

### 2. 先事实，后行为，最后语言

不要一上来就模仿口癖。先确保角色“设定没错”，再确保“行为像 ta”，最后才是“说话像 ta”。

### 3. 纠错要落在正确层

- 设定错了，改 `canon`
- 行为不像，改 `persona`
- 语气不对，改 `style_examples`

### 4. 蒸馏优先，不做大段搬运

这个项目的目标是蒸馏角色，不是复制角色原文数据库。

---

## 当前版本的边界

V0.1 当前已经完成：

- 仓库初始化骨架
- prompts / docs / tools 全套第一版
- 基础文本工具链
- 角色目录与版本快照结构

V0.1 当前还没有：

- 图片 / 音频 / 视频解析
- 自动联网抓取资料
- 高级语义审查器
- 大规模角色样例库

---

## 注意事项

- 资料质量会直接决定还原度
- 官方资料、原作剧情、台词摘录的优先级高于百科和主观总结
- 角色 Skill 应该忠于资料，不应为了“更像”而强行补设定
- `style_examples` 只负责表达质感，不负责制造新 lore

---

## License

MIT
