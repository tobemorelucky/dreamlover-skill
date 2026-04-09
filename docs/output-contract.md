# Output Contract

## Character Package Layout

Each generated character package lives under `characters/{slug}/`:

- `SKILL.md`: child skill entrypoint
- `canon.md`: factual layer
- `persona.md`: behavioral layer
- `style_examples.md`: wording layer
- `meta.json`: character metadata
- `sources/normalized.json`: normalized source bundle or merge result
- `versions/`: character-level snapshots

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

## Child Skill Rule

The child `SKILL.md` must tell the runtime:

- read `canon.md` first for facts
- use `persona.md` for behavior and interaction strategy
- use `style_examples.md` for wording texture
- never upgrade persona inference into canon during conversation
