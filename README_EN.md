# dreamlover-skill

> Distill anime and game character materials into one canonical character source, then generate a Codex-first runtime package and an optional OpenClaw export.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)

Repo: [tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)

[中文](README.md)

## What This Repo Does

`dreamlover-skill` is the top-level generator skill, not the final chat-facing character skill itself.

It first produces one canonical static character source:

- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`

That source lives in:

- `characters/{slug}/`

Then it generates platform wrappers from the same static content:

- Codex primary install: `./.agents/skills/{slug}/`
- OpenClaw optional export: `<openclaw_workspace>/.agents/skills/{slug}/`

The static files stay identical across both platforms.
Only `SKILL.md` and required `runtime/` packaging are platform-specific.

## Primary Flow

Codex is the primary install target.

When a character is generated, the default behavior is:

1. write the canonical source to `characters/{slug}/`
2. install the Codex package to `./.agents/skills/{slug}/`
3. ask whether to export an OpenClaw version
4. if yes, ask for the OpenClaw workspace path
5. export to `<openclaw_workspace>/.agents/skills/{slug}/`

Do not treat the Codex install and the OpenClaw export as two editable sources.
If the character changes, regenerate or re-export from the canonical source instead.

## Layer Separation

- `canon.md`: facts, setting, confirmed events, confirmed relationships
- `persona.md`: behavior patterns, interaction strategy, boundaries
- `style_examples.md`: wording texture and short example lines

## Conditional Memory

Generated child skills keep conditional memory, but runtime memory is not part of the static character package.

- runtime database path: `<workspace>/.dreamlover-data/memory.sqlite3`
- `.dreamlover-data/` is not copied into skill directories
- small talk should usually skip memory entirely
- call `runtime/memory_prepare.py` only when needed
- call `runtime/memory_commit.py` only when a write is needed after the reply
- call `runtime/memory_summarize.py` only when the threshold is reached

If `python3` is unavailable, the child skill should gracefully fall back to no-memory mode.

## Usage

### Generate with the top-level skill

```text
$dreamlover-skill
Help me create a Rem character skill
```

Expected flow:

1. intake gate
2. generated draft summary confirmation
3. canonical source is written
4. Codex package is installed
5. optional OpenClaw export is offered

### CLI generation

```bash
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug rem --name "Rem"
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /path/to/openclaw-workspace
```

## Codex Usage

After generation, the Codex package should exist at:

```text
./.agents/skills/rem/
```

Then in Codex:

```text
/skills
$rem
```

## OpenClaw Usage

If export is enabled, the OpenClaw package should exist at:

```text
<openclaw_workspace>/.agents/skills/rem/
```

Then in OpenClaw:

- refresh skills or start a new session
- let OpenClaw discover the child skill from the workspace
- trigger the character naturally through normal conversation

The OpenClaw package shares the same static character files, but uses an OpenClaw-specific wrapper `SKILL.md`.

## Path and Export Guarantees

To avoid path bugs, exported OpenClaw packages do not rely on hard-coded home directories.

The current design is:

- static role files live directly in `<openclaw_workspace>/.agents/skills/{slug}/`
- runtime scripts live in `<openclaw_workspace>/.agents/skills/{slug}/runtime/`
- the wrapper calls local `runtime/` scripts through relative paths
- the wrapper writes memory to `<workspace>/.dreamlover-data/` through a relative `--data-root`

That means:

- you do not need to copy the entire repo into the OpenClaw workspace
- export should not break because a different machine uses a different home path
- runtime memory is kept out of the exported skill directory

## Local Verification

### Verify canonical + Codex generation

```bash
python tools/skill_writer.py --action create --interactive
```

Expected result:

- `characters/{slug}/` contains the canonical source
- `./.agents/skills/{slug}/` contains the Codex package

### Verify OpenClaw export

```bash
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /tmp/openclaw-demo
```

Expected result:

- `/tmp/openclaw-demo/.agents/skills/rem/` exists
- `canon.md`, `persona.md`, `style_examples.md`, and `meta.json` match the Codex package
- only `SKILL.md` and `runtime/` differ by platform

### Verify memory gate behavior

```bash
python scripts/memory_prepare.py --character-slug rem --user-message "The weather is nice today."
python scripts/memory_prepare.py --character-slug rem --user-message "Do you remember what I told you last time?"
python scripts/memory_prepare.py --character-slug rem --user-message "From now on, call me Azhao."
```

Expected result:

- small talk: no read, no write
- explicit memory question: read
- stable nickname preference: write after the reply

## Notes

- the canonical source is the only recommended editable source
- do not hand-edit exported Codex or OpenClaw directories
- regenerate or re-export when the character changes
- the current version is still text-first and does not process image, audio, or video inputs

## License

MIT
