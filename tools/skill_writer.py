from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from skill_linter import lint_skill_dir

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
DEFAULT_INSTALL_ROOT = Path(".agents") / "skills"
DEFAULT_ARCHIVE_ROOT = Path("characters")
SECTION_PLACEHOLDERS = {
    "## Basic Identity": "- No confirmed identity facts recorded yet.",
    "## Setting Attributes": "- No confirmed setting attributes recorded yet.",
    "## Key Plot Events": "- No confirmed plot events recorded yet.",
    "## Confirmed Relationships": "- No confirmed relationships recorded yet.",
    "## Official Statements And Notes": "- No official statements recorded yet.",
    "## Behavior Patterns": "- No summarized behavior patterns recorded yet.",
    "## Emotional Tendencies": "- No summarized emotional tendencies recorded yet.",
    "## Interaction Style": "- No summarized interaction strategy recorded yet.",
    "## Relationship Progression": "- No summarized relationship progression recorded yet.",
    "## Boundaries And Preferences": "- No summarized boundaries or preferences recorded yet.",
    "## Address Patterns": "- No style address patterns recorded yet.",
    "## Rhythm And Sentence Shape": "- No style rhythm notes recorded yet.",
    "## Verbal Tics": "- No style verbal tics recorded yet.",
    "## Short Example Lines": "- No short example lines recorded yet.",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_scope(value: str) -> str:
    allowed = {"codex", "archive", "both"}
    if value not in allowed:
        raise argparse.ArgumentTypeError(f"Unsupported scope: {value}")
    return value


def resolve_root(base_root: Path, value: str | None, fallback: Path) -> Path:
    if not value:
        return base_root / fallback
    path = Path(value)
    return path if path.is_absolute() else base_root / path


def read_text(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8")


def default_markdown(headers: list[str]) -> str:
    blocks = [f"{header}\n\n{SECTION_PLACEHOLDERS[header]}" for header in headers]
    return "\n\n".join(blocks) + "\n"


def is_placeholder_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return stripped == "- TODO" or stripped in SECTION_PLACEHOLDERS.values()


def normalize_header_line(line: str) -> str:
    return line.strip().lstrip("\ufeff")


def parse_section_segments(text: str, headers: list[str]) -> dict[str, list[list[str]]]:
    segments = {header: [] for header in headers}
    current_header: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_header, current_lines
        if current_header is not None:
            segments[current_header].append(current_lines[:])
        current_header = None
        current_lines = []

    for raw_line in text.splitlines():
        stripped = normalize_header_line(raw_line)
        if stripped in headers:
            flush()
            current_header = stripped
            current_lines = []
            continue
        if stripped.startswith("## "):
            flush()
            continue
        if current_header is not None:
            current_lines.append(raw_line)

    flush()
    return segments


def choose_section_body(segments: list[list[str]], placeholder: str) -> str:
    best_lines: list[str] | None = None
    best_score = -1

    for candidate in segments:
        meaningful = [line for line in candidate if line.strip() and not is_placeholder_line(line)]
        score = len(meaningful)
        if score > best_score:
            best_score = score
            best_lines = candidate

    lines = [line.rstrip() for line in (best_lines or [])]
    lines = [line for line in lines if line.strip()]
    if not lines:
        return placeholder

    meaningful = [line for line in lines if not is_placeholder_line(line)]
    if meaningful:
        lines = meaningful

    return "\n".join(lines)


def ensure_sections(text: str | None, headers: list[str]) -> str:
    if not text or not text.strip():
        return default_markdown(headers)
    segments = parse_section_segments(text, headers)
    blocks = []
    for header in headers:
        body = choose_section_body(segments[header], SECTION_PLACEHOLDERS[header])
        blocks.append(f"{header}\n\n{body}")
    return "\n\n".join(blocks) + "\n"


def validate_cross_headers(text: str, forbidden: list[str], label: str) -> None:
    for header in forbidden:
        if header in text:
            raise ValueError(f"{label} contains forbidden section header: {header}")


def build_child_skill(name: str, slug: str) -> str:
    return (
        f"---\n"
        f"name: {slug}\n"
        f"description: Roleplay as {name} and answer in {name}'s voice. Read canon first, then persona, then style examples.\n"
        f"---\n\n"
        f"# {name}\n\n"
        f"Use this skill to roleplay or answer as {name}.\n\n"
        f"## Runtime Order\n\n"
        f"1. Read `canon.md` first for facts, setting, events, and relationships.\n"
        f"2. Read `persona.md` for behavior patterns, emotional tendencies, and interaction strategy.\n"
        f"3. Read `style_examples.md` for wording texture, cadence, and short response flavor.\n\n"
        f"## Direct Invocation\n\n"
        f"- In Codex, call this skill with `${slug}`.\n"
        f"- Use `/skills` to verify that `{slug}` is installed and discoverable.\n\n"
        f"## Rules\n\n"
        f"- Never promote persona inference into canon during live conversation.\n"
        f"- If facts and style conflict, facts from `canon.md` win.\n"
        f"- If the behavior feels off, improve `persona.md` before changing canon.\n"
        f"- If the voice feels weak, improve `style_examples.md` before changing canon.\n"
    )


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_path(base_root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    return path.relative_to(base_root).as_posix()


def load_existing_meta(paths: list[Path]) -> dict:
    for path in paths:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_existing_text(paths: list[Path]) -> str | None:
    for path in paths:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def package_targets(
    root: Path,
    slug: str,
    install_scope: str,
    output_root: str | None,
) -> tuple[Path, Path | None]:
    primary_root = resolve_root(
        root,
        output_root,
        DEFAULT_ARCHIVE_ROOT if install_scope == "archive" else DEFAULT_INSTALL_ROOT,
    )
    primary_dir = primary_root / slug
    archive_dir = None
    default_archive_dir = (root / DEFAULT_ARCHIVE_ROOT) / slug
    if install_scope == "both":
        if primary_dir != default_archive_dir:
            archive_dir = default_archive_dir
    return primary_dir, archive_dir


def ensure_package_dir(package_dir: Path) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "sources").mkdir(parents=True, exist_ok=True)
    (package_dir / "versions").mkdir(parents=True, exist_ok=True)


def write_package(
    package_dir: Path,
    canon_text: str,
    persona_text: str,
    style_text: str,
    skill_text: str,
    meta: dict,
    normalized_payload: dict,
) -> None:
    ensure_package_dir(package_dir)
    (package_dir / "canon.md").write_text(canon_text, encoding="utf-8")
    (package_dir / "persona.md").write_text(persona_text, encoding="utf-8")
    (package_dir / "style_examples.md").write_text(style_text, encoding="utf-8")
    (package_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
    write_json(package_dir / "meta.json", meta)
    normalized_path = package_dir / "sources" / "normalized.json"
    if not normalized_path.exists():
        write_json(normalized_path, normalized_payload)


def lint_package(package_dir: Path) -> dict:
    report = lint_skill_dir(package_dir)
    if report["errors"]:
        raise ValueError(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def list_packages(root: Path, scope: str) -> list[dict]:
    search_roots: list[tuple[str, Path]] = []
    if scope in {"codex", "both"}:
        search_roots.append(("codex", root / DEFAULT_INSTALL_ROOT))
    if scope in {"archive", "both"}:
        search_roots.append(("archive", root / DEFAULT_ARCHIVE_ROOT))

    indexed: dict[str, dict] = {}
    for location, search_root in search_roots:
        if not search_root.exists():
            continue
        for item in sorted(search_root.iterdir()):
            if not item.is_dir():
                continue
            meta_path = item / "meta.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"slug": item.name}
            record = indexed.setdefault(meta.get("slug", item.name), dict(meta))
            record.setdefault("locations", [])
            record["locations"].append(location)
    return list(indexed.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="Create, update, or list character skill packages.")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"], help="Operation to run.")
    parser.add_argument("--slug", help="Character slug.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root.")
    parser.add_argument("--output-root", help="Override the primary output root. Defaults to ./.agents/skills for codex installs.")
    parser.add_argument(
        "--install-scope",
        default="both",
        type=parse_scope,
        help="Where to write packages: codex, archive, or both. Default writes to ./.agents/skills and mirrors to characters.",
    )
    parser.add_argument(
        "--list-scope",
        default="codex",
        type=parse_scope,
        help="Which package roots to inspect when using --action list.",
    )
    parser.add_argument("--name", help="Character display name.")
    parser.add_argument("--source-work", default="", help="Source work name.")
    parser.add_argument("--canon-file", help="Optional canon markdown path.")
    parser.add_argument("--persona-file", help="Optional persona markdown path.")
    parser.add_argument("--style-file", help="Optional style markdown path.")
    parser.add_argument("--skip-lint", action="store_true", help="Skip post-write package linting.")
    args = parser.parse_args()

    root = Path(args.root)
    (root / DEFAULT_INSTALL_ROOT).mkdir(parents=True, exist_ok=True)
    (root / DEFAULT_ARCHIVE_ROOT).mkdir(parents=True, exist_ok=True)

    if args.action == "list":
        print(json.dumps(list_packages(root, args.list_scope), ensure_ascii=False, indent=2))
        return

    if not args.slug:
        raise SystemExit("--slug is required for create and update")

    primary_dir, archive_dir = package_targets(root, args.slug, args.install_scope, args.output_root)
    meta_candidates = [primary_dir / "meta.json"]
    if archive_dir is not None:
        meta_candidates.append(archive_dir / "meta.json")
    existing = load_existing_meta(meta_candidates)

    canon_existing = load_existing_text([primary_dir / "canon.md"] + ([archive_dir / "canon.md"] if archive_dir else []))
    persona_existing = load_existing_text([primary_dir / "persona.md"] + ([archive_dir / "persona.md"] if archive_dir else []))
    style_existing = load_existing_text([primary_dir / "style_examples.md"] + ([archive_dir / "style_examples.md"] if archive_dir else []))

    canon_text = ensure_sections(read_text(args.canon_file) or canon_existing, CANON_HEADERS)
    persona_text = ensure_sections(read_text(args.persona_file) or persona_existing, PERSONA_HEADERS)
    style_text = ensure_sections(read_text(args.style_file) or style_existing, STYLE_HEADERS)

    validate_cross_headers(canon_text, PERSONA_HEADERS, "canon")
    validate_cross_headers(persona_text, CANON_HEADERS, "persona")

    name = args.name or existing.get("character_name") or args.slug
    created_at = existing.get("created_at", utc_now())
    updated_at = utc_now()
    meta = {
        "slug": args.slug,
        "character_name": name,
        "source_work": args.source_work or existing.get("source_work", ""),
        "layout_version": "0.2",
        "created_at": created_at,
        "updated_at": updated_at,
        "primary_path": relative_path(root, primary_dir),
        "archive_path": relative_path(root, archive_dir),
        "install_scope": args.install_scope,
    }
    normalized_payload = {
        "schema_version": "0.1",
        "source": {"source_type": "manual", "input_path": "", "normalized_at": updated_at},
        "entries": [],
    }
    skill_text = build_child_skill(name, args.slug)

    write_package(primary_dir, canon_text, persona_text, style_text, skill_text, meta, normalized_payload)
    if archive_dir is not None:
        write_package(archive_dir, canon_text, persona_text, style_text, skill_text, meta, normalized_payload)

    lint_results: dict[str, dict] = {}
    if not args.skip_lint:
        lint_results["primary"] = lint_package(primary_dir)
        if archive_dir is not None:
            lint_results["archive"] = lint_package(archive_dir)

    print(json.dumps({"package": meta, "lint": lint_results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
