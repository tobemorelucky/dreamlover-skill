from __future__ import annotations

import argparse
import json
import re

from memory_store import connect_memory_db, count_unsummarized_episodes

READ_PHRASES = [
    "上次",
    "之前",
    "还记得",
    "答应我",
    "我们聊过",
]

CONTEXT_CONTINUATION_PHRASES = [
    "接着",
    "继续",
    "刚才说到",
    "那个项目",
    "这个项目",
    "进度",
    "昵称",
    "偏好",
    "关系",
    "长期项目",
]

WRITE_STABLE_PHRASES = [
    "以后都喜欢你叫我",
    "以后叫我",
    "你可以叫我",
    "我的昵称是",
    "我平时喜欢",
    "我通常喜欢",
    "我一般喜欢",
]

WRITE_EVENT_PHRASES = [
    "今天我们",
    "刚才我们",
    "一起",
    "第一次",
    "终于",
    "发生了",
]

WRITE_RELATIONSHIP_PHRASES = [
    "我们现在",
    "朋友",
    "恋人",
    "搭档",
    "信任你",
    "不信任你",
]

WRITE_PROMISE_PHRASES = [
    "明天",
    "下次",
    "以后",
    "记得",
    "答应",
    "约好",
    "待会",
    "稍后",
]

WRITE_BOUNDARY_PHRASES = [
    "不要",
    "别",
    "不许",
    "别再",
    "边界",
]

EMOTION_WORDS = [
    "难过",
    "崩溃",
    "生气",
    "害怕",
    "焦虑",
    "开心",
    "兴奋",
    "委屈",
]


def contains_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def detect_read_reasons(text: str, relationship_exists: bool) -> list[str]:
    reasons: list[str] = []
    if contains_any(text, READ_PHRASES):
        reasons.append("user_explicitly_referenced_past_context")
    if contains_any(text, CONTEXT_CONTINUATION_PHRASES):
        reasons.append("current_turn_depends_on_context_continuation")
    if re.search(r"(偏好|昵称|称呼|关系|长期项目|项目进度)", text):
        reasons.append("user_referenced_stable_preference_or_long_term_state")
    if relationship_exists and re.search(r"(我们|关系|叫我|答应)", text):
        reasons.append("relationship_consistency_requires_memory")
    return list(dict.fromkeys(reasons))


def detect_write_reasons(text: str) -> list[str]:
    reasons: list[str] = []
    if contains_any(text, WRITE_STABLE_PHRASES) or re.search(r"(以后都|平时|通常|一直).*(喜欢|叫我)", text):
        reasons.append("stable_preference_or_long_term_fact")
    if contains_any(text, WRITE_EVENT_PHRASES):
        reasons.append("important_shared_event")
    if contains_any(text, WRITE_RELATIONSHIP_PHRASES):
        reasons.append("relationship_state_changed")
    if contains_any(text, WRITE_PROMISE_PHRASES):
        reasons.append("future_commitment_or_todo")
    if contains_any(text, WRITE_BOUNDARY_PHRASES) or contains_any(text, EMOTION_WORDS) or text.count("!") + text.count("！") >= 2:
        reasons.append("high_emotion_or_boundary_signal")
    return list(dict.fromkeys(reasons))


def main() -> None:
    parser = argparse.ArgumentParser(description="Route conditional memory read/write decisions for a child skill.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-message", required=True)
    parser.add_argument("--assistant-message", default="")
    parser.add_argument("--phase", choices=["pre", "post"], default="pre")
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--summary-threshold", type=int, default=8)
    parser.add_argument("--data-root")
    args = parser.parse_args()

    with connect_memory_db(args.data_root) as connection:
        relationship_row = connection.execute(
            """
            SELECT relationship_label, trust_level, closeness_level, status_summary
            FROM relationship_state
            WHERE character_slug = ? AND user_id = ?
            """,
            (args.character_slug, args.user_id),
        ).fetchone()
        relationship_exists = relationship_row is not None
        unsummarized_count = count_unsummarized_episodes(connection, args.character_slug, args.user_id)

    read_reasons = detect_read_reasons(args.user_message, relationship_exists)
    write_reasons = detect_write_reasons(args.user_message) if args.phase == "post" else []
    projected_unsummarized = unsummarized_count + (1 if write_reasons else 0)
    should_summarize = args.phase == "post" and projected_unsummarized >= args.summary_threshold

    payload = {
        "phase": args.phase,
        "should_read": bool(read_reasons),
        "should_write": bool(write_reasons),
        "should_summarize": should_summarize,
        "read_reasons": read_reasons,
        "write_reasons": write_reasons,
        "summarize_reason": "unsummarized_threshold_reached" if should_summarize else "",
        "state": {
            "relationship_state_exists": relationship_exists,
            "unsummarized_episodic_count": unsummarized_count,
            "summary_threshold": args.summary_threshold,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
