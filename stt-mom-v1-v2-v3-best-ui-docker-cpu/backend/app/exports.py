def to_txt(meeting: dict) -> str:
    t = meeting.get("transcript", "")
    mom = meeting.get("mom") or {}
    lines = ["TRANSCRIPT", t, "", "MoM"]
    for k in ["summary","decisions","action_items","risks","next_steps"]:
        if k in mom:
            lines.append(f"{k.upper()}:")
            v = mom.get(k)
            if isinstance(v, list):
                for i, it in enumerate(v, 1):
                    if isinstance(it, dict):
                        s = it.get("task","")
                        if it.get("owner"): s += f" (Owner: {it.get('owner')})"
                        if it.get("due_date"): s += f" (Due: {it.get('due_date')})"
                        lines.append(f"  {i}. {s}".strip())
                    else:
                        lines.append(f"  {i}. {it}")
            else:
                lines.append(f"  {v}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"

def to_md(meeting: dict) -> str:
    t = meeting.get("transcript","")
    mom = meeting.get("mom") or {}
    md = ["# Meeting Notes", "", "## Transcript", "", t or "", "", "## MoM", ""]
    for k in ["summary","decisions","action_items","risks","next_steps"]:
        if k in mom:
            md.append(f"### {k.replace('_',' ').title()}")
            v = mom.get(k)
            if isinstance(v, list):
                for it in v:
                    if isinstance(it, dict):
                        s = it.get("task","")
                        if it.get("owner"): s += f" (Owner: {it.get('owner')})"
                        if it.get("due_date"): s += f" (Due: {it.get('due_date')})"
                        md.append(f"- {s}".strip())
                    else:
                        md.append(f"- {it}")
            else:
                md.append(str(v))
            md.append("")
    return "\n".join(md).strip() + "\n"
