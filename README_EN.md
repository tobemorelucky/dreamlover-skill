# dreamlover-skill

> *"The people who built large models are basically coding gods. AI-assisted coding already helped frontend people, and it should help backend people, QA people, ops people, security people, IC people, and eventually help everyone liberate themselves and all humanity. (This skill was generated almost entirely by Codex.)"*
>
> Distill anime and game virtual character materials into a reusable agent skill.
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
> [![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
> [![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)
>
> Feed it character profiles, plot summaries, quote collections, wiki pages, or your own notes, and it will turn them into a layered, reusable character skill.
>
> Repository: [tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)
>
> [Installation](#installation) · [Usage](#usage) · [Example](#example) · [Project Structure](#project-structure) · [中文](README.md)

---

## What It Is

`dreamlover-skill` is not a single character skill. It is a **meta-skill** for building character skills.

It helps you:

- ingest character source materials
- sort them by evidence quality
- split them into `canon / persona / style_examples`
- generate a child character skill
- support corrections, updates, and version snapshots

It is useful when you want a character skill that is both believable and structured: factually grounded, behaviorally consistent, and stylistically recognizable.

---

## Core Layering

| Layer | Purpose | Allowed content |
| --- | --- | --- |
| `canon` | factual layer | objective facts, explicit plot events, explicit identity relationships, explicit setting attributes, explicit official statements |
| `persona` | behavior layer | behavior patterns, emotional tendencies, interaction style, relationship progression logic, boundaries and preferences |
| `style_examples` | expression layer | address habits, sentence rhythm, verbal tics, short example lines |

Recommended runtime order:

1. Read `canon.md` for facts.
2. Read `persona.md` for behavior.
3. Read `style_examples.md` for wording texture.

---

## Installation

### Claude Code

```bash
# global install
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill

# project-local install
git clone https://github.com/tobemorelucky/dreamlover-skill .claude/skills/dreamlover-skill
```

### Codex

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### Requirements

- Python 3.9+
- A skill-capable agent runtime
- Text-based source materials

---

## Usage

### 1. Prepare source materials

V0.1 is text-only. Typical inputs include:

- official character profiles
- plot summaries
- quote collections
- wiki or encyclopedia summaries
- user-written notes

### 2. Audit sources

Recommended evidence priority:

1. official material
2. quoted plot or dialogue excerpts
3. fandom wiki or community summaries
4. user summaries

### 3. Build the character package

Recommended order:

1. `canon`
2. `persona`
3. `style_examples`
4. child `SKILL.md`
5. version snapshot

### 4. Use the helper tools

```bash
python tools/slugify.py "Raiden Shogun"
python tools/source_normalizer.py --input sample.txt --type wiki --output normalized.json
python tools/evidence_indexer.py --input normalized.json --output indexed.json
python tools/style_extractor.py --input sample.txt --output style.json
python tools/skill_writer.py --action create --slug raiden-shogun --name "Raiden Shogun"
python tools/version_manager.py --action snapshot --slug raiden-shogun
```

---

## Example

A minimal example package is included at:

- `characters/demo-hero/`

It shows the expected structure for:

- `canon.md`
- `persona.md`
- `style_examples.md`
- child `SKILL.md`
- `sources/normalized.json`
- version snapshots

---

## Features

### Included in V0.1

- text normalization
- source reliability layering
- strict `canon / persona / style_examples` separation
- character package generation
- snapshot and rollback foundations

### Not included yet

- image parsing
- audio parsing
- video parsing
- online source fetching
- advanced semantic policy enforcement

---

## Project Structure

```text
dreamlover-skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── docs/
├── prompts/
├── tools/
├── characters/
└── versions/
```

Key directories:

- `docs/`: contracts, evidence rules, safety rules
- `prompts/`: prompt guides for each build stage
- `tools/`: helper scripts for normalization, indexing, writing, and snapshots
- `characters/`: generated character packages
- `versions/`: repository-level contract snapshots

---

## Notes

- Material quality directly affects fidelity.
- `canon` must stay factual and directly supported.
- `persona` must stay inferential and behavioral.
- `style_examples` should shape language, not lore.
- The goal is character distillation, not raw corpus copying.

---

## License

MIT
