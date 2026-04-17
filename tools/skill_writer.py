from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from skill_linter import lint_skill_dir
from slugify import slugify

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
DEFAULT_SOURCE_TYPES = ["user"]
DEFAULT_SOURCE_DECISION_POLICY = "user_only"
DEFAULT_INPUT_MODE = "direct_text"
DEFAULT_SEARCH_SCOPE = "none"
SOURCE_DECISION_POLICIES = {
    "1": "user_only",
    "2": "official_wiki_only",
    "3": "official_plus_user",
    "4": "official_quick",
}
SOURCE_DECISION_LABELS = {
    "user_only": "Only use the information provided by the user",
    "official_wiki_only": "Official sources plus wiki sources",
    "official_plus_user": "Official sources plus user-provided information",
    "official_quick": "Quick generate from official-style defaults",
}
INPUT_MODES = {
    "1": "direct_text",
    "2": "file_path",
}
SEARCH_SCOPES = {
    "1": "small",
    "2": "medium",
    "3": "large",
}
INPUT_MODE_LABELS = {
    "direct_text": "Direct text",
    "file_path": "File path",
}
SEARCH_SCOPE_LABELS = {
    "none": "No public search",
    "small": "Small search scope",
    "medium": "Medium search scope",
    "large": "Large search scope",
}
CANONICAL_SLOTS = [
    "source_policy",
    "input_mode",
    "character_name",
    "source_work",
    "material_types",
    "allow_low_confidence_persona",
    "archive_mirror",
]
SOURCE_POLICY_ALIASES = {
    "1": "user_only",
    "只用我给的信息": "user_only",
    "只用我提供的信息": "user_only",
    "仅用我给的信息": "user_only",
    "仅用用户信息": "user_only",
    "user_only": "user_only",
    "2": "official_wiki_only",
    "官方资料+wiki资料": "official_wiki_only",
    "官方资料+wiki": "official_wiki_only",
    "官方+wiki": "official_wiki_only",
    "official_wiki_only": "official_wiki_only",
    "3": "official_plus_user",
    "官方资料+我给的信息": "official_plus_user",
    "官方资料+用户资料": "official_plus_user",
    "官方+用户": "official_plus_user",
    "official_plus_user": "official_plus_user",
    "4": "official_quick",
    "快速生成": "official_quick",
    "快生成": "official_quick",
    "直接生成": "official_quick",
    "official_quick": "official_quick",
}
INPUT_MODE_ALIASES = {
    "1": "direct_text",
    "我直接贴文本": "direct_text",
    "直接贴文本": "direct_text",
    "聊天里贴文本": "direct_text",
    "聊天里发": "direct_text",
    "直接输入": "direct_text",
    "chat": "direct_text",
    "direct_text": "direct_text",
    "2": "file_path",
    "文件路径": "file_path",
    "路径": "file_path",
    "给你文件路径": "file_path",
    "发文件路径": "file_path",
    "file_path": "file_path",
}
SEARCH_SCOPE_ALIASES = {
    "1": "small",
    "小": "small",
    "small": "small",
    "2": "medium",
    "中": "medium",
    "medium": "medium",
    "3": "large",
    "大": "large",
    "large": "large",
}
SOURCE_TYPE_SYNONYMS = {
    "official": "official",
    "official-setting": "official",
    "official_profile": "official",
    "瀹樻柟": "official",
    "瀹樻柟璁惧畾": "official",
    "plot": "plot",
    "plot-summary": "plot",
    "story": "plot",
    "鍓ф儏": "plot",
    "鍓ф儏鎽樿": "plot",
    "quotes": "quotes",
    "quote": "quotes",
    "dialogue": "quotes",
    "鍙拌瘝": "quotes",
    "鍙拌瘝鎽樺綍": "quotes",
    "wiki": "wiki",
    "鐧剧": "wiki",
    "user": "user",
    "manual": "user",
    "user-description": "user",
    "鐢ㄦ埛": "user",
    "鐢ㄦ埛鎻忚堪": "user",
}
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
CANON_PREFIXES = {
    "identity": "## Basic Identity",
    "basic": "## Basic Identity",
    "attribute": "## Setting Attributes",
    "setting": "## Setting Attributes",
    "event": "## Key Plot Events",
    "plot": "## Key Plot Events",
    "relation": "## Confirmed Relationships",
    "relationship": "## Confirmed Relationships",
    "official": "## Official Statements And Notes",
    "note": "## Official Statements And Notes",
}
PERSONA_PREFIXES = {
    "behavior": "## Behavior Patterns",
    "emotion": "## Emotional Tendencies",
    "interaction": "## Interaction Style",
    "progression": "## Relationship Progression",
    "relationship": "## Relationship Progression",
    "boundary": "## Boundaries And Preferences",
    "preference": "## Boundaries And Preferences",
}
STYLE_PREFIXES = {
    "address": "## Address Patterns",
    "rhythm": "## Rhythm And Sentence Shape",
    "sentence": "## Rhythm And Sentence Shape",
    "tic": "## Verbal Tics",
    "verbal": "## Verbal Tics",
    "example": "## Short Example Lines",
    "line": "## Short Example Lines",
}
INTERACTIVE_SENTINEL = "END"


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


def normalize_source_types(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_SOURCE_TYPES)
    normalized: list[str] = []
    for item in raw.replace("，", ",").split(","):
        token = item.strip().lower()
        if not token:
            continue
        normalized_token = SOURCE_TYPE_SYNONYMS.get(token)
        if normalized_token is None:
            raise ValueError(f"Unsupported source type: {item.strip()}")
        if normalized_token not in normalized:
            normalized.append(normalized_token)
    return normalized or list(DEFAULT_SOURCE_TYPES)


def parse_bool_flag(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "t", "yes", "y", "允许", "允许推断", "允许补充", "可以", "可以补充"}:
        return True
    if normalized in {"0", "false", "f", "no", "n", "不允许", "不允许推断", "不要补充", "不可以"}:
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


def prompt_required(prompt: str, default: str | None = None) -> str:
    shown_default = default if default else None
    suffix = f" [{shown_default}]" if shown_default else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if shown_default is not None:
            return shown_default
        print("This field is required.")


def prompt_yes_no(prompt: str, default: bool = False) -> bool:
    default_label = "Y/n" if default else "y/N"
    while True:
        value = input(f"{prompt} [{default_label}]: ").strip()
        if not value:
            return default
        try:
            return parse_bool_flag(value)
        except ValueError:
            print("Please answer yes or no.")


def prompt_choice(
    prompt: str,
    choices: dict[str, str],
    default_key: str | None = None,
    labels: dict[str, str] | None = None,
    aliases: dict[str, str] | None = None,
) -> str:
    default_suffix = f" [{default_key}]" if default_key else ""
    while True:
        print(prompt)
        for key, value in choices.items():
            label = labels.get(value, value) if labels else value
            print(f"{key}. {label}")
        value = input(f"Choose one{default_suffix}: ").strip()
        if not value and default_key:
            value = default_key
        normalized_value = value.strip().lower()
        if aliases and normalized_value in aliases:
            return aliases[normalized_value]
        if value in choices:
            return choices[value]
        print("Please choose a valid option.")


def prompt_multiline(prompt: str) -> str:
    print(f"{prompt} Finish with a line containing only {INTERACTIVE_SENTINEL}.")
    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == INTERACTIVE_SENTINEL:
            break
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def read_source_paths(raw_paths: str) -> tuple[list[str], str]:
    paths: list[str] = []
    contents: list[str] = []
    for raw_line in raw_paths.splitlines():
        candidate = raw_line.strip()
        if not candidate:
            continue
        path = Path(candidate)
        if not path.exists():
            raise FileNotFoundError(f"Source path not found: {candidate}")
        paths.append(candidate)
        contents.append(path.read_text(encoding="utf-8"))
    if not paths:
        raise ValueError("At least one source path is required when input mode is file_path.")
    return paths, "\n\n".join(contents).strip()


def build_slot_state(existing: dict) -> dict:
    return {
        "source_policy": existing.get("source_decision_policy"),
        "input_mode": existing.get("input_mode"),
        "character_name": existing.get("character_name") or existing.get("requested_character_name"),
        "source_work": existing.get("source_work"),
        "material_types": existing.get("source_types"),
        "allow_low_confidence_persona": existing.get("allow_low_confidence_persona"),
        "archive_mirror": existing.get("archive_mirror"),
    }


def infer_material_types_from_policy(source_policy: str) -> list[str]:
    if source_policy == "user_only":
        return normalize_source_types("user")
    if source_policy == "official_wiki_only":
        return normalize_source_types("official,wiki")
    if source_policy == "official_plus_user":
        return normalize_source_types("official,user")
    return normalize_source_types("official")


def compute_missing_slots(slot_state: dict, source_policy: str | None) -> list[str]:
    required = ["source_policy", "character_name", "material_types", "allow_low_confidence_persona", "archive_mirror"]
    if source_policy in {"user_only", "official_plus_user"}:
        required.append("input_mode")
    if source_policy != "official_quick" and slot_state.get("source_work") is None:
        required.append("source_work")
    return [slot for slot in CANONICAL_SLOTS if slot in required and slot_state.get(slot) is None]


def normalize_note_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("- "):
        stripped = stripped[2:].strip()
    return stripped


def parse_prefixed_notes(
    raw: str,
    headers: list[str],
    prefix_map: dict[str, str],
    default_header: str,
) -> dict[str, list[str]]:
    bucket = {header: [] for header in headers}
    for raw_line in raw.splitlines():
        line = normalize_note_line(raw_line)
        if not line:
            continue
        if ":" in line:
            prefix, value = line.split(":", 1)
            header = prefix_map.get(prefix.strip().lower())
            if header:
                cleaned = value.strip()
                if cleaned:
                    bucket[header].append(cleaned)
                continue
        bucket[default_header].append(line)
    return bucket


def render_markdown_from_sections(headers: list[str], sections: dict[str, list[str]]) -> str:
    blocks = []
    for header in headers:
        lines = sections.get(header) or []
        body = "\n".join(f"- {line}" for line in lines) if lines else SECTION_PLACEHOLDERS[header]
        blocks.append(f"{header}\n\n{body}")
    return "\n\n".join(blocks) + "\n"


def merge_section_defaults(
    sections: dict[str, list[str]],
    defaults: dict[str, list[str]],
) -> dict[str, list[str]]:
    merged = {header: list(sections.get(header, [])) for header in defaults}
    for header, lines in defaults.items():
        if not merged[header]:
            merged[header] = list(lines)
    return merged


def build_minimal_persona_defaults(target_use: str, allow_low_confidence: bool) -> dict[str, list[str]]:
    if allow_low_confidence:
        return {
            "## Behavior Patterns": [
                f"Based on limited intake material, keep the roleplay aligned with the user's stated goal: {target_use}."
            ],
            "## Emotional Tendencies": [
                "When evidence is thin, express emotions conservatively instead of inventing strong unverified reactions."
            ],
            "## Interaction Style": [
                "Prefer clear, supportive, character-facing replies and mark uncertain traits through restraint rather than new canon claims."
            ],
            "## Relationship Progression": [
                "Let familiarity grow gradually from the ongoing conversation instead of assuming deep trust immediately."
            ],
            "## Boundaries And Preferences": [
                "Do not present speculative traits as confirmed facts, even when low-confidence persona inference is allowed."
            ],
        }
    return {
        "## Behavior Patterns": [
            "Insufficient persona evidence is currently available, so keep behavior restrained and avoid strong unverified traits."
        ],
        "## Emotional Tendencies": [
            "Default to mild, controlled emotional expression until more source-backed characterization is added."
        ],
        "## Interaction Style": [
            "Answer in a neutral, steady roleplay voice and avoid claiming inner motives that were not provided."
        ],
        "## Relationship Progression": [
            "Do not force closeness or hostility without explicit support from later materials or user guidance."
        ],
        "## Boundaries And Preferences": [
            "If a response depends on missing characterization, stay conservative rather than fabricating details."
        ],
    }


def build_minimal_style_defaults(target_use: str) -> dict[str, list[str]]:
    return {
        "## Address Patterns": [
            "Use direct address suitable for the current conversation and avoid overcommitting to honorific habits not yet supported."
        ],
        "## Rhythm And Sentence Shape": [
            f"Keep sentence rhythm stable and readable for the stated use case: {target_use}."
        ],
        "## Verbal Tics": [
            "Avoid adding signature catchphrases unless they were explicitly provided in the intake."
        ],
        "## Short Example Lines": [
            "I am here, so tell me what you need.",
        ],
    }


def build_minimal_canon_defaults() -> dict[str, list[str]]:
    return {
        "## Basic Identity": [],
        "## Setting Attributes": [
            "No additional confirmed setting attributes were supplied in the current intake bundle."
        ],
        "## Key Plot Events": [
            "No explicit plot events were supplied in the current intake bundle."
        ],
        "## Confirmed Relationships": [
            "No explicit relationships were supplied in the current intake bundle."
        ],
        "## Official Statements And Notes": [
            "No official statements were supplied in the current intake bundle."
        ],
    }


def build_canon_markdown(name: str, source_work: str, note_blocks: dict[str, list[str]]) -> str:
    sections = {header: list(note_blocks.get(header, [])) for header in CANON_HEADERS}
    sections = merge_section_defaults(sections, build_minimal_canon_defaults())
    identity = sections["## Basic Identity"]
    if name:
        identity.insert(0, f"Name: {name}")
    if source_work:
        identity.append(f"Source Work: {source_work}")
    return render_markdown_from_sections(CANON_HEADERS, sections)


def build_persona_markdown(
    note_blocks: dict[str, list[str]],
    target_use: str,
    allow_low_confidence: bool,
) -> str:
    sections = {header: list(note_blocks.get(header, [])) for header in PERSONA_HEADERS}
    sections = merge_section_defaults(
        sections,
        build_minimal_persona_defaults(target_use, allow_low_confidence),
    )
    return render_markdown_from_sections(PERSONA_HEADERS, sections)


def build_style_markdown(note_blocks: dict[str, list[str]], target_use: str) -> str:
    sections = {header: list(note_blocks.get(header, [])) for header in STYLE_HEADERS}
    sections = merge_section_defaults(sections, build_minimal_style_defaults(target_use))
    return render_markdown_from_sections(STYLE_HEADERS, sections)


def build_normalized_payload(
    intake: dict,
    raw_material_notes: str,
    canon_notes: str,
    persona_notes: str,
    style_notes: str,
    source_paths: list[str],
    updated_at: str,
) -> dict:
    entries: list[dict] = []

    def push_entry(kind: str, text: str, entry_id: str) -> None:
        if text.strip():
            entries.append(
                {
                    "entry_id": entry_id,
                    "text": text.strip(),
                    "kind": kind,
                    "line_start": 1,
                    "line_end": len(text.splitlines()),
                }
            )

    push_entry("source_summary", raw_material_notes, "intake-001")
    push_entry("canon_notes", canon_notes, "intake-002")
    push_entry("persona_notes", persona_notes, "intake-003")
    push_entry("style_notes", style_notes, "intake-004")

    return {
        "schema_version": "0.4",
        "source": {
            "source_type": "interactive-intake",
            "input_path": "",
            "normalized_at": updated_at,
            "source_types": intake["source_types"],
            "source_decision_policy": intake["source_decision_policy"],
            "input_mode": intake["input_mode"],
            "search_scope": intake.get("search_scope", DEFAULT_SEARCH_SCOPE),
            "archive_mirror": intake.get("archive_mirror", True),
            "source_paths": source_paths,
        },
        "intake": {
            "character_name": intake["character_name"],
            "source_work": intake["source_work"],
            "target_use": intake["target_use"],
            "source_types": intake["source_types"],
            "allow_low_confidence_persona": intake["allow_low_confidence_persona"],
            "source_decision_policy": intake["source_decision_policy"],
            "input_mode": intake["input_mode"],
            "search_scope": intake.get("search_scope", DEFAULT_SEARCH_SCOPE),
            "archive_mirror": intake.get("archive_mirror", True),
            "source_paths": source_paths,
            "confirmed": intake["confirmed"],
        },
        "entries": entries,
    }


def build_child_skill(name: str, slug: str, target_use: str, allow_low_confidence: bool) -> str:
    confidence_line = (
        "Low-confidence persona inference is allowed when material is thin, but it must stay clearly subordinate to canon."
        if allow_low_confidence
        else "When persona evidence is thin, stay conservative and do not improvise strong characterization."
    )
    return (
        f"---\n"
        f"name: {slug}\n"
        f"description: OpenClaw-compatible role skill for {name}. Answer directly in {name}'s voice using canon, persona, style examples, and silent conditional memory.\n"
        f"metadata: {{openclaw: {{requires: {{bins: [python3]}}}}}}\n"
        f"---\n\n"
        f"# {name}\n\n"
        f"Use this skill to roleplay or answer as {name} inside OpenClaw or other AgentSkills-compatible runtimes.\n\n"
        f"## Intent\n\n"
        f"- Preferred use: {target_use}\n"
        f"- Runtime slug: `{slug}`\n\n"
        f"## Silent Runtime Order\n\n"
        f"1. Read `canon.md` first for facts, setting, events, and relationships.\n"
        f"2. Read `persona.md` for behavior patterns, emotional tendencies, and interaction strategy.\n"
        f"3. Read `style_examples.md` for wording texture, cadence, and short response flavor.\n"
        f"4. Only when the latest user turn suggests past context, long-term preference, nickname, or relationship state may matter, silently call `python3 ../../../scripts/memory_prepare.py --character-slug {slug} --user-message \"<latest user message>\"`.\n"
        f"5. If `memory_prepare.py` returns `should_read: true`, use the returned `memory_context`. Do not make a separate fetch call in normal operation.\n"
        f"6. Reply directly in character. Do not mention memory gates, routers, scripts, or checks.\n"
        f"7. If `memory_prepare.py` returns `should_write_after_reply: true`, silently call `python3 ../../../scripts/memory_commit.py --character-slug {slug} --user-message \"<latest user message>\" --assistant-message \"<final reply>\"` after the reply.\n"
        f"8. If `memory_prepare.py` returns `should_summarize_after_reply: true`, silently call `python3 ../../../scripts/memory_summarize.py --character-slug {slug}` after the reply.\n\n"
        f"## Conditional Memory System\n\n"
        f"- Memory is opt-in per turn, not always-on.\n"
        f"- Read `../../../references/memory_policy.md` before any memory action.\n"
        f"- Memory data lives in `../../../.dreamlover-data/memory.sqlite3`, not inside this skill package.\n"
        f"- Default behavior: no memory read and no memory write.\n"
        f"- Ordinary small talk should usually skip memory scripts entirely.\n"
        f"- If `python3` is not available, skip memory scripts and continue in no-memory mode.\n"
        f"- If no relevant memory exists, answer naturally and do not fabricate shared history.\n\n"
        f"## Rules\n\n"
        f"- Enter the character voice immediately. Do not explain internal workflow to the user.\n"
        f"- Never narrate internal checks, tools, or hidden preparation steps.\n"
        f"- If a memory lookup fails and it affects the answer, use one short natural sentence instead of exposing internal tooling.\n"
        f"- Never promote persona inference into canon during live conversation.\n"
        f"- Never say \"we talked about this before\" unless fetched memory actually supports it.\n"
        f"- If facts and style conflict, facts from `canon.md` win.\n"
        f"- If the behavior feels off, improve `persona.md` before changing canon.\n"
        f"- If the voice feels weak, improve `style_examples.md` before changing canon.\n"
        f"- {confidence_line}\n"
    )


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
    if install_scope == "both" and primary_dir != default_archive_dir:
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
    write_json(package_dir / "sources" / "normalized.json", normalized_payload)


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


def interactive_intake(existing: dict) -> dict:
    print("Interactive intake mode for character skill generation.")
    slot_state = build_slot_state(existing)
    slot_state["archive_mirror"] = existing.get(
        "archive_mirror",
        existing.get("install_scope", "both") in {"both", "archive"},
    )

    if slot_state["source_policy"] is None:
        slot_state["source_policy"] = prompt_choice(
            "Choose a source completion policy.",
            SOURCE_DECISION_POLICIES,
            "1",
            SOURCE_DECISION_LABELS,
            SOURCE_POLICY_ALIASES,
        )
    source_decision_policy = slot_state["source_policy"]

    requested_name = existing.get("requested_character_name") or existing.get("character_name") or ""
    if slot_state["character_name"] is None and requested_name:
        if prompt_yes_no(f'Use "{requested_name}" as the character name', True):
            slot_state["character_name"] = requested_name
        else:
            slot_state["character_name"] = prompt_required("Character name")
    elif slot_state["character_name"] is None:
        slot_state["character_name"] = prompt_required("Character name")
    character_name = slot_state["character_name"]

    if source_decision_policy == "official_quick":
        effective_slug = slugify(character_name)
        return {
            "slug": effective_slug,
            "character_name": character_name,
            "source_work": existing.get("source_work", ""),
            "target_use": existing.get("target_use") or "openclaw roleplay conversation",
            "source_types": infer_material_types_from_policy(source_decision_policy),
            "allow_low_confidence_persona": existing.get("allow_low_confidence_persona", False),
            "source_decision_policy": source_decision_policy,
            "input_mode": DEFAULT_INPUT_MODE,
            "search_scope": "medium",
            "source_paths": [],
            "archive_mirror": slot_state["archive_mirror"],
            "raw_material_notes": "",
            "canon_notes": "",
            "persona_notes": "",
            "style_notes": "",
            "confirmed": False,
        }

    if source_decision_policy in {"user_only", "official_plus_user"} and slot_state["input_mode"] is None:
        slot_state["input_mode"] = prompt_choice(
            "Choose how you will provide the source material.",
            INPUT_MODES,
            "1",
            INPUT_MODE_LABELS,
            INPUT_MODE_ALIASES,
        )
    input_mode = slot_state["input_mode"] or DEFAULT_INPUT_MODE

    if slot_state["source_work"] is None:
        slot_state["source_work"] = input("Source work (leave blank if this is a fully original character): ").strip()
    source_work = slot_state["source_work"]

    search_scope = existing.get("search_scope", DEFAULT_SEARCH_SCOPE)
    if source_decision_policy in {"official_wiki_only", "official_plus_user"} and source_work:
        search_scope = prompt_choice(
            "Choose the public search scope.",
            SEARCH_SCOPES,
            "2",
            SEARCH_SCOPE_LABELS,
            SEARCH_SCOPE_ALIASES,
        )

    source_paths: list[str] = []
    raw_material_notes = ""
    if input_mode == "file_path":
        raw_path_block = prompt_multiline("Provide one or more file paths for the source material.")
        source_paths, raw_material_notes = read_source_paths(raw_path_block)
    elif input_mode == "direct_text":
        raw_material_notes = prompt_multiline("Paste the source text or notes you want the generator to use.")

    if slot_state["material_types"] is None:
        slot_state["material_types"] = infer_material_types_from_policy(source_decision_policy)

    if slot_state["allow_low_confidence_persona"] is None:
        slot_state["allow_low_confidence_persona"] = prompt_yes_no(
            "If the materials are not enough, may I add a little personality supplementation for you",
            False,
        )
    allow_low_confidence = slot_state["allow_low_confidence_persona"]

    canon_notes = ""
    persona_notes = ""
    style_notes = ""
    effective_slug = slugify(character_name)
    target_use = existing.get("target_use") or "openclaw roleplay conversation"

    return {
        "slug": effective_slug,
        "character_name": character_name,
        "source_work": source_work,
        "target_use": target_use,
        "source_types": slot_state["material_types"],
        "allow_low_confidence_persona": allow_low_confidence,
        "source_decision_policy": source_decision_policy,
        "input_mode": input_mode,
        "search_scope": search_scope,
        "source_paths": source_paths,
        "archive_mirror": slot_state["archive_mirror"],
        "raw_material_notes": raw_material_notes,
        "canon_notes": canon_notes,
        "persona_notes": persona_notes,
        "style_notes": style_notes,
        "confirmed": False,
    }


def build_generated_confirmation_summary(
    intake: dict,
    canon_text: str,
    persona_text: str,
    style_text: str,
) -> list[str]:
    persona_behavior = choose_section_body(
        parse_section_segments(persona_text, PERSONA_HEADERS)["## Behavior Patterns"],
        SECTION_PLACEHOLDERS["## Behavior Patterns"],
    ).splitlines()[0].lstrip("- ").strip()
    style_line = choose_section_body(
        parse_section_segments(style_text, STYLE_HEADERS)["## Short Example Lines"],
        SECTION_PLACEHOLDERS["## Short Example Lines"],
    ).splitlines()[0].lstrip("- ").strip()
    summary_lines = [
        f"- Character: {intake['character_name']}",
        f"- Slug: {intake['slug']}",
        f"- Source policy: {SOURCE_DECISION_LABELS.get(intake['source_decision_policy'], intake['source_decision_policy'])}",
        f"- Input mode: {INPUT_MODE_LABELS.get(intake['input_mode'], intake['input_mode'])}",
        f"- Source work: {intake['source_work'] or 'original character / not provided'}",
        f"- Search scope: {SEARCH_SCOPE_LABELS.get(intake.get('search_scope', DEFAULT_SEARCH_SCOPE), intake.get('search_scope', DEFAULT_SEARCH_SCOPE))}",
        f"- Low-confidence persona: {'yes' if intake['allow_low_confidence_persona'] else 'no'}",
        f"- Persona preview: {persona_behavior}",
        f"- Style preview: {style_line}",
    ]
    return summary_lines


def build_interactive_outputs(existing: dict, forced_slug: str | None) -> tuple[str, str, str, dict, str, dict]:
    intake = interactive_intake(existing)
    if forced_slug:
        intake["slug"] = forced_slug

    updated_at = utc_now()
    canon_blocks = parse_prefixed_notes(intake["canon_notes"], CANON_HEADERS, CANON_PREFIXES, "## Basic Identity")
    persona_blocks = parse_prefixed_notes(
        intake["persona_notes"],
        PERSONA_HEADERS,
        PERSONA_PREFIXES,
        "## Behavior Patterns",
    )
    style_blocks = parse_prefixed_notes(
        intake["style_notes"],
        STYLE_HEADERS,
        STYLE_PREFIXES,
        "## Address Patterns",
    )
    canon_text = build_canon_markdown(intake["character_name"], intake["source_work"], canon_blocks)
    persona_text = build_persona_markdown(
        persona_blocks,
        intake["target_use"],
        intake["allow_low_confidence_persona"],
    )
    style_text = build_style_markdown(style_blocks, intake["target_use"])
    normalized_payload = build_normalized_payload(
        intake,
        intake["raw_material_notes"],
        intake["canon_notes"],
        intake["persona_notes"],
        intake["style_notes"],
        intake["source_paths"],
        updated_at,
    )
    skill_text = build_child_skill(
        intake["character_name"],
        intake["slug"],
        intake["target_use"],
        intake["allow_low_confidence_persona"],
    )
    print("Review the generated draft summary before any files are written:")
    print("\n".join(build_generated_confirmation_summary(intake, canon_text, persona_text, style_text)))
    intake["confirmed"] = prompt_yes_no("Confirm this generated draft and allow file creation", False)
    if not intake["confirmed"]:
        raise SystemExit(
            json.dumps(
                {
                    "status": "aborted",
                    "reason": "intake_not_confirmed",
                    "message": "Hard intake gate blocked generation before any files were written.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return canon_text, persona_text, style_text, normalized_payload, skill_text, intake


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
    parser.add_argument("--interactive", action="store_true", help="Run an intake-first interactive session for create or update.")
    parser.add_argument("--name", help="Character display name.")
    parser.add_argument("--source-work", default="", help="Source work name.")
    parser.add_argument("--target-use", default="", help="Target roleplay use or scenario.")
    parser.add_argument("--source-types", help="Comma-separated source types: official, plot, quotes, wiki, user.")
    parser.add_argument("--allow-low-confidence-persona", help="Whether low-confidence persona inference is allowed: yes/no.")
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

    effective_slug = args.slug or (slugify(args.name) if args.name else None)
    if not effective_slug and not args.interactive:
        raise SystemExit("--slug is required for create and update unless --interactive is used")

    placeholder_slug = effective_slug or "interactive-intake"
    primary_dir, archive_dir = package_targets(root, placeholder_slug, args.install_scope, args.output_root)
    meta_candidates = [primary_dir / "meta.json"]
    if archive_dir is not None:
        meta_candidates.append(archive_dir / "meta.json")
    existing = load_existing_meta(meta_candidates)
    if args.name:
        existing.setdefault("requested_character_name", args.name)
    elif args.slug:
        existing.setdefault("requested_character_name", args.slug)

    if args.interactive:
        canon_text, persona_text, style_text, normalized_payload, skill_text, intake = build_interactive_outputs(existing, args.slug)
        name = intake["character_name"]
        effective_slug = intake["slug"]
        source_work = intake["source_work"]
        target_use = intake["target_use"]
        source_types = intake["source_types"]
        allow_low_confidence = intake["allow_low_confidence_persona"]
        primary_dir, archive_dir = package_targets(root, effective_slug, args.install_scope, args.output_root)
    else:
        canon_existing = load_existing_text([primary_dir / "canon.md"] + ([archive_dir / "canon.md"] if archive_dir else []))
        persona_existing = load_existing_text([primary_dir / "persona.md"] + ([archive_dir / "persona.md"] if archive_dir else []))
        style_existing = load_existing_text([primary_dir / "style_examples.md"] + ([archive_dir / "style_examples.md"] if archive_dir else []))
        canon_text = ensure_sections(read_text(args.canon_file) or canon_existing, CANON_HEADERS)
        persona_text = ensure_sections(read_text(args.persona_file) or persona_existing, PERSONA_HEADERS)
        style_text = ensure_sections(read_text(args.style_file) or style_existing, STYLE_HEADERS)
        name = args.name or existing.get("character_name") or effective_slug or "character"
        source_work = args.source_work or existing.get("source_work", "")
        target_use = args.target_use or existing.get("target_use", "roleplay conversation")
        source_types = normalize_source_types(args.source_types or ",".join(existing.get("source_types", DEFAULT_SOURCE_TYPES)))
        allow_low_confidence = parse_bool_flag(
            args.allow_low_confidence_persona,
            existing.get("allow_low_confidence_persona", False),
        )
        source_decision_policy = existing.get("source_decision_policy", DEFAULT_SOURCE_DECISION_POLICY)
        input_mode = existing.get("input_mode", DEFAULT_INPUT_MODE)
        normalized_payload = {
            "schema_version": "0.4",
            "source": {
                "source_type": "manual",
                "input_path": "",
                "normalized_at": utc_now(),
                "source_types": source_types,
                "source_decision_policy": source_decision_policy,
                "input_mode": input_mode,
                "search_scope": existing.get("search_scope", DEFAULT_SEARCH_SCOPE),
                "archive_mirror": existing.get("archive_mirror", True),
                "source_paths": existing.get("source_paths", []),
            },
            "intake": {
                "slug": effective_slug,
                "character_name": name,
                "source_work": source_work,
                "target_use": target_use,
                "source_types": source_types,
                "allow_low_confidence_persona": allow_low_confidence,
                "source_decision_policy": source_decision_policy,
                "input_mode": input_mode,
                "search_scope": existing.get("search_scope", DEFAULT_SEARCH_SCOPE),
                "archive_mirror": existing.get("archive_mirror", True),
                "source_paths": existing.get("source_paths", []),
                "confirmed": True,
            },
            "entries": [],
        }
        skill_text = build_child_skill(name, effective_slug or "character", target_use, allow_low_confidence)

    validate_cross_headers(canon_text, PERSONA_HEADERS + STYLE_HEADERS, "canon")
    validate_cross_headers(persona_text, CANON_HEADERS + STYLE_HEADERS, "persona")
    validate_cross_headers(style_text, CANON_HEADERS + PERSONA_HEADERS, "style_examples")

    created_at = existing.get("created_at", utc_now())
    updated_at = utc_now()
    meta = {
        "slug": effective_slug,
        "character_name": name,
        "source_work": source_work,
        "target_use": target_use,
        "source_types": source_types,
        "allow_low_confidence_persona": allow_low_confidence,
        "source_decision_policy": normalized_payload["intake"]["source_decision_policy"],
        "input_mode": normalized_payload["intake"]["input_mode"],
        "search_scope": normalized_payload["intake"].get("search_scope", DEFAULT_SEARCH_SCOPE),
        "archive_mirror": normalized_payload["intake"].get("archive_mirror", True),
        "source_paths": normalized_payload["intake"].get("source_paths", []),
        "layout_version": "0.6",
        "created_at": created_at,
        "updated_at": updated_at,
        "primary_path": relative_path(root, primary_dir),
        "archive_path": relative_path(root, archive_dir),
        "install_scope": args.install_scope,
    }
    normalized_payload["source"]["normalized_at"] = updated_at
    normalized_payload["intake"]["slug"] = effective_slug
    normalized_payload["intake"]["character_name"] = name

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




