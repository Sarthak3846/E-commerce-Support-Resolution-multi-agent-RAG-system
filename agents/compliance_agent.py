from typing import Dict

class ComplianceAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, resolution_output: Dict) -> Dict:
        prompt = f"""
You are a compliance and safety agent.

Check:
- Are all claims backed by citations?
- Any hallucinations?
- Any unsafe or unsupported decisions?

Input:
{resolution_output}

Return JSON:
{{
  "is_valid": true/false,
  "issues": [],
  "final_decision": "...",
  "corrected_output": {{}}
}}

Rules:
- If citations missing → INVALID
- If unsupported claims → INVALID
- If invalid → fix output
"""

        response = self.llm(prompt)
        return response