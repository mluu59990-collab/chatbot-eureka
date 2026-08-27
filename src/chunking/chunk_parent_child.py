import re
import json
from pathlib import Path
ARTICLE_RE = re.compile(r"(?m)^Điều\s+(\d+[a-zA-Z]?)\.\s*(.*)$")
CLAUSE_RE = re.compile(r"(?m)^(\d+)\.\s+")
def split_articles(text:str) -> list[dict]:
    article_matches = list(ARTICLE_RE.finditer(text))
    articles = []
    for i, match in enumerate(article_matches):
        start = match.start()
        end = article_matches[i+1].start() if i+1<len(article_matches) else len(text)
        articles_no = match.group(1)
        heading = match.group(2).strip()
        articles_text = text[start:end].strip()
        articles.append({
            "article_no": articles_no,
            "heading": heading,
            "text": articles_text,
        })
    return articles
def split_clauses(article:dict) -> list[dict]:
    parent_text = article["text"]
    clause_matches = list(CLAUSE_RE.finditer(parent_text))
    clauses = []
    if not clause_matches:
        clauses.append({
            "clause_no":None,
            "text":parent_text,
        })
        return clauses
    for i, match in enumerate(clause_matches):
        start = match.start()
        end = clause_matches[i+1].start() if i+1<len(clause_matches) else len(parent_text)
        clause_no = match.group(1)
        clause_text = parent_text[start:end].strip()
        clauses.append({
            "clause_no":clause_no,
            "text":clause_text
        })
    return clauses
def sliding_window_chunks(
    source_file: str,
    text: str,
    chunk_size: int = 250,
    overlap: int = 50,
) -> list[dict]:
    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for index, start in enumerate(range(0, len(words), step), start=1):
        end = start + chunk_size
        chunk_words = words[start:end]

        if not chunk_words:
            break

        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunk_id": f"{source_file}__window_{index}",
            "parent_id": None,
            "source_file": source_file,
            "article": None,
            "heading": None,
            "child_label": f"Window {index}",
            "child_text": chunk_text,
            "parent_text": chunk_text,
            "chunk_strategy": "sliding_window",
            "start_word": start,
            "end_word": min(end, len(words)),
        })

        if end >= len(words):
            break

    return chunks
def build_parent_child_chunks(source_file: str, text: str) -> list[dict]:
    chunks = []

    articles = split_articles(text)
    if not articles:
        return sliding_window_chunks(source_file,text)
    for article in articles:
        parent_id = f"{source_file}__dieu_{article['article_no']}"
        parent_text = article["text"]

        clauses = split_clauses(article)

        for index, clause in enumerate(clauses, start=1):
            chunk_id = f"{parent_id}__child_{index}"

            if clause["clause_no"]:
                child_label = f"Khoản {clause['clause_no']}"
            else:
                child_label = f"Điều {article['article_no']}"

            chunk = {
                "chunk_id": chunk_id,
                "parent_id": parent_id,
                "source_file": source_file,
                "article": f"Điều {article['article_no']}",
                "heading": article["heading"],
                "child_label": child_label,
                "child_text": clause["text"],
                "parent_text": parent_text,
                "chunk_strategy": "parent_child",
            }

            chunks.append(chunk)

    return chunks
def chunking_data(input:str, output: str):
    input_dir = Path(input)
    output_dir = Path(output)
    output_dir.mkdir(parents=True,exist_ok=True)
    for input_path in input_dir.glob("*.txt"):
        raw = input_path.read_text(encoding="utf-8",errors="ignore")
        chunks = build_parent_child_chunks(input_path.name,raw)
        output_path = output_dir / f"{input_path.stem}.jsonl"
        with output_path.open("w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

        print(f"Done: {input_path.name} -> {len(chunks)} chunks")
if __name__ == "__main__":
    chunking_data("/Users/apple/Downloads/App_chatbot/clean_text/normalize_texts","/Users/apple/Downloads/App_chatbot/clean_text/chunking")
