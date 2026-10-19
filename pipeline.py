
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import llm
from tools import (
    calculate_delay_compensation,
    calculate_damage_compensation,
    calculate_lost_compensation,
)

from chains import (
    classify_chain,
    escalate_chain,
    draft_email_chain,
)

# Keep your existing imports for the compensation
# functions, thresholds, and email chains here.

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You triage shipment exception reports for a logistics company. "
        "Read the report and classify it into exactly one word: "
        "'delayed', 'damaged', 'lost', or 'unknown' if it doesn't clearly "
        "fit any of those. Reply with that single word only, nothing else."
    ),
    ("human", "{report_text}"),
])

classify_chain = CLASSIFY_PROMPT | llm | StrOutputParser()


def process_exception(report_text, shipment_value, customer_tier):
    log = []

    raw_category = classify_chain.invoke(
        {"report_text": report_text}
    ).strip().lower()

    if raw_category == "delayed":
        category = "delayed"
        comp = calculate_delay_compensation(
            shipment_value, report_text
        )

    elif raw_category == "damaged":
        category = "damaged"
        comp = calculate_damage_compensation(
            shipment_value, report_text
        )

    elif raw_category == "lost":
        category = "lost"
        comp = calculate_lost_compensation(
            shipment_value, report_text
        )

    else:
        category = "unknown"
        comp = {
            "amount": 0.0,
            "reasoning": "Could not confidently classify this report."
        }

    log.append(f"Classified as '{category}'")
    log.append(
        f"Compensation calculated: ${comp['amount']:.2f}"
    )
    PREMIUM_ESCALATION_THRESHOLD = 100.0
    STANDARD_ESCALATION_THRESHOLD = 50.0
    threshold = (
        PREMIUM_ESCALATION_THRESHOLD
        if customer_tier == "premium"
        else STANDARD_ESCALATION_THRESHOLD
    )

    needs_approval = (
        category == "unknown"
        or comp["amount"] > threshold
    )

    chain_input = {
        "report_text": report_text,
        "category": category,
        "amount": comp["amount"],
        "reasoning": comp["reasoning"],
    }

    if needs_approval:
        message_draft = escalate_chain.invoke(chain_input)
        log.append("Escalated to manager for approval")
    else:
        message_draft = draft_email_chain.invoke(chain_input)
        log.append("Auto-resolved — drafted customer email")

    return {
        "report_text": report_text,
        "shipment_value": shipment_value,
        "customer_tier": customer_tier,
        "category": category,
        "compensation": comp["amount"],
        "compensation_reasoning": comp["reasoning"],
        "needs_approval": needs_approval,
        "message_draft": message_draft,
        "log": log,
    }
