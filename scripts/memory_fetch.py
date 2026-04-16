from __future__ import annotations

import argparse
import json

from memory_store import connect_memory_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch relevant local memory for a child skill.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-message", required=True)
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--profile-limit", type=int, default=8)
    parser.add_argument("--episodic-limit", type=int, default=5)
    parser.add_argument("--summary-limit", type=int, default=3)
    parser.add_argument("--data-root")
    args = parser.parse_args()

    with connect_memory_db(args.data_root) as connection:
        relationship_row = connection.execute(
            """
            SELECT relationship_label, trust_level, closeness_level, status_summary, updated_at
            FROM relationship_state
            WHERE character_slug = ? AND user_id = ?
            """,
            (args.character_slug, args.user_id),
        ).fetchone()

        profile_rows = connection.execute(
            """
            SELECT memory_key, memory_value, confidence, source, updated_at
            FROM profile_memory
            WHERE character_slug = ? AND user_id = ?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (args.character_slug, args.user_id, args.profile_limit),
        ).fetchall()

        episodic_rows = connection.execute(
            """
            SELECT id, summary, event_type, emotional_intensity, source_excerpt, created_at
            FROM episodic_memory
            WHERE character_slug = ? AND user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (args.character_slug, args.user_id, args.episodic_limit),
        ).fetchall()

        summary_rows = connection.execute(
            """
            SELECT id, turn_start, turn_end, summary, created_at
            FROM conversation_summary
            WHERE character_slug = ? AND user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (args.character_slug, args.user_id, args.summary_limit),
        ).fetchall()

    payload = {
        "character_slug": args.character_slug,
        "user_id": args.user_id,
        "query": args.user_message,
        "has_memory": bool(relationship_row or profile_rows or episodic_rows or summary_rows),
        "relationship_state": dict(relationship_row) if relationship_row else None,
        "profile_memory": [dict(row) for row in profile_rows],
        "episodic_memory": [dict(row) for row in episodic_rows],
        "conversation_summary": [dict(row) for row in summary_rows],
        "guidance": [
            "Use only memory that is relevant to the current reply.",
            "If no memory is relevant, answer normally and do not pretend there is prior history.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
