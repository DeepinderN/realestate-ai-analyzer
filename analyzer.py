import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a real estate lead qualification expert for a residential and industrial investment firm.
Given a lead's details, you analyze their quality and return a structured JSON response.

You must return ONLY valid JSON with exactly these fields:
{
  "priority_score": <integer 1-10, 10 = hottest lead>,
  "lead_grade": <"A" | "B" | "C" | "D">,
  "intent": <"buyer" | "investor" | "seller" | "unknown">,
  "urgency": <"immediate" | "short-term" | "long-term" | "cold">,
  "recommended_action": <string, one clear next step under 20 words>,
  "risk_flags": <list of strings, potential issues — empty list if none>,
  "summary": <string, 2-sentence max assessment of this lead>
}

Be direct. Do not include any explanation outside the JSON."""


def analyze_lead(lead: dict) -> dict:
    """Send a single lead to Claude for AI analysis. Returns parsed JSON result."""

    prompt = f"""Analyze this real estate lead and return your JSON assessment:

Name: {lead.get('name')}
Source: {lead.get('source')}
Property Type: {lead.get('property_type')}
Budget: ${lead.get('budget')}
Timeline: {lead.get('timeline')}
Location: {lead.get('location')}
Notes: {lead.get('notes')}
Days Since First Contact: {lead.get('days_since_contact')}
Follow-Up Attempts: {lead.get('follow_up_attempts')}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return json.loads(raw)
