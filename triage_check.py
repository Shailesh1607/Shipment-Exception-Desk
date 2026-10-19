SCENARIOS = [
    {
        "label": "1. Mild delay, standard customer -> expect: delayed, auto-resolved",
        "report_text": "Package arrived 2 days later than the estimated delivery date. Customer ...",
        "shipment_value": 800.0,
        "customer_tier": "standard",
    },
    {
        "label": "2. High-value lost shipment, premium customer -> expect: lost, ESCALATED",
        "report_text": "The shipment appears to be completely lost — carrier has had no tra...",
        "shipment_value": 3000.0,
        "customer_tier": "premium",
    },
    {
        "label": "3. Minor damage, standard customer -> expect: damaged, auto-resolved",
        "report_text": "Box arrived with the corner dented and scratched, but the product is ...",
        "shipment_value": 150.0,
        "customer_tier": "standard",
    },
    {
        "label": "4. Garbled report -> expect: unknown, ESCALATED [regardless of value]",
        "report_text": "Hi so the thing with the order number and also the guy said something ...",
        "shipment_value": 40.0,
        "customer_tier": "standard",
    },
]