from utils.llm import gemini_llm

print(gemini_llm("""
Return ONLY JSON:
{"status": "ok"}
"""))