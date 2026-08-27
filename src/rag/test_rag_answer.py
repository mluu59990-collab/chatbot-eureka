from pathlib import Path
import sys
import os
import re

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from dotenv import load_dotenv
from openai import OpenAI

from src.vector_db.search_chroma import search, build_context

load_dotenv(BASE_DIR / ".env", override=True)
chat_api_key = os.getenv("CHAT_API_KEY")
chat_base_url = os.getenv("CHAT_BASE_URL")
chat_model = os.getenv("CHAT_MODEL")
if not chat_api_key:
    raise RuntimeError("Missing CHAT_API_KEY")

if not chat_base_url:
    raise RuntimeError("Missing CHAT_BASE_URL")

if not chat_model:
    raise RuntimeError("Missing CHAT_MODEL")
chat_client = OpenAI(
    api_key=chat_api_key,
    base_url=chat_base_url,
)
def strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
def answer_with_context(question: str) -> str:
    results = search(question, top_k=5)

    context = build_context(results)

    system_prompt = """
Bạn là trợ lý hỏi đáp văn bản pháp luật Việt Nam.
Chỉ trả lời dựa trên ngữ cảnh được cung cấp.
Nếu ngữ cảnh không đủ căn cứ, hãy nói không tìm thấy thông tin trong tài liệu.
Khi trả lời, nêu rõ văn bản, điều, khoản nếu có.
""".strip()

    user_prompt = f"""
Ngữ cảnh:
{context}

Câu hỏi:
{question}

/no_think
""".strip()

    response = chat_client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    answer = response.choices[0].message.content

    return strip_thinking(answer)
if __name__ == "__main__":
    question = "Bếp từ phải dán nhãn năng lượng bắt buộc từ ngày nào?"

    answer = answer_with_context(question)

    print(answer)