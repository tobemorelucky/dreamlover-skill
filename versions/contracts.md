# Contracts

## Repository Layout

- `SKILL.md`
- `AGENTS.md`
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
- `python tools/skill_writer.py --action create|update|list --slug <slug> --root <path>`
- `python tools/version_manager.py --action snapshot|rollback --slug <slug> --root <path>`

## Layer Contracts

- `canon` contains only directly supported facts and explicit official positions
- `persona` contains only summarized behavior and interaction logic
- `style_examples` contains only language texture and short examples
