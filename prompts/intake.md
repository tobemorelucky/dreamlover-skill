# Intake Prompt

Use this prompt at the start of a request.

## Goal

Decide whether the user wants to create, update, correct, or list character skills.
If the request is for a new character skill and the intake bundle is incomplete, stop and ask the missing intake questions before generating anything.

## Collect

- character name
- source work
- target use
- request type: create, update, correct, list
- source types provided: official, plot, quotes, wiki, user
- whether low-confidence persona inference is allowed
- expected output quality: fact fix, persona fix, style fix, or full build

## Minimum Intake Questions

Ask these questions in order whenever a new character request is underspecified:

1. What is the character name?
2. What is the source work?
3. What is the target use for this skill?
4. Which source material types do you have right now: official setting, plot summary, quote excerpts, wiki summary, or user description?
5. If the source material stays incomplete, may the system use low-confidence persona inference, or should it stay fully conservative?

If the user only provides a name, the intake is not complete yet.

## Routing Rule

- if the user wants a new character package and intake is incomplete, keep asking intake questions
- if the user wants a new character package and intake is complete, go to `source_audit.md`
- if the user wants a correction, go to `correction_handler.md`
- if the user wants to merge new material, go to `evolution_merge.md`
- if the user wants to inspect existing characters, use `tools/skill_writer.py --action list`

## Output

Produce a short intake summary with:

- character
- source work
- target use
- request type
- source bundle summary
- low-confidence persona policy
- next prompt to use
