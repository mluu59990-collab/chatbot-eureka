from pathlib import Path
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from src.vector_db.search_chroma import search, build_context
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env",override = True)
chat_api_key = os.getenv("CHAT_API_KEY")
chat_model = os.getenv("CHAT_MODEL")
chat_base_url = os.getenv("CHAT_BASE_URL")
if not chat_api_key:
    raise RuntimeError("missing CHAT_API_KEY")
if not chat_model:
    raise RuntimeError("Missing Chat_model")
if not chat_base_url:
    raise RuntimeError("Missing Chat_Base")
chat_client = OpenAI(
    api_key=chat_api_key,
    base_url=chat_base_url
)
def strip_thinking(text:str) -> str:
    return re.sub(r"<think>.*?</think>","",text,flags=re.DOTALL).strip()
def answer_with_context(question:str,top_k: int = 3) -> str:
    result=search(question,top_k=top_k)
    context = build_context(result)
    system_prompt = """
Bạn là trợ lý hỏi đáp văn bản pháp luật Việt Nam.
Chỉ trả lời dựa trên ngữ cảnh được cung cấp.
Nếu ngữ cảnh không đủ căn cứ, hãy nói không tìm thấy thông tin trong tài liệu.
Khi trả lời, nêu rõ văn bản, điều, khoản nếu có.
Không trả lời kiểu "theo nguồn 1, 2, 3"; hãy nêu tên văn bản, điều, khoản cụ thể.
""".strip()
    user_prompt = f"""
Ngữ cảnh:{context}
Câu hỏi:{question}
/no_think
""".strip()
    response = chat_client.chat.completions.create(
        model = chat_model,
        messages = [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        temperature =  0.7,
        max_tokens = 1024
    )
    answer = response.choices[0].message.content
    return strip_thinking(answer)

