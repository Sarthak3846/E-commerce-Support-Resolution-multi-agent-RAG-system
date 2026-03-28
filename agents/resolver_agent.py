from typing import Dict, List

class ResolverAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, ticket_text: str, order_context: Dict, retrieved_docs: List[Dict]) -> Dict:
        context = "\n\n".join([
            f"{d['content']} (Source: {d['source']}, Section: {d['section']})"
            for d in retrieved_docs
        ])

        prompt = f"""
You are a support resolution agent.

STRICT RULE:
- ONLY use the provided policy context
- If insufficient evidence → say "NOT_ENOUGH_INFO"

Ticket:
{ticket_text}

Order Context:
{order_context}

Policy Context:
{context}

Return JSON:
{{
  "decision": "approve/deny/partial/needs escalation",
  "rationale": "...",
  "citations": ["source - section"],
  "customer_response_draft": "...",
  "next_steps": "..."
}}
"""

        response = self.llm(prompt)
        return response