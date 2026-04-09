from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

CANON_HEADERS = [
    "## Basic Identity",
    "## Setting Attributes",
    "## Key Plot Events",
    "## Confirmed Relationships",
    "## Official Statements And Notes",
]
PERSONA_HEADERS = [
    "## Behavior Patterns",
    "## Emotional Tendencies",
    "## Interaction Style",
    "## Relationship Progression",
    "## Boundaries And Preferences",
]
STYLE_HEADERS = [
    "## Address Patterns",
    "## Rhythm And Sentence Shape",
    "## Verbal Tics",
    "## Short Example Lines",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8")


def default_markdown(headers: list[str]) -> str:
    blocks = [f"{header}\n\n- TODO" for header in headers]
    return "\n\n".join(blocks) + "\n"


def ensure_sections(text: str | None, headers: list[str]) -> str:
    if not text or not text.strip():
        return default_markdown(headers)
    result = text.rstrip() + "\n"
    existing = {line.strip() for line in result.splitlines() if line.startswith("## ")}
    for header in headers:
        if header not in existing:
            result += f"\n{header}\n\n- TODO\n"
    return result


def validate_cross_headers(text: str, forbidden: list[str], label: str) -> None:
    for header in forbidden:
        if header in text:
            raise ValueError(f"{label} contains forbidden section header: {header}")


def build_child_skill(name: str, slug: str) -> str:
    return f"---\nname: {slug}\ndescription: Distilled role skill for {name}. Read canon first, then persona, then style examples.\n---\n\n# {name}\n\nUse this child skill to roleplay or answer as the character.\n\n## Runtime Order\n\n1. Read `canon.md` first for facts.\n2. Read `persona.md` for behavior, reactions, and interaction logic.\n3. Read `style_examples.md` for wording texture and rhythm.\n\n## Rules\n\n- Never promote persona inference into canon during live conversation.\n- If facts and style conflict, facts from `canon.md` win.\n- If the voice feels weak, improve `style_examples.md` before changing canon.\n- If the behavior feels off, improve `persona.md` before changing canon.\n"


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create, update, or list character packages.")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"], help="Operation to run.")
    parser.add_argument("--slug", help="Character slug.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root.")
    parser.add_argument("--name", help="Character display name.")
    parser.add_argument("--source-work", default="", help="Source work name.")
    parser.add_argument("--canon-file", help="Optional canon markdown path.")
    parser.add_argument("--persona-file", help="Optional persona markdown path.")
    parser.add_argument("--style-file", help="Optional style markdown path.")
    args = parser.parse_args()

    root = Path(args.root)
    characters_dir = root / "characters"
    characters_dir.mkdir(parents=True, exist_ok=True)

    if args.action == "list":
        payload = []
        for item in sorted(characters_dir.iterdir()):
            if item.is_dir():
                meta_path = item / "meta.json"
                meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"slug": item.name}
                payload.append(meta)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if not args.slug:
        raise SystemExit("--slug is required for create and update")

    character_dir = characters_dir / args.slug
    character_dir.mkdir(parents=True, exist_ok=True)
    sources_dir = character_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    (character_dir / "versions").mkdir(parents=True, exist_ok=True)

    canon_text = ensure_sections(read_text(args.canon_file), CANON_HEADERS)
    persona_text = ensure_sections(read_text(args.persona_file), PERSONA_HEADERS)
    style_text = ensure_sections(read_text(args.style_file), STYLE_HEADERS)

    validate_cross_headers(canon_text, PERSONA_HEADERS, "canon")
    validate_cross_headers(persona_text, CANON_HEADERS, "persona")

    name = args.name or args.slug
    meta_path = character_dir / "meta.json"
    existing = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    created_at = existing.get("created_at", utc_now())
    updated_at = utc_now()
    meta = {
        "slug": args.slug,
        "character_name": name,
        "source_work": args.source_work or existing.get("source_work", ""),
        "layout_version": "0.1",
        "created_at": created_at,
        "updated_at": updated_at,
    }

    (character_dir / "canon.md").write_text(canon_text, encoding="utf-8")
    (character_dir / "persona.md").write_text(persona_text, encoding="utf-8")
    (character_dir / "style_examples.md").write_text(style_text, encoding="utf-8")
    (character_dir / "SKILL.md").write_text(build_child_skill(name, args.slug), encoding="utf-8")
    write_json(meta_path, meta)

    normalized_path = sources_dir / "normalized.json"
    if not normalized_path.exists():
        write_json(
            normalized_path,
            {
                "schema_version": "0.1",
                "source": {"source_type": "manual", "input_path": "", "normalized_at": updated_at},
                "entries": [],
            },
        )

    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
