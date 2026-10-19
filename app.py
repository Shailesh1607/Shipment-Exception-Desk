
import gradio as gr
from pipeline import process_exception
import session


def format_triage_log():
    if not session.DAILY_LOG:
        return "_No exceptions processed yet today._"

    lines = []
    for i, e in enumerate(session.DAILY_LOG, 1):
        status = (
            "ESCALATED"
            if e["needs_approval"]
            else "auto-resolved"
        )
        lines.append(
            f"**{i}.** {e['category']} "
            f"${e['compensation']:.2f} — {status}"
        )

    return "\n\n".join(lines)


def on_submit(report_text, shipment_value, customer_tier):
    if not report_text.strip():
        return "Enter a report first.", format_triage_log(), ""

    result = process_exception(
        report_text,
        float(shipment_value),
        customer_tier
    )
    session.record(result)

    status = (
        "**ESCALATED to manager**"
        if result["needs_approval"]
        else "**Auto-resolved**"
    )

    outcome = (
        f"### Outcome: {status}\n\n"
        f"**Category:** {result['category']}\n\n"
        f"**Compensation:** ${result['compensation']:.2f} — "
        f"{result['compensation_reasoning']}\n\n"
        f"**Drafted message:**\n\n{result['message_draft']}\n\n"
        f"**Steps:** {' -> '.join(result['log'])}"
    )

    return outcome, format_triage_log(), ""


def daily_summary():
    return session.generate_daily_summary()


with gr.Blocks(title="Shipment Exception Desk") as demo:
    gr.Markdown("## Northwind Logistics — Shipment Exception Desk")

    with gr.Row():
        report_box = gr.Textbox(
            label="Exception report",
            lines=4,
            scale=2
        )

        with gr.Column(scale=1):
            value_box = gr.Number(
                label="Shipment value ($)",
                value=100
            )
            tier_box = gr.Dropdown(
                ["standard", "premium"],
                value="standard",
                label="Customer tier"
            )

    submit_btn = gr.Button("Process Exception")
    outcome_box = gr.Markdown(label="Outcome")

    gr.Markdown("### Daily Triage Log")
    log_box = gr.Markdown("_No exceptions processed yet today._")

    summary_btn = gr.Button("Get Daily Summary")
    summary_box = gr.Markdown()

    submit_btn.click(
        on_submit,
        inputs=[report_box, value_box, tier_box],
        outputs=[outcome_box, log_box, report_box]
    )

    summary_btn.click(
        daily_summary,
        outputs=summary_box
    )


if __name__ == "__main__":
    demo.launch()
