# Intake Prompt

Use this prompt at the start of a request.

## Goal

Decide whether the user wants to create, update, correct, or list character skills.

## Collect

- character name
- source work
- request type: create, update, correct, list
- source types provided: manual, wiki, quotes, plot
- expected output quality: fact fix, persona fix, style fix, or full build

## Routing Rule

- if the user wants a new character package, go to `source_audit.md`
- if the user wants a correction, go to `correction_handler.md`
- if the user wants to merge new material, go to `evolution_merge.md`
- if the user wants to inspect existing characters, use `tools/skill_writer.py --action list`

## Output

Produce a short intake summary with:

- character
- source work
- request type
- source bundle summary
- next prompt to use
