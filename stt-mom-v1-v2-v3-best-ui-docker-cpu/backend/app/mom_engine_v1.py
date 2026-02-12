import re

def generate_mom_v1(transcript: str, lang: str = "auto") -> dict:
    text = transcript.strip()
    action_patterns = [
        r"\bwe will\b", r"\bi will\b", r"\bplease\b", r"\bneed to\b", r"\bshall\b",
        r"చేయాలి", r"చేద్దాం", r"చెయ్యాలి", r"చేస్తాను",
        r"करेंगे", r"करना है", r"कर दूँगा",
        r"செய்ய", r"வேண்டும்",
        r"ಮಾಡಬೇಕು", r"ಮಾಡೋಣ"
    ]
    actions = []
    for sent in re.split(r"[.\n!?]+", text):
        s = sent.strip()
        if not s:
            continue
        if any(re.search(p, s.lower()) for p in action_patterns) and len(s) > 8:
            actions.append(s)

    decisions = []
    for sent in re.split(r"[.\n!?]+", text):
        s = sent.strip()
        if re.search(r"\b(decided|final|approved|confirmed)\b", s.lower()):
            decisions.append(s)

    return {
        "engine": "v1-rule-based",
        "language": lang,
        "summary": ["MoM generated with V1 (rule-based). Enable V2 (Ollama) for best quality."],
        "decisions": decisions[:12],
        "action_items": [{"task": a, "owner": "", "due_date": ""} for a in actions[:15]],
        "risks": [],
        "next_steps": [a for a in actions[:8]]
    }
