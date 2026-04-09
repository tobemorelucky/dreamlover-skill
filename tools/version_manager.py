from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

TRACKED_FILES = [
    "SKILL.md",
    "canon.md",
    "persona.md",
    "style_examples.md",
    "meta.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def snapshot_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def copy_sources(source_dir: Path, target_dir: Path) -> None:
    if source_dir.exists():
        shutil.copytree(source_dir, target_dir / "sources", dirs_exist_ok=True)


def load_manifest(path: Path) -> list[dict]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def write_manifest(path: Path, payload: list[dict]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def take_snapshot(character_dir: Path) -> dict:
    versions_dir = character_dir / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)
    sid = snapshot_id()
    target = versions_dir / sid
    target.mkdir(parents=True, exist_ok=False)
    for filename in TRACKED_FILES:
        src = character_dir / filename
        if src.exists():
            shutil.copy2(src, target / filename)
    copy_sources(character_dir / "sources", target)
    manifest_path = versions_dir / "index.json"
    manifest = load_manifest(manifest_path)
    entry = {"snapshot_id": sid, "created_at": utc_now()}
    manifest.append(entry)
    write_manifest(manifest_path, manifest)
    return entry


def rollback(character_dir: Path, sid: str) -> dict:
    source = character_dir / "versions" / sid
    if not source.exists():
        raise FileNotFoundError(f"Snapshot not found: {sid}")
    for filename in TRACKED_FILES:
        src = source / filename
        if src.exists():
            shutil.copy2(src, character_dir / filename)
    sources_dir = source / "sources"
    if sources_dir.exists():
        shutil.copytree(sources_dir, character_dir / "sources", dirs_exist_ok=True)
    return {"snapshot_id": sid, "rolled_back_at": utc_now()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create and restore character package snapshots.")
    parser.add_argument("--action", required=True, choices=["snapshot", "rollback"], help="Operation to run.")
    parser.add_argument("--slug", required=True, help="Character slug.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root.")
    parser.add_argument("--snapshot-id", help="Snapshot id for rollback.")
    args = parser.parse_args()

    character_dir = Path(args.root) / "characters" / args.slug
    if not character_dir.exists():
        raise SystemExit(f"Character package not found: {character_dir}")

    if args.action == "snapshot":
        result = take_snapshot(character_dir)
    else:
        if not args.snapshot_id:
            raise SystemExit("--snapshot-id is required for rollback")
        result = rollback(character_dir, args.snapshot_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
