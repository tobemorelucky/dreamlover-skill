# Output Contract

## Character Package Layout

Each generated character package is installed under `./.agents/skills/{slug}/`.

This is the primary runtime location that Codex should discover through `/skills` and direct invocation with `$slug`.

If archive mirroring is enabled, the same package is also written to `characters/{slug}/` as a repository-local archive copy.

Each package contains:

- `SKILL.md`: child skill entrypoint
- `canon.md`: factual layer
- `persona.md`: behavioral layer
- `style_examples.md`: wording layer
- `meta.json`: character metadata
- `sources/normalized.json`: normalized source bundle or merge result
- `versions/`: character-level snapshots

Generated packages should also satisfy these lint expectations:

- no missing required files
- no duplicate required section headers
- no cross-layer section headers mixed into the wrong file
- child `SKILL.md` contains YAML front matter with `name` and `description`
- published packages should not keep raw `TODO` placeholders

## Canon Sections

`canon.md` should use these sections:

- `## Basic Identity`
- `## Setting Attributes`
- `## Key Plot Events`
- `## Confirmed Relationships`
- `## Official Statements And Notes`

## Persona Sections

`persona.md` should use these sections:

- `## Behavior Patterns`
- `## Emotional Tendencies`
- `## Interaction Style`
- `## Relationship Progression`
- `## Boundaries And Preferences`

## Style Sections

`style_examples.md` should use these sections:

- `## Address Patterns`
- `## Rhythm And Sentence Shape`
- `## Verbal Tics`
- `## Short Example Lines`

## Metadata

`meta.json` should at least include:

- `slug`
- `character_name`
- `source_work`
- `layout_version`
- `created_at`
- `updated_at`
- `primary_path`
- `archive_path`
- `install_scope`

## Child Skill Rule

The child `SKILL.md` must tell the runtime:

- read `canon.md` first for facts
- use `persona.md` for behavior and interaction strategy
- use `style_examples.md` for wording texture
- never upgrade persona inference into canon during conversation
- include YAML front matter with `name` and `description`
- make `description` explicit that the skill is for roleplay or answering in the character's voice
- be directly discoverable from `./.agents/skills/{slug}/`
