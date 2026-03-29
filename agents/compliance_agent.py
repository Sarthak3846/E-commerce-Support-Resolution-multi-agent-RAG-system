from typing import Dict


class ComplianceAgent:
    def __init__(self, llm):
        self.llm = llm

    def safe_llm_call(self, prompt):
        response = self.llm(prompt)
        if not isinstance(response, dict):
            return {"is_valid": False, "issues": ["Invalid LLM response"], "corrected_output": {}}
        return response

    def run(self, resolution_output: Dict) -> Dict:
        prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

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
  "corrected_output": {{}}
}}

Rules:
- If citations missing → INVALID
- If unsupported claims → INVALID
- If invalid → fix output strictly using provided data
"""

        return self.safe_llm_call(prompt)