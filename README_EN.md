# dreamlover-skill

> Distill anime and game character materials into a reusable Agent Skill that Codex can discover and call directly.
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
> [![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
> [![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)
>
> Repo: [tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)

---

## What This Is

`dreamlover-skill` is a generator skill.

It turns character material into three layers:

- `canon.md`: facts, setting, explicit events, relationships
- `persona.md`: behavior patterns, interaction strategy, boundaries
- `style_examples.md`: wording texture and short example lines

After generation, the child skill is installed as a directly callable Codex skill:

- primary output: `./.agents/skills/{slug}/`
- archive mirror: `characters/{slug}/`
- explicit invocation: `$slug`
- discovery check: `/skills`

---

## Install

### Claude Code

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill
```

### Codex

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

---

## Usage

### 1. Intake First

If you only say:

```text
$dreamlover-skill
Help me create a Rem character skill
```

the generator should not jump straight into generation. It should first ask for:

- character name
- source work
- target use
- source material types: official / plot / quotes / wiki / user description
- whether low-confidence persona inference is allowed

### 2. Generate A Character Skill

Recommended flow:

1. Use `$dreamlover-skill`
2. Answer the intake questions
3. Run source audit
4. Build `canon`
5. Build `persona`
6. Build `style_examples`
7. Compose the child `SKILL.md`
8. Install to `./.agents/skills/{slug}/`
9. Mirror to `characters/{slug}/` when needed
10. Create a version snapshot

### 3. CLI Helpers

```bash
python tools/slugify.py "Raiden Shogun"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/skill_linter.py --slug raiden-shogun --scope codex
python tools/version_manager.py --action snapshot --slug raiden-shogun --scope codex
```

`skill_writer.py --interactive` asks intake questions and writes the answers into:

- `canon.md`
- `persona.md`
- `style_examples.md`
- `sources/normalized.json`
- the child `SKILL.md`

### 4. Call The Character In Codex

After generation:

```text
/skills
$rem
```

### 5. Minimal End-To-End Example

```text
$dreamlover-skill
Help me create a Rem character skill
```

Answer a few intake rounds, then:

```text
/skills
$rem
```

That starts direct in-character conversation.

### 6. Conditional Memory

Generated child skills now use a conditional memory flow instead of always-on memory.

- default: do not read memory
- default: do not write memory
- run `memory_router.py` before the reply
- fetch memory only when the router says read is needed
- commit memory only when the router says write is needed
- summarize memory only when the threshold is reached
- local memory lives in `./.dreamlover-data/`

Minimal local verification:

```bash
python scripts/memory_router.py --character-slug rem --phase pre --user-message "今天天气不错"
python scripts/memory_router.py --character-slug rem --phase pre --user-message "你还记得我上次说过什么吗"
python scripts/memory_router.py --character-slug rem --phase post --user-message "我以后都喜欢你叫我阿昭"
python scripts/memory_commit.py --character-slug rem --user-message "我以后都喜欢你叫我阿昭"
python scripts/memory_fetch.py --character-slug rem --user-message "你还记得我喜欢你怎么叫我吗"
```

---

## Project Structure

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

## Notes

- material quality determines fidelity
- `canon` must stay evidence-backed
- `persona` must stay inferential, not factual
- `style_examples` should not invent lore
- Codex discovers `./.agents/skills/{slug}/`, not `characters/{slug}/`

---

## License

MIT
