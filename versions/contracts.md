# Contracts

## Repository Layout

- `SKILL.md`
- `AGENTS.md`
- `.agents/skills/`
- `docs/`
- `prompts/`
- `tools/`
- `versions/`
- `characters/`

## Tool Interfaces

- `python tools/slugify.py "<name>"`
- `python tools/source_normalizer.py --input <path> --type manual|wiki|quotes|plot --output <path>`
- `python tools/evidence_indexer.py --input <normalized.json> --output <indexed.json>`
- `python tools/style_extractor.py --input <path> --output <style.json>`
- `python tools/skill_writer.py --action create|update|list --slug <slug> --root <path> [--output-root <path>] [--install-scope codex|archive|both] [--skip-lint]`
- `python tools/version_manager.py --action snapshot|rollback --slug <slug> --root <path> [--output-root <path>] [--scope codex|archive|both]`
- `python tools/skill_linter.py --slug <slug> --root <path> [--output-root <path>] [--scope codex|archive|both]`

## Layer Contracts

- `canon` contains only directly supported facts and explicit official positions
- `persona` contains only summarized behavior and interaction logic
- `style_examples` contains only language texture and short examples

## Runtime Contract

- generated child skills are installed to `./.agents/skills/{slug}/` by default
- `characters/{slug}/` is an archive mirror when `skill_writer.py` runs with the default `both` scope
- Codex discovery should happen from the installed skill directory, not from the archive mirror
- `skill_writer.py` runs a post-write lint pass by default and returns lint results alongside package metadata
