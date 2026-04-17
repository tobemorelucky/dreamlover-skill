# dreamlover-skill

> “搞出来大模型的简直是码神，使用 AI 编码解放了前端兄弟，还要解放后端兄弟，测试兄弟，运维兄弟，解放网安兄弟，解放 ic 兄弟，最后解放自己解放全人类（本 skill 几乎完全由 Codex 生成）”

把动漫 / 游戏虚拟角色资料蒸馏成一套共享静态角色内容，然后自动生成适配 Codex 的主安装包，并按需导出 OpenClaw 版本。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)

仓库地址：[tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)

[English](README_EN.md)

## 这是什么

`dreamlover-skill` 是顶层生成器 skill，不是最终拿来聊天的角色本体。

它会先生成唯一的 canonical source：

- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`

这套静态角色内容保存在：

- `characters/{slug}/`

然后基于同一套静态内容生成平台包装层：

- Codex 主安装：`./.agents/skills/{slug}/`
- OpenClaw 可选导出：`<openclaw_workspace>/.agents/skills/{slug}/`

静态角色内容在两个平台之间保持一致，差异只体现在：

- `SKILL.md`
- 必要的 `runtime/` 脚本打包方式

## 当前主流程

默认以 Codex 为主安装目标：

1. 先生成 canonical source 到 `characters/{slug}/`
2. 默认安装 Codex 版本到 `./.agents/skills/{slug}/`
3. 生成完成后再问是否导出 OpenClaw
4. 如果用户确认导出，再询问 OpenClaw workspace 路径
5. 导出到 `<openclaw_workspace>/.agents/skills/{slug}/`

不建议把 Codex 安装目录和 OpenClaw 导出目录当成两个可编辑源。角色有变更时，应回到 canonical source 重新导出覆盖。

## 三层拆分

- `canon.md`：只保留事实、设定、明确事件、关系
- `persona.md`：只保留行为模式、互动策略、边界
- `style_examples.md`：只保留表达风格和短句样例

## 条件触发式记忆

生成出的子角色 skill 保留条件触发式记忆，但运行时记忆不是角色静态内容的一部分。

- 运行时数据库路径：`<workspace>/.dreamlover-data/memory.sqlite3`
- 不会把 `.dreamlover-data/` 复制进 skill 目录
- 普通闲聊默认不读也不写记忆
- 只有命中条件时才调用 `runtime/memory_prepare.py`
- 只有需要写入时才调用 `runtime/memory_commit.py`
- 只有达到阈值时才调用 `runtime/memory_summarize.py`

如果 `python3` 不可用，子 skill 会自动退化为无记忆模式，而不是整个角色失效。

## 使用

### 用顶层生成器创建角色

```text
$dreamlover-skill
帮我创建雷姆这个角色 skill
```

预期行为：

1. 先进入 intake gate
2. 生成草稿摘要并让用户确认
3. 先写 canonical source
4. 默认安装 Codex 版本
5. 再询问是否导出 OpenClaw

### CLI 生成

```bash
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug rem --name "Rem"
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /path/to/openclaw-workspace
```

## Codex 使用方式

生成后，Codex 主安装目录应为：

```text
./.agents/skills/rem/
```

然后在 Codex 中验证：

```text
/skills
$rem
```

## OpenClaw 使用方式

如果用户选择导出，OpenClaw 目录应为：

```text
<openclaw_workspace>/.agents/skills/rem/
```

然后在 OpenClaw 中：

- 刷新 skills 或新建会话
- 让 OpenClaw 从 workspace 自动发现该角色 skill
- 通过普通对话触发角色扮演

OpenClaw 版本共享同一套静态角色内容，但使用独立的 OpenClaw wrapper `SKILL.md`。

## 路径与导出说明

为避免路径问题，导出的 OpenClaw 版本不会依赖硬编码的 home 目录。

当前设计是：

- 角色静态文件直接放在 `<openclaw_workspace>/.agents/skills/{slug}/`
- 运行脚本放在 `<openclaw_workspace>/.agents/skills/{slug}/runtime/`
- wrapper 使用相对路径调用本地 `runtime/` 脚本
- wrapper 使用相对路径把记忆数据写到 `<workspace>/.dreamlover-data/`

因此：

- 不需要把仓库根目录复制到 OpenClaw workspace
- 不会因为用户机器的 home 路径不同而失效
- 不会把运行时记忆数据库错误地打进 skill 包

## 本地验证

### 验证 Codex 主安装

```bash
python tools/skill_writer.py --action create --interactive
```

预期：

- `characters/{slug}/` 生成 canonical source
- `./.agents/skills/{slug}/` 生成 Codex 包装层

### 验证 OpenClaw 导出

```bash
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /tmp/openclaw-demo
```

预期：

- `/tmp/openclaw-demo/.agents/skills/rem/` 存在
- `canon.md` / `persona.md` / `style_examples.md` / `meta.json` 与 Codex 版本一致
- 只有 `SKILL.md` 和 `runtime/` 属于平台差异层

### 验证记忆门控

```bash
python scripts/memory_prepare.py --character-slug rem --user-message "今天天气不错"
python scripts/memory_prepare.py --character-slug rem --user-message "你还记得我上次说过什么吗"
python scripts/memory_prepare.py --character-slug rem --user-message "以后叫我阿昭"
```

预期：

- 普通闲聊：不读、不写
- 明确追问历史：触发读取
- 稳定称呼偏好：回复后触发写入

## 注意事项

- canonical source 才是唯一建议编辑的角色源
- 不建议手改导出的 Codex / OpenClaw 目录
- 角色有变更时，请重新生成或重新导出
- 当前版本仍以文本资料为主，不处理图片、音频、视频

## License

MIT
