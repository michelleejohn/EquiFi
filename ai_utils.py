import re


RISK_KEYWORDS = {
    "variable apr": 3,
    "balloon payment": 4,
    "late fee": 2,
    "penalty": 2,
    "compounding daily": 3,
    "prepayment penalty": 3,
    "collection": 2,
    "default": 3
}


def calculate_risk(text: str):
    score = 0
    flags = []
    text_lower = text.lower()


    for keyword, weight in RISK_KEYWORDS.items():
        if keyword in text_lower:
            score += weight
            flags.append(keyword)


    apr_match = re.search(r"\b(\d{2,})%\b", text)
    if apr_match:
        apr = int(apr_match.group(1))
        if apr >= 20:
            score += 3
            flags.append(f"High APR detected: {apr}%")


    if score <= 3:
        level = "Low"
    elif score <= 6:
        level = "Medium"
    else:
        level = "High"


    return {
        "score": score,
        "level": level,
        "flags": flags
    }
