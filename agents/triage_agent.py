from typing import Dict


class TriageAgent:
    def __init__(self, llm):
        self.llm = llm

    def safe_llm_call(self, prompt):
        response = self.llm(prompt)
        if not isinstance(response, dict):
            return {"error": "Invalid LLM response"}
        return response

    def run(self, ticket_text: str, order_context: Dict) -> Dict:
        prompt = f"""
Return ONLY valid JSON. No explanation.

You are a triage agent.

Classify the issue.

IMPORTANT:
- If the issue is clear (refund, return, cancellation, damaged item, wrong item)
  → DO NOT ask clarifying questions
- Only ask questions if decision CANNOT be made without missing data

Examples:
- "wrong size" → NO questions
- "damaged item" → NO questions
- "refund request" → NO questions

Return:
{{
  "issue_type": "...",
  "confidence": "low/medium/high",
  "clarifying_questions": []
}}

Rules:
- Issue types: refund, shipping, payment, promo, fraud, other
- Ask max 3 clarifying questions if needed
- Be precise

Ticket:
{ticket_text}

Order Context:
{order_context}
"""

        return self.safe_llm_call(prompt)