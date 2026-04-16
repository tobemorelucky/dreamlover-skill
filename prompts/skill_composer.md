# Skill Composer Prompt

Use this prompt after all three layers exist.

## Goal

Compose the child `SKILL.md` for the installed runtime package at `./.agents/skills/{slug}/`.

## The Child Skill Must Say

- read `canon.md` first for facts
- use `persona.md` for behavior and interaction strategy
- use `style_examples.md` for wording texture
- use OpenClaw-compatible front matter with `name`, `description`, and Python requirement metadata
- run `memory_router.py` before reading memory
- fetch memory only when the router says read is needed
- commit memory only when the router says write is needed
- summarize memory only at the configured threshold
- degrade to no-memory mode if `python3` is unavailable
- never upgrade persona inference into canon during live conversation

## Composition Rules

- keep the child skill short and operational
- do not duplicate every bullet from canon and persona into the child skill
- reference the layer files as the source of truth
- keep the runtime order explicit: canon, then persona, then style, then conditional memory routing
- point dynamic memory to `./.dreamlover-data/` instead of the skill package
- write the child skill as an OpenClaw-ready runtime instruction, not a Codex-only invocation note
