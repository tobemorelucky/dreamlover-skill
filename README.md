# dreamlover-skill

> Anime / game virtual character distillation skill repo.
>
> GitHub: https://github.com/tobemorelucky/dreamlover-skill

`dreamlover-skill` is a meta-skill for turning character materials into reusable agent skills.
It takes text sources such as official profiles, plot summaries, quote collections, wiki pages, and user notes, then separates them into three layers:

- `canon`: directly supported facts
- `persona`: behavior and interaction patterns summarized from the materials
- `style_examples`: wording, rhythm, and short example lines

The goal is to keep factual setting, behavioral inference, and language style from getting mixed together.

---

## What It Does

This repository helps you:

- build a new character skill from raw text materials
- update an existing character when new materials appear
- correct fact drift, behavior drift, or style drift separately
- keep version snapshots for generated character packages

It is designed for text-first character distillation, not large-scale raw corpus storage.

---

## Core Layering

| Layer | Purpose | Allowed content |
| --- | --- | --- |
| `canon` | factual layer | objective facts, explicit plot events, explicit identity relationships, explicit setting attributes, explicit official statements |
| `persona` | behavior layer | behavior patterns, emotional tendencies, interaction style, relationship progression logic, boundaries and preferences |
| `style_examples` | expression layer | address habits, sentence rhythm, verbal tics, short example lines |

Recommended runtime order:

1. Read `canon.md` for facts.
2. Read `persona.md` for behavior and reactions.
3. Read `style_examples.md` for wording texture.

---

## Installation

### Claude Code

Clone this repository into your Claude skill directory:

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill
```

Or for a project-local install:

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill .claude/skills/dreamlover-skill
```

### Codex

If you want to use it in Codex, place it under your skills directory:

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### Requirements

- Python 3.9+
- A skill-capable agent environment
- Text source materials

---

## How To Use

### 1. Prepare source materials

V0.1 is text-only. Typical inputs include:

- official character profiles
- plot summaries
- quote collections
- wiki / encyclopedia summaries
- user-written notes

### 2. Audit the materials

Before writing the character package, sort materials by reliability:

1. official material
2. quoted plot or dialogue excerpts
3. fandom wiki or community summaries
4. user summaries

### 3. Build the three layers

Write the character package in this order:

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

## Generated Output

Each generated character package lives under:

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

---

## Example

A sample package is included at:

- `characters/demo-hero/`

It shows the expected structure for:

- `canon.md`
- `persona.md`
- `style_examples.md`
- child `SKILL.md`
- `sources/normalized.json`
- version snapshots

---

## Project Structure

```text
dreamlover-skill/
├── SKILL.md
├── README.md
├── docs/
├── prompts/
├── tools/
├── characters/
└── versions/
```

Key directories:

- `docs/`: contracts, safety rules, evidence rules
- `prompts/`: phase-specific prompt guides
- `tools/`: helper scripts for normalization, indexing, writing, and snapshots
- `characters/`: generated character packages
- `versions/`: repository-level contract snapshots

---

## Design Rules

- Keep `canon` factual and directly supported.
- Keep `persona` inferential, but never factual.
- Keep `style_examples` focused on expression, not lore.
- Fix fact errors in `canon`.
- Fix behavior drift in `persona`.
- Fix voice drift in `style_examples`.

---

## Current Scope

V0.1 currently includes:

- repository skeleton
- prompts, docs, and tools
- text-first workflow
- character package layout
- version snapshot support

V0.1 does not yet include:

- image parsing
- audio parsing
- video parsing
- online source fetching
- advanced semantic policy enforcement

---

## License

MIT
