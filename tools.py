
# Compensation rates and keyword rules

DELAY_BASE_RATE = 0.05
# 5% of shipment value

DELAY_URGENT_MULTIPLIER = 2.0
# Double the rate if the report signals urgency

URGENT_SIGNALS = ["urgent", "critical", "asap", "time-sensitive"]

SEVERE_DAMAGE_KEYWORDS = [
    "shattered", "destroyed", "unusable", "crushed"
]

MINOR_DAMAGE_KEYWORDS = [
    "dented", "scratched", "scuffed", "chipped"
]


def calculate_delay_compensation(
    shipment_value: float,
    report_text: str
) -> dict:
    """Delay compensation: a flat percentage of shipment value,
    doubled if the report signals urgency."""

    text = report_text.lower()

    urgent = any(sig in text for sig in URGENT_SIGNALS)

    rate = DELAY_BASE_RATE * (
        DELAY_URGENT_MULTIPLIER if urgent else 1.0
    )

    amount = round(shipment_value * rate, 2)

    reasoning = (
        f"Delay compensation at {rate * 100:.0f}% of shipment value"
        + (" (urgency signal detected)" if urgent else "")
        + f" = ${amount:.2f}."
    )

    return {"amount": amount, "reasoning": reasoning}


def calculate_damage_compensation(
    shipment_value: float,
    report_text: str
) -> dict:
    """Damage compensation: percentage of shipment value driven by
    the most severe keyword tier found in the report
    (severe=100%, minor=25%, unclear=50% default)."""

    text = report_text.lower()

    if any(k in text for k in SEVERE_DAMAGE_KEYWORDS):
        rate, tier = 1.0, "severe"
    elif any(k in text for k in MINOR_DAMAGE_KEYWORDS):
        rate, tier = 0.25, "minor"
    else:
        rate, tier = 0.5, "unclear severity, default"

    amount = round(shipment_value * rate, 2)

    reasoning = (
        f"Damage compensation at {rate * 100:.0f}% of shipment value "
        f"({tier}) = ${amount:.2f}."
    )

    return {"amount": amount, "reasoning": reasoning}


def calculate_lost_compensation(
    shipment_value: float,
    report_text: str
) -> dict:
    """Lost shipment compensation: always 100% of shipment value."""

    amount = round(shipment_value, 2)

    reasoning = (
        f"Lost shipment — full compensation of ${amount:.2f} "
        f"(100% of shipment value)."
    )

    return {"amount": amount, "reasoning": reasoning}
