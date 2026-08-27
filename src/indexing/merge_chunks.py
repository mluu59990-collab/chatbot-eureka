import json
from pathlib import Path
def merge_jsonl(input_dir: str, output_path: str):
    input_dir = Path(input_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents = True, exist_ok = True)
    total =0
    with output_path.open("w", encoding = "utf-8") as out_file:
        for json_path in sorted(input_dir.glob("*.jsonl")):
            with json_path.open("r",encoding="utf-8") as in_file:
                for line in in_file:
                    chunk = json.loads(line)
                    out_file.write(json.dumps(chunk,ensure_ascii=False)+"\n")
                    total+=1
            print(f"Merge {total} chunk into{output_path}")
if __name__ =="__main__":
    merge_jsonl(
        input_dir="clean_text/chunking",
        output_path="clean_text/all_chunks.jsonl"
    )