#!/usr/bin/env python3
"""
RealEstate AI Lead Analyzer
----------------------------
Reads a CSV of real estate leads, sends each one to Claude for AI-powered
qualification, scores them A-D, and outputs a ranked report + saved CSV.

Usage:
    python main.py                        # uses data/sample_leads.csv
    python main.py --file your_leads.csv  # custom file
    python main.py --top 5               # analyze top N leads only
"""

import csv
import sys
import time
import argparse
import os

from analyzer import analyze_lead
from utils.formatter import print_lead_result, print_summary, save_report

BOLD = "\033[1m"
RESET = "\033[0m"
CYAN = "\033[96m"


def load_leads(filepath: str) -> list:
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def run(filepath: str, top_n: int = None):
    print(f"\n{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  🏠  RealEstate AI Lead Analyzer  |  Powered by Claude")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    leads = load_leads(filepath)

    if top_n:
        leads = leads[:top_n]

    print(f"  Loaded {len(leads)} leads from {filepath}")
    print(f"  Sending to Claude for analysis...\n")

    analyses = []
    failed = []

    for i, lead in enumerate(leads, 1):
        name = lead.get("name", f"Lead {i}")
        print(f"  [{i}/{len(leads)}] Analyzing {name}...", end=" ", flush=True)

        try:
            result = analyze_lead(lead)
            analyses.append(result)
            grade = result.get("lead_grade", "?")
            score = result.get("priority_score", "?")
            print(f"Grade {grade}  Score {score}/10 ✓")
        except Exception as e:
            print(f"FAILED ✗ ({e})")
            failed.append((i, name, str(e)))
            analyses.append({})

        time.sleep(0.3)  # rate limit buffer

    # Print detailed results
    valid_pairs = [(l, a) for l, a in zip(leads, analyses) if a]
    for i, (lead, analysis) in enumerate(valid_pairs, 1):
        print_lead_result(lead, analysis, i, len(valid_pairs))

    # Summary table
    print_summary(leads, list(zip(leads, analyses)))

    # Save report
    report_path = save_report(leads, analyses)
    print(f"\n  ✅ Report saved → {report_path}")

    if failed:
        print(f"\n  ⚠ {len(failed)} lead(s) failed to analyze:")
        for idx, name, err in failed:
            print(f"     Lead {idx} ({name}): {err}")

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-powered real estate lead qualifier")
    parser.add_argument("--file", default="data/sample_leads.csv", help="Path to leads CSV")
    parser.add_argument("--top", type=int, default=None, help="Analyze only top N leads")
    args = parser.parse_args()

    run(filepath=args.file, top_n=args.top)
