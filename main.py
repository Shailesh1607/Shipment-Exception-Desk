
from pipeline import process_exception
from session import record, generate_daily_summary


SAMPLE_REPORTS = [
    {
        "report_text": (
            "Package arrived 2 days later than the estimated "
            "delivery date. Customer is complaining about the delay."
        ),
        "shipment_value": 800.0,
        "customer_tier": "standard",
    },
    {
        "report_text": (
            "The shipment appears to be completely lost — "
            "carrier has had no tracking updates."
        ),
        "shipment_value": 3000.0,
        "customer_tier": "premium",
    },
]


def main():
    print("=== Northwind Logistics -- Shipment Exception Desk ===\n")

    for report in SAMPLE_REPORTS:
        print(f"Report: {report['report_text']}")

        # Process the shipment exception
        result = process_exception(**report)

        # Record the processing result
        record(**result)

        # Determine the outcome
        status = (
            "ESCALATED to manager"
            if result["needs_approval"]
            else "auto-resolved"
        )

        # Display the results
        print(f"Category: {result['category']}")
        print(
            f"Compensation: ${result['compensation']:.2f}"
            f" -- {result['compensation_reason']}"
        )
        print(f"Outcome: {status}")
        print(f"Draft message: {result['message_draft']}")
        print(f"Steps: {' -> '.join(result['log'])}")
        print("-" * 60)

    # Display the daily summary
    print("\n=== Daily Triage Summary ===")
    print(generate_daily_summary())


if __name__ == "__main__":
    main()
