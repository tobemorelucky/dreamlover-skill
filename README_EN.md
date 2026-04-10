# dreamlover-skill

> *"The people who built large models are basically coding gods. AI-assisted coding created Raiden Shogun, and it should go on to create Makima, Marin Kitagawa, Violet Evergarden, Rem, Utaha Kasumigaoka, Nino Nakano, Mai Sakurajima, and eventually a perfect world filled with beautiful girls."*
>
> Distill anime and game virtual character materials into a reusable Agent Skill.
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
> [![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
> [![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)
>
> Feed it character settings, plot summaries, quote collections, wiki pages, or your own notes, and it will turn them into a sustainable character skill.
>
> Repository: [tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)
>
> [Installation](#installation) · [Usage](#usage) · [Example](#example) · [Project Structure](#project-structure) · [Notes](#notes) · [中文](README.md)

---

## What It Is

`dreamlover-skill` is a character skill generator.

It organizes character materials into three layers:

- `canon.md`: facts, setting, explicit events, relationships
- `persona.md`: behavior patterns, interaction strategy, boundaries
- `style_examples.md`: expression style and short example lines

After generation, it installs the result as a real child skill discoverable by Codex:

- primary install path: `./.agents/skills/{slug}/`
- archive mirror: `characters/{slug}/`
- direct invocation: `$slug`
- discovery check: `/skills`

---

## Installation

### Claude Code

Claude Code will discover this repository from a skill directory.

```bash
# global install
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill

# project-local install
git clone https://github.com/tobemorelucky/dreamlover-skill .claude/skills/dreamlover-skill
```

### Codex

If you want to use it in Codex:

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

Generated child skills are installed by default into:

```text
./.agents/skills/{slug}/
```

### Requirements

- Python 3.9+
- A skill-capable agent environment
- Text-only materials for v1
- No GPU, local model, or Docker required

---

## Usage

### 1. Prepare source materials

V0.1 supports:

- official character settings
- plot summaries
- quote collections
- wiki / encyclopedia summaries
- user notes

### 2. Audit sources

Recommended priority:

1. official material
2. plot / dialogue excerpts
3. community wiki summaries
4. user summaries

### 3. Generate a character skill

Recommended flow:

1. invoke `$dreamlover-skill`
2. provide character name, source work, and use case
3. perform source audit
4. build `canon`
5. build `persona`
6. build `style_examples`
7. compose child `SKILL.md`
8. install to `./.agents/skills/{slug}/`
9. optionally mirror to `characters/{slug}/`
10. create a snapshot

### 4. Use helper tools

```bash
python tools/slugify.py "Raiden Shogun"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/version_manager.py --action snapshot --slug raiden-shogun --scope codex
```

### 5. Call it directly in Codex

After generation:

1. run `/skills`
2. verify the slug appears
3. call `$slug` directly

Example:

```text
/skills
$raiden-shogun
$rem
```

---

## Example

The repository includes a minimal demo:

- `characters/demo-hero/`

And the same role can be installed as a directly callable child skill:

- `./.agents/skills/demo-hero/`

Each generated child skill contains at least:

- `SKILL.md`
- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`

The shortest end-to-end path is:

1. generate a role
2. see it in `/skills`
3. talk to it with `$slug`

---

## Features

### Current capabilities

- text normalization
- source reliability layering
- strict `canon / persona / style_examples` separation
- character package generation
- installation to `./.agents/skills/{slug}/`
- archive mirroring to `characters/{slug}/`
- snapshot and rollback foundations

### Not included yet

- image parsing
- audio parsing
- video parsing
- automatic online source retrieval
- advanced semantic review

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

- source quality determines fidelity
- `canon` must stay factual and directly supported
- `persona` must stay behavioral and inferential
- `style_examples` should shape expression, not invent lore
- Codex discovers `./.agents/skills/{slug}/`, not `characters/{slug}/`
- if `/skills` does not refresh, restart or refresh Codex and check again
- the goal is distillation, not raw corpus copying

---

## License

MIT
