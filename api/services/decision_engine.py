# api/services/decision_engine.py
import json
from pathlib import Path

# Always resolves path relative to this file
THRESHOLD_PATH = Path(__file__).parent.parent / "models/thresholds_v1.json"

def load_thresholds():
    if THRESHOLD_PATH.exists():
        with open(THRESHOLD_PATH) as f:
            return json.load(f)
    # fallback default thresholds
    return {"T_review": 0.5, "T_block": 0.8}

def apply_rules(features):
    rules = []
    if features.get('amount_z', 0) > 3:
        rules.append("high_amount")
    if features.get('velocity', 0) > 5:
        rules.append("high_velocity")
    return rules

def make_decision(score, rules):
    thresholds = load_thresholds()
    if "critical_rule" in rules:
        return "REJECT"
    elif score >= thresholds["T_block"]:
        return "REJECT"
    elif score >= thresholds["T_review"]:
        return "REVIEW"
    else:
        return "APPROVE"
