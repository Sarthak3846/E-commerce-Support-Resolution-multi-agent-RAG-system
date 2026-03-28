from typing import Dict, List

class TriageAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, ticket_text: str, order_context: Dict) -> Dict:
        prompt = f"""
You are a support triage agent.

Classify the issue and detect missing fields.

Ticket:
{ticket_text}

Order Context:
{order_context}

Return JSON:
{{
  "issue_type": "...",
  "confidence": "...",
  "missing_fields": [],
  "clarifying_questions": []
}}

Rules:
- Issue types: refund, shipping, payment, promo, fraud, other
- Ask max 3 clarifying questions if needed
- Be precise
"""

        response = self.llm(prompt)

        return response