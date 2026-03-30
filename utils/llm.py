import os
import time
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.0-flash"   


import time

def gemini_llm(prompt: str):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            text = response.text.strip()
            start = text.find("{")
            end = text.rfind("}") + 1

            return json.loads(text[start:end])

        except Exception as e:
            if "429" in str(e):
                time.sleep(5)
            else:
                return {"error": str(e)}

    return {"error": "Max retries exceeded"}