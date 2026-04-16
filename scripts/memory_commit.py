from __future__ import annotations

import argparse
import json
import re

from memory_store import connect_memory_db, utc_now


def clamp_intensity(value: int) -> int:
    return max(0, min(3, value))


def detect_emotional_intensity(text: str) -> int:
    score = 0
    score += min(2, text.count("!") + text.count("！"))
    if re.search(r"(难过|崩溃|生气|害怕|焦虑|开心|兴奋|委屈|别|不要|不许)", text):
        score += 1
    return clamp_intensity(score)


def extract_profile_updates(text: str) -> list[tuple[str, str]]:
    updates: list[tuple[str, str]] = []
    nickname_patterns = [
        r"以后都喜欢你叫我(?P<value>[^，。！？\n]{1,20})",
        r"以后叫我(?P<value>[^，。！？\n]{1,20})",
        r"你可以叫我(?P<value>[^，。！？\n]{1,20})",
        r"我的昵称是(?P<value>[^，。！？\n]{1,20})",
    ]
    for pattern in nickname_patterns:
        match = re.search(pattern, text)
        if match:
            updates.append(("preferred_name", match.group("value").strip()))
            break

    general_preference = re.search(r"(我平时|我通常|我一般)喜欢(?P<value>[^，。！？\n]{1,30})", text)
    if general_preference:
        updates.append(("general_preference", general_preference.group("value").strip()))

    boundary = re.search(r"(不要|别|不许)(?P<value>[^，。！？\n]{1,40})", text)
    if boundary:
        updates.append(("boundary_preference", boundary.group("value").strip()))

    return updates


def extract_relationship_update(text: str) -> tuple[str, int, int, str] | None:
    if "恋人" in text:
        return ("lover", 3, 3, text.strip())
    if "朋友" in text:
        return ("friend", 2, 2, text.strip())
    if "搭档" in text:
        return ("partner", 2, 2, text.strip())
    if "信任你" in text:
        return ("trusted", 3, 2, text.strip())
    if "不信任你" in text:
        return ("strained", 0, 0, text.strip())
    return None


def choose_event_type(text: str) -> str:
    if re.search(r"(明天|下次|以后|记得|答应|约好)", text):
        return "commitment"
    if re.search(r"(不要|别|不许|边界)", text):
        return "boundary"
    if re.search(r"(朋友|恋人|搭档|信任你|不信任你)", text):
        return "relationship"
    if re.search(r"(喜欢你叫我|昵称是|平时喜欢|通常喜欢|一般喜欢)", text):
        return "profile"
    return "event"


def summarize_event(text: str) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= 120:
        return cleaned
    return cleaned[:117] + "..."


def main() -> None:
    parser = argparse.ArgumentParser(description="Commit conditional local memory after a character reply.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-message", required=True)
    parser.add_argument("--assistant-message", default="")
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--data-root")
    args = parser.parse_args()

    now = utc_now()
    profile_updates = extract_profile_updates(args.user_message)
    relationship_update = extract_relationship_update(args.user_message)
    event_type = choose_event_type(args.user_message)
    emotional_intensity = detect_emotional_intensity(args.user_message)
    event_summary = summarize_event(args.user_message)

    with connect_memory_db(args.data_root) as connection:
        for key, value in profile_updates:
            connection.execute(
                """
                INSERT INTO profile_memory (
                    character_slug, user_id, memory_key, memory_value, confidence, source, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(character_slug, user_id, memory_key)
                DO UPDATE SET
                    memory_value = excluded.memory_value,
                    confidence = excluded.confidence,
                    source = excluded.source,
                    updated_at = excluded.updated_at
                """,
                (args.character_slug, args.user_id, key, value, 0.9, "memory_commit", now, now),
            )

        if relationship_update:
            connection.execute(
                """
                INSERT INTO relationship_state (
                    character_slug, user_id, relationship_label, trust_level, closeness_level, status_summary, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(character_slug, user_id)
                DO UPDATE SET
                    relationship_label = excluded.relationship_label,
                    trust_level = excluded.trust_level,
                    closeness_level = excluded.closeness_level,
                    status_summary = excluded.status_summary,
                    updated_at = excluded.updated_at
                """,
                (
                    args.character_slug,
                    args.user_id,
                    relationship_update[0],
                    relationship_update[1],
                    relationship_update[2],
                    relationship_update[3],
                    now,
                ),
            )

        cursor = connection.execute(
            """
            INSERT INTO episodic_memory (
                character_slug, user_id, summary, event_type, emotional_intensity, source_excerpt, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                args.character_slug,
                args.user_id,
                event_summary,
                event_type,
                emotional_intensity,
                args.user_message.strip(),
                now,
            ),
        )
        episodic_id = int(cursor.lastrowid)
        connection.commit()

    payload = {
        "character_slug": args.character_slug,
        "user_id": args.user_id,
        "profile_updates": [{"key": key, "value": value} for key, value in profile_updates],
        "relationship_update": {
            "relationship_label": relationship_update[0],
            "trust_level": relationship_update[1],
            "closeness_level": relationship_update[2],
            "status_summary": relationship_update[3],
        }
        if relationship_update
        else None,
        "episodic_memory": {
            "id": episodic_id,
            "summary": event_summary,
            "event_type": event_type,
            "emotional_intensity": emotional_intensity,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
