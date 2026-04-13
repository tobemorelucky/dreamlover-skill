# Changelog

## v0.4

- upgraded intake from a soft recommendation to a hard no-write gate
- added source decision policy and input mode prompts to interactive intake
- required confirmation of the intake summary before any files are created or modified
- persisted source decision metadata into `meta.json` and `sources/normalized.json`

## v0.3

- added intake-first generation rules to the top-level skill and intake prompt
- added `tools/skill_writer.py --interactive` for CLI question-driven creation
- persisted interactive intake answers into `meta.json`, `sources/normalized.json`, and generated layer files
- updated contracts and README examples to show `/skills` plus `$slug` after generation

## v0.2

- switched generated child skills to Codex-installable output under `./.agents/skills/{slug}/`
- kept `characters/{slug}/` as an archive mirror instead of the only output location
- added `tools/skill_linter.py` for package validation
- made `tools/skill_writer.py` preserve existing content during updates and normalize duplicate sections
- made `tools/skill_writer.py` run post-write linting by default
- required child `SKILL.md` front matter for discoverable roleplay skills

## v0.1

- initialized repository structure
- defined canon, persona, and style_examples boundaries
- added prompt guides for intake, audit, building, correction, and merge
- added deterministic helper tools for first-pass workflows
- defined character package layout and version snapshot behavior
