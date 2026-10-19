
DAILY_LOG = []  # each entry is the final state dict returned by process_exception()


def record(final_state: dict) -> None:
    DAILY_LOG.append(final_state)


def generate_daily_summary() -> str:
    if not DAILY_LOG:
        return "No exceptions processed yet today."

    total_compensation = sum(e["compensation"] for e in DAILY_LOG)
    escalated = [e for e in DAILY_LOG if e["needs_approval"]]
    escalation_rate = round(100 * len(escalated) / len(DAILY_LOG))

    by_category = {}
    for e in DAILY_LOG:
        by_category[e["category"]] = (
            by_category.get(e["category"], 0.0) + e["compensation"]
        )

    costliest_category = (
        max(by_category, key=by_category.get) if by_category else "n/a"
    )

    lines = [
        f"Daily Triage Summary — {len(DAILY_LOG)} exception(s) processed"
    ]

    for i, e in enumerate(DAILY_LOG, 1):
        status = "ESCALATED" if e["needs_approval"] else "auto-resolved"
        lines.append(
            f"  {i}. {e['category']} | ${e['compensation']:.2f} — {status}"
        )

    lines.append(
        f"\nTotal compensation paid out: ${total_compensation:.2f}"
    )
    lines.append(
        f"Escalation rate: {escalation_rate}% "
        f"({len(escalated)}/{len(DAILY_LOG)})"
    )
    lines.append(
        f"Costliest category: {costliest_category} "
        f"(${by_category.get(costliest_category, 0):.2f})"
    )

    return "\n".join(lines)
