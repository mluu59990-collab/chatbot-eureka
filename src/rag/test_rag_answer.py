from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))


from src.rag.rag_service import answer_with_context


if __name__ == "__main__":
    question = "Bếp từ phải dán nhãn năng lượng bắt buộc từ ngày nào?"

    answer = answer_with_context(question)

    print(answer)