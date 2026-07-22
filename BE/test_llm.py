import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

print("API_KEY:", "<set>" if os.getenv("LLM_API_KEY") else "<missing>")
print("BASE_URL:", os.getenv("LLM_BASE_URL") or "<missing>")
print("MODEL:", os.getenv("LLM_MODEL") or "<missing>")

from llm import get_ai_response

print("Đang gọi API...")
try:
    result = get_ai_response([{"role": "user", "content": "Hôm nay là ngày bao nhiêu?"}])
    print("Kết quả:", result)
except Exception as exc:
    print("LLM test failed:", exc)
