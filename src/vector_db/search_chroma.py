from pathlib import Path
import chromadb
from dotenv import load_dotenv
import os
from openai import OpenAI
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
CHROMA_DIR = BASE_DIR / "vector_db" / "chroma"
load_dotenv(BASE_DIR / ".env",override=True)

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_collection("legal_chunks")

api_key = os.getenv("EMBEDDING_API_KEY")
base_url = os.getenv("EMBEDDING_BASE_URL")
model = os.getenv("EMBEDDING_MODEL")
if not api_key:
    raise RuntimeError("Missing EMBEDDING_API_KEY")

if not base_url:
    raise RuntimeError("Missing EMBEDDING_BASE_URL")

if not model:
    raise RuntimeError("Missing EMBEDDING_MODEL")
client_embed = OpenAI(
    api_key=api_key,
    base_url=base_url,
)
def embed_query(query:str) -> list[float]:
    response = client_embed.embeddings.create(
        model=model,
        input=query,
    )
    return response.data[0].embedding
def search(query: str, top_k: int=5):
    query_embedding = embed_query(query)
    result = collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k,
    include=["documents", "metadatas", "distances"],
)
    return result
def build_context(results) ->str:
    context_parts = []
    total_results = len(results["ids"][0])
    for i in range(total_results):
        metadata=results["metadatas"][0][i]
        document=metadata.get("parent_text") or results["documents"][0][i]
        source_file=metadata.get("source_file") or ""
        article = metadata.get("article") or ""
        heading = metadata.get("heading") or ""
        child_label = metadata.get("child_label") or ""
        context = f"""
        [Nguồn {i + 1}]
Văn bản: {source_file}
Điều: {article}
Tiêu đề: {heading}
Mục: {child_label}
Nội dung:
{document}
""".strip()
        context_parts.append(context)
    return "\n\n".join(context_parts)
def answer_with_context(question: str) -> str:
    results = search(question, top_k=5)

    context = build_context(results)

    system_prompt = """
Bạn là trợ lý pháp lý cho văn bản Việt Nam.
Chỉ trả lời dựa trên phần ngữ cảnh được cung cấp.
Nếu ngữ cảnh không đủ thông tin, hãy nói không tìm thấy căn cứ trong tài liệu.
Khi trả lời, nêu rõ văn bản, điều, khoản nếu có.
""".strip()

    user_prompt = f"""
Ngữ cảnh:
{context}

Câu hỏi:
{question}

Hãy trả lời ngắn gọn, chính xác, có căn cứ.
""".strip()

    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content
if __name__ == "__main__":
    print("Total records:", collection.count())

    query = "bếp từ phải dán nhãn năng lượng từ ngày nào?"
    results = search(query, top_k=5)

    context = build_context(results)

    print(context)