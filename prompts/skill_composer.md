# Skill Composer Prompt

Use this prompt after all three layers exist.

## Goal

Compose the child `SKILL.md` for `characters/{slug}/`.

## The Child Skill Must Say

- read `canon.md` first for facts
- use `persona.md` for behavior and interaction strategy
- use `style_examples.md` for wording texture
- run `memory_router.py` before reading memory
- fetch memory only when the router says read is needed
- commit memory only when the router says write is needed
- summarize memory only at the configured threshold
- never upgrade persona inference into canon during live conversation

## Composition Rules

- keep the child skill short and operational
- do not duplicate every bullet from canon and persona into the child skill
- reference the layer files as the source of truth
- keep the runtime order explicit: canon, then persona, then style, then conditional memory routing
- point dynamic memory to `./.dreamlover-data/` instead of the skill package
