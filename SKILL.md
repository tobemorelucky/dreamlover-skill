---
name: dreamlover-skill
description: Create or update distilled agent skills for anime and game virtual characters from text materials. Use when the task requires separating canon, persona, and style examples, then composing a reusable role skill.
---

# Dreamlover Skill

This repository is a meta-skill for building character skills from text-only source materials.

Use this skill when the user wants to:

- create a new character skill from raw notes, wiki pages, plot summaries, or quote collections
- correct an existing character because the facts are wrong, the behavior feels off, or the voice is weak
- merge new source materials into an existing character skill without collapsing canon and persona together
- inspect what character skills are installed in `./.agents/skills/` or archived in `characters/`

## Core Workflow

Follow this order:

1. Collect and normalize the source materials.
2. Audit each source by reliability.
3. Build `canon` first.
4. Build `persona` from source materials plus the confirmed `canon`.
5. Extract `style_examples`.
6. Compose the child `SKILL.md`.
7. Install the child skill under `./.agents/skills/{slug}/`.
8. Mirror it to `characters/{slug}/` when archive output is enabled.
9. Snapshot the installed skill into its `versions/` directory.

Do not skip the ordering. `persona` may depend on `canon`, but `canon` must not depend on `persona`.

## Layer Boundaries

`canon` may only contain:

- objective facts directly supported by source material
- explicit plot events
- explicit identity relationships
- explicit setting attributes
- explicit official statements

`canon` must never contain:

- interpretation
- psychology guesses
- behavior summaries
- style descriptions
- unverified lore

`persona` may only contain:

- behavior patterns summarized from materials
- emotional reaction tendencies
- interaction style
- relationship progression logic
- boundaries and preferences

`persona` must never contain:

- new facts presented as canon
- new plot events
- new identity data
- worldbuilding claims not grounded in source material

`style_examples` may only contain:

- address patterns
- rhythm and sentence habits
- verbal tics and recurring discourse markers
- short example lines

`style_examples` must never replace `canon` or `persona`.

## Files To Read

Read these files only when needed:

- `docs/PRD.md` for product goals and lifecycle
- `docs/evidence-model.md` for evidence priority and conflict handling
- `docs/canon-persona-boundary.md` for layer separation rules
- `docs/input-contract.md` for accepted source formats
- `docs/output-contract.md` for child skill layout
- `docs/safety.md` for content and copyright boundaries

Use these prompts during execution:

- `prompts/intake.md`
- `prompts/source_audit.md`
- `prompts/canon_builder.md`
- `prompts/persona_builder.md`
- `prompts/style_examples_builder.md`
- `prompts/skill_composer.md`
- `prompts/correction_handler.md`
- `prompts/evolution_merge.md`

Use these tools when deterministic output helps:

- `tools/slugify.py`
- `tools/source_normalizer.py`
- `tools/evidence_indexer.py`
- `tools/style_extractor.py`
- `tools/skill_writer.py`
- `tools/version_manager.py`

## Output Layout

Each generated character should be installed under `./.agents/skills/{slug}/`:

- `SKILL.md`
- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`

When archive mirroring is enabled, the same package should also exist under `characters/{slug}/`.

## Quality Bar

Before finishing:

- make sure `canon` contains only directly supported material
- make sure `persona` contains only summarized behavior
- make sure `style_examples` only handles language texture
- make sure corrections modify the right layer
- make sure the child skill is discoverable from `./.agents/skills/{slug}/`
- make sure a snapshot exists after creation or major updates
