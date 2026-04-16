# dreamlover-skill

> Distill anime and game character materials into a generator skill that produces OpenClaw-ready child role skills.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)

Repo: [tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)

## What This Repo Contains

`dreamlover-skill` is the generator skill.

It turns source material into:

- `canon.md`: facts, setting, explicit events, relationships
- `persona.md`: behavior patterns, interaction strategy, boundaries
- `style_examples.md`: wording texture and short example lines

The generated child character skill is the runtime skill.

- install path: `<workspace>/.agents/skills/{slug}/`
- archive mirror: `characters/{slug}/`
- OpenClaw loads the child skill from the workspace skill directory

## Generator Vs Child Skill

- top-level `dreamlover-skill`: asks intake questions and generates the character package
- child `SKILL.md`: the actual role skill that OpenClaw loads and uses in conversation

## OpenClaw Child Skill Output

Each generated child package contains:

- `SKILL.md`
- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`

The child `SKILL.md` is written with OpenClaw-oriented front matter:

```yaml
---
name: rem
description: OpenClaw-compatible role skill for Rem. Answer in Rem's voice using canon, persona, style examples, and conditional memory gates.
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}}
metadata.openclaw.requires.bins: ["python3"]
---
```

## Conditional Memory

Generated child skills keep the conditional memory system.

- default: do not read memory
- default: do not write memory
- pre-reply: run `scripts/memory_router.py`
- only if `should_read: true`: run `scripts/memory_fetch.py`
- generate the reply
- post-reply: run `scripts/memory_router.py`
- only if `should_write: true`: run `scripts/memory_commit.py`
- only if `should_summarize: true`: run `scripts/memory_summarize.py`

Local memory lives inside the workspace:

- `<workspace>/.dreamlover-data/memory.sqlite3`

If `python3` is unavailable, the child skill should fall back to no-memory mode instead of failing completely.

## Usage

### 1. Generate A Character Skill

Use the top-level generator skill first:

```text
$dreamlover-skill
Help me create a Rem character skill
```

The generator should ask intake questions before writing anything.

### 2. CLI Generation

```bash
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug rem --name "Rem"
```

### 3. OpenClaw Runtime Use

After generation, the child skill should be located at:

```text
<workspace>/.agents/skills/rem/
```

OpenClaw usage:

1. Put the child skill in `<workspace>/.agents/skills/{slug}/`
2. Start a new session or refresh skills
3. Let OpenClaw discover the skill from the workspace
4. Talk normally and let the character skill handle the roleplay

This repo is not only about explicit `$slug` invocation. The main runtime target is ordinary OpenClaw conversation after skill discovery.

## Local Verification

Read gate should stay off for small talk:

```bash
python scripts/memory_router.py --character-slug rem --phase pre --user-message "The weather is nice today."
```

Read gate should trigger for memory-dependent turns:

```bash
python scripts/memory_router.py --character-slug rem --phase pre --user-message "你还记得我上次说过什么吗"
```

Write gate should trigger for stable preferences:

```bash
python scripts/memory_router.py --character-slug rem --phase post --user-message "以后叫我阿昭"
python scripts/memory_commit.py --character-slug rem --user-message "以后叫我阿昭"
python scripts/memory_fetch.py --character-slug rem --user-message "你还记得我喜欢你怎么叫我吗"
```

## Requirements

- Python 3 for the memory scripts used by generated child skills
- OpenClaw or another AgentSkills-compatible runtime
- text-only source materials in the current version

## License

MIT
