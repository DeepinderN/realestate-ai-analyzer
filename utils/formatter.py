import csv
import os
from datetime import datetime


GRADE_COLORS = {
    "A": "\033[92m",   # green
    "B": "\033[94m",   # blue
    "C": "\033[93m",   # yellow
    "D": "\033[91m",   # red
}
RESET = "\033[0m"
BOLD = "\033[1m"


def print_lead_result(lead: dict, analysis: dict, index: int, total: int):
    grade = analysis.get("lead_grade", "?")
    color = GRADE_COLORS.get(grade, "")
    score = analysis.get("priority_score", "?")

    print(f"\n{'─' * 60}")
    print(f"{BOLD}Lead {index}/{total}: {lead['name']}{RESET}  |  "
          f"Budget: ${int(lead['budget']):,}  |  Source: {lead['source']}")
    print(f"  Grade:   {color}{BOLD}{grade}{RESET}   Score: {score}/10")
    print(f"  Intent:  {analysis.get('intent', '?').capitalize()}")
    print(f"  Urgency: {analysis.get('urgency', '?').replace('-', ' ').capitalize()}")
    print(f"  Action:  {analysis.get('recommended_action', '?')}")

    flags = analysis.get("risk_flags", [])
    if flags:
        print(f"  ⚠ Flags:  {', '.join(flags)}")

    print(f"  {analysis.get('summary', '')}")


def save_report(leads: list, analyses: list, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"lead_report_{timestamp}.csv")

    fieldnames = [
        "lead_id", "name", "budget", "source", "property_type", "location",
        "priority_score", "lead_grade", "intent", "urgency",
        "recommended_action", "risk_flags", "summary"
    ]

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for lead, analysis in zip(leads, analyses):
            writer.writerow({
                "lead_id": lead.get("lead_id"),
                "name": lead.get("name"),
                "budget": lead.get("budget"),
                "source": lead.get("source"),
                "property_type": lead.get("property_type"),
                "location": lead.get("location"),
                "priority_score": analysis.get("priority_score"),
                "lead_grade": analysis.get("lead_grade"),
                "intent": analysis.get("intent"),
                "urgency": analysis.get("urgency"),
                "recommended_action": analysis.get("recommended_action"),
                "risk_flags": "; ".join(analysis.get("risk_flags", [])),
                "summary": analysis.get("summary"),
            })

    return path


def print_summary(leads: list, analyses: list):
    print(f"\n{'═' * 60}")
    print(f"{BOLD}PIPELINE SUMMARY{RESET}")
    print(f"{'═' * 60}")

    graded = sorted(
        zip(leads, analyses),
        key=lambda x: x[1].get("priority_score", 0),
        reverse=True
    )

    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for _, a in analyses if isinstance(analyses, list) else []:
        g = a.get("lead_grade")
        if g in grade_counts:
            grade_counts[g] += 1

    # Recount properly
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for _, a in graded:
        g = a.get("lead_grade")
        if g in grade_counts:
            grade_counts[g] += 1

    total_budget = sum(int(l.get("budget", 0)) for l, _ in graded
                       if l.get("budget", "").isdigit() or str(l.get("budget", "")).isdigit())

    print(f"  Total leads analyzed: {len(graded)}")
    for grade, count in grade_counts.items():
        bar = "█" * count
        color = GRADE_COLORS.get(grade, "")
        print(f"  Grade {color}{grade}{RESET}: {bar} ({count})")

    print(f"\n{BOLD}Top 3 Priority Leads:{RESET}")
    for i, (lead, analysis) in enumerate(graded[:3], 1):
        grade = analysis.get("lead_grade")
        color = GRADE_COLORS.get(grade, "")
        print(f"  {i}. {lead['name']} — "
              f"{color}Grade {grade}{RESET} — "
              f"Score {analysis.get('priority_score')}/10 — "
              f"{analysis.get('recommended_action')}")
