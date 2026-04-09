# Input Contract

## Supported Source Types

V0.1 accepts text-only inputs through `tools/source_normalizer.py`:

- `manual`: user notes or manually written summaries
- `wiki`: fandom wiki or encyclopedia-style summaries
- `quotes`: quote collections or direct dialogue snippets
- `plot`: plot summaries or event recaps

## Minimum Input

Each import should include:

- a source type
- a text file
- enough context to know which character the material belongs to

## Normalized Shape

The normalizer outputs JSON with this structure:

```json
{
  "schema_version": "0.1",
  "source": {
    "source_type": "manual",
    "input_path": "path/to/source.txt",
    "normalized_at": "2026-04-09T00:00:00Z"
  },
  "entries": [
    {
      "entry_id": "manual-001",
      "text": "Character statement or paragraph",
      "kind": "note",
      "line_start": 1,
      "line_end": 3
    }
  ]
}
```

## Guidance

- Use one file per source import when possible.
- Preserve paragraph boundaries for plot and wiki text.
- Preserve line boundaries for quote collections.
- Do not pre-merge unrelated source files before normalization.
