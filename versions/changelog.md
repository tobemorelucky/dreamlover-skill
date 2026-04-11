# Changelog

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
