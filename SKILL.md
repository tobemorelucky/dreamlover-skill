---
name: dreamlover-skill
description: Always run intake first before creating or updating distilled agent skills for anime and game virtual characters. Use when the task requires separating canon, persona, and style examples, then composing a reusable role skill with conditional memory gates.
---

# Dreamlover Skill

This repository is a meta-skill for building character skills from text-only source materials.

Use this skill when the user wants to:

- create a new character skill from raw notes, wiki pages, plot summaries, or quote collections
- correct an existing character because the facts are wrong, the behavior feels off, or the voice is weak
- merge new source materials into an existing character skill without collapsing canon and persona together
- inspect what character skills are installed in `./.agents/skills/` or archived in `characters/`

## Hard Intake Gate

If the user wants a new character skill but has not supplied enough intake information, stop and ask the intake questions before generating anything.
If intake is incomplete, you are forbidden to create, update, or modify any character files.

The minimum intake bundle is:

- source decision policy
- input mode: direct text or file path
- character name
- source work
- target use
- source material types: official, plot, quotes, wiki, or user description
- whether low-confidence persona inference is allowed when materials are thin

If the user says only something like "create a Rem skill", do not jump straight to `canon`, `persona`, or `style_examples`. Ask the missing intake questions first, summarize the intake, repeat the key facts back for confirmation, and only then continue.

## Source Decision Policy

Before any generation work, ask which source completion policy is allowed:

1. only user-provided information
2. official material plus wiki material
3. official material plus user material

Then ask how the directly provided material will arrive:

1. direct text entered in chat or CLI
2. file paths that should be read first

If the user has not answered both source policy and input mode, the hard intake gate is still incomplete.

## Core Workflow

Follow this order:

1. Run the hard intake gate first whenever the request is underspecified.
2. Collect and normalize the source materials.
3. Audit each source by reliability.
4. Build `canon` first.
5. Build `persona` from source materials plus the confirmed `canon`.
6. Extract `style_examples`.
7. Compose the child `SKILL.md`.
8. Install the child skill under `./.agents/skills/{slug}/`.
9. Mirror it to `characters/{slug}/` when archive output is enabled.
10. Snapshot the installed skill into its `versions/` directory.
11. Keep dynamic memory outside the package and route it through the local memory scripts only when needed.

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
- `docs/input-contract.md` for accepted source formats and intake minimums
- `docs/output-contract.md` for child skill layout
- `docs/safety.md` for content and copyright boundaries
- `references/memory_policy.md` for conditional memory rules

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
- `tools/skill_linter.py`
- `tools/version_manager.py`

Use these runtime memory scripts when composing or validating child skill behavior:

- `scripts/memory_router.py`
- `scripts/memory_fetch.py`
- `scripts/memory_commit.py`
- `scripts/memory_summarize.py`

Prefer `tools/skill_writer.py --interactive` when intake information is missing or incomplete.
In interactive mode, do not allow any writes before the intake summary is confirmed.

## Output Layout

Each generated character should be installed under `./.agents/skills/{slug}/`:

- `SKILL.md`
- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`

Dynamic memory must not be stored inside the character package. Use `./.dreamlover-data/` for local runtime memory storage.

When archive mirroring is enabled, the same package should also exist under `characters/{slug}/`.

## Quality Bar

Before finishing:

- make sure the hard intake gate completed before generation if the request started underspecified
- make sure no character files were written before intake confirmation
- make sure `canon` contains only directly supported material
- make sure `persona` contains only summarized behavior
- make sure `style_examples` only handles language texture
- make sure corrections modify the right layer
- make sure the child skill is discoverable from `./.agents/skills/{slug}/`
- make sure the installed package passes `tools/skill_linter.py` without errors
- make sure a snapshot exists after creation or major updates
- make sure the child skill only reads or writes memory when the router says it should
- make sure the child skill never fabricates prior conversation history
