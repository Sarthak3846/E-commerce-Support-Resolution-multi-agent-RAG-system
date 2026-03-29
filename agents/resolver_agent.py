from typing import Dict, List


class ResolverAgent:
    def __init__(self, llm):
        self.llm = llm

    def safe_llm_call(self, prompt):
        response = self.llm(prompt)
        if not isinstance(response, dict):
            return {"error": "Invalid LLM response"}
        return response

    def run(self, ticket_text: str, order_context: Dict, retrieved_docs: List[Dict]) -> Dict:
        context = "\n\n".join([
            f"{d['content']} (Source: {d['source']}, ID: {d['id']})"
            for d in retrieved_docs
        ])

        prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

You are a support resolution agent.

STRICT RULES:
- ONLY use the provided policy context
- If insufficient evidence → say "NOT_ENOUGH_INFO"
- Citations must be EXACTLY in this format:
  [source_file - chunk_id]
  Example: [amazon_returns.txt - amazon_returns.txt_chunk_0]

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
  "citations": ["source_file - chunk_id"],
  "customer_response_draft": "...",
  "next_steps": "..."
}}
"""

        return self.safe_llm_call(prompt)