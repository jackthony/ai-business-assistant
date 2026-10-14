#!/usr/bin/env python3
"""Monthly cost scenarios (USD). Usage: cost_scenarios.py PROVIDERS_JSON
PROVIDERS_JSON: [{"name": str, "monthly_fee_usd": float, "markup_pct": float, "per_msg_fee_usd": float}, ...]
Meta Peru rates (reference 1-oct-2026, pending confirmation in WABA Billing):
service 0.033 after 1000 free/number/month; utility 0.033; marketing 0.07733.
Prints a JSON list of scenarios. Pure arithmetic; every assumption is in the output."""
import json
import sys

SERVICE, UTILITY, MARKETING, FREE = 0.033, 0.033, 0.07733, 1000
providers = json.loads(sys.argv[1]) if sys.argv[1].lstrip().startswith("[") else json.load(open(sys.argv[1], encoding="utf-8"))
out = []
for svc in (500, 3000, 10000):
    for util, mkt in ((0, 0), (150, 50)):
        meta = max(0, svc - FREE) * SERVICE + util * UTILITY + mkt * MARKETING
        total_msgs = svc + util + mkt
        row = {"service_msgs": svc, "utility_templates": util, "marketing_templates": mkt, "meta_fees_usd": round(meta, 2), "by_provider": []}
        for p in providers:
            extra = meta * p.get("markup_pct", 0) / 100 + p.get("monthly_fee_usd", 0) + total_msgs * p.get("per_msg_fee_usd", 0)
            row["by_provider"].append({"name": p["name"], "total_usd": round(meta + extra, 2)})
        out.append(row)
print(json.dumps({"assumptions": {"service": SERVICE, "utility": UTILITY, "marketing": MARKETING, "free_service_per_number": FREE}, "scenarios": out}, ensure_ascii=False))
