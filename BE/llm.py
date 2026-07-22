import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
from datetime import datetime 
load_dotenv(Path(__file__).resolve().parent / ".env")
client = OpenAI(
    api_key = os.getenv("LLM_API_KEY"),
    base_url = os.getenv("LLM_BASE_URL")
)
MODEL_NAME = os.getenv("LLM_MODEL")
def get_ai_response(chat_history: list[dict]) -> str:
    system_message ={
        "role":"system",
        "content": f"Hôm nay là ngày {datetime.now().strftime('%d/%m/%Y')}. Bạn là trợ lý AI hữu ích."
    }
    full_message = [system_message]+chat_history
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=full_message,
    )
    return response.choices[0].message.content
