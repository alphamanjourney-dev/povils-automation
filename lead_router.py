#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class Decision:
    score: int
    tier: str
    route: str
    next_action: str
    reason: str

def normalize(lead: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": str(lead.get("name", "")).strip(),
        "email": str(lead.get("email", "")).strip().lower(),
        "budget": int(lead.get("budget", 0) or 0),
        "timeline_days": int(lead.get("timeline_days", 999) or 999),
        "service": str(lead.get("service", "")).strip().lower(),
        "message": str(lead.get("message", "")).strip(),
    }

def validate(lead: Dict[str, Any]) -> None:
    missing = [k for k in ("name", "email", "service") if not lead.get(k)]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    if "@" not in lead["email"]:
        raise ValueError("Invalid email address")

def score_lead(lead: Dict[str, Any]) -> Decision:
    l = normalize(lead)
    validate(l)
    score = 0
    reasons = []

    if l["budget"] >= 1000:
        score += 40
        reasons.append("budget >= 1000")
    elif l["budget"] >= 500:
        score += 25
        reasons.append("budget >= 500")
    elif l["budget"] >= 250:
        score += 10
        reasons.append("budget >= 250")

    if l["timeline_days"] <= 7:
        score += 30
        reasons.append("timeline <= 7 days")
    elif l["timeline_days"] <= 30:
        score += 15
        reasons.append("timeline <= 30 days")

    high_fit_terms = ("automation", "crm", "api", "integration", "follow-up", "workflow")
    if any(term in (l["service"] + " " + l["message"]).lower() for term in high_fit_terms):
        score += 30
        reasons.append("high-fit automation need")

    if score >= 70:
        return Decision(score, "HOT", "priority-sales", "reply within 15 minutes and propose a diagnostic", "; ".join(reasons))
    if score >= 40:
        return Decision(score, "WARM", "standard-sales", "reply same business day with scoped questions", "; ".join(reasons))
    return Decision(score, "COLD", "nurture", "send concise fit-check and avoid high-touch effort", "; ".join(reasons) or "limited fit signals")

def run_sample() -> Dict[str, Any]:
    sample = {
        "name": "Jordan Example",
        "email": "jordan@example.com",
        "budget": 750,
        "timeline_days": 7,
        "service": "CRM automation",
        "message": "We need lead forms routed into our CRM with automated follow-up."
    }
    decision = score_lead(sample)
    return {"lead": normalize(sample), "decision": asdict(decision)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()
    if args.sample:
        print(json.dumps(run_sample(), indent=2))
