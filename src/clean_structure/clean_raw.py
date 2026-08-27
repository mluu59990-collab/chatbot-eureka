import re
import unicodedata
from pathlib import Path
structure_line_re = re.compile(
    r"^(CHƯƠNG|Chương|MỤC|Mục|Điều\s+\d+[a-zA-Z]?\b|\d+\.\s|[a-zđ]\)\s)"
)

def normalize_unicode(text:str) -> str:
    #Thay kys tu dau la "BOM" cho doan van sau khi model OCR lay van ban ra
    text = text.replace("\ufeff","")
    #Chuan hoa van ban theo tieng viet
    return unicodedata.normalize("NFC",text)
def normalize_whitespace(text:str) -> str:
    # thay the doan xuong dong thanh \n win:\r\n mac:\r
    text = text.replace("\r\n","\n").replace("\r","\n")
    text = re.sub(r"[ \t\u00a0]+"," ",text)
    text = re.sub(r"\n[ \t]+","\n",text)
    text = re.sub(r"\n{3,}","\n\n",text)
    return text.strip()
def remove_page_markers(text:str) -> str:
    text = re.sub(r"(?im)^---\s*Page\s+\d+.*?---\s*$","",text)
    text = re.sub(r"(?m)^_{3,}$","",text)
    text = re.sub(r"(?m)^-{3,}$","",text)
    return text
def should_join_lines(prev_line:str,next_line:str) -> bool:
    if not prev_line or not next_line:
        return False
    if structure_line_re.match(next_line):
        return False
    if prev_line.endswith((".",":",";","!","'",'"')):
        return False
    return True
def join_broken_lines(text:str) -> str:
    result = []
    lines = [line.strip() for line in text.split("\n")]
    for line in lines:
        if not line:
            result.append("")
            continue
        if result and should_join_lines(result[-1],line):
            result[-1] = result[-1] + " " +line
        else:
            result.append(line)
    return "\n".join(result)
def remove_tail(text:str) -> str:
    parts = re.split(r"(?im)^\s*Nơi nhận:\s*$",text)
    return parts[0].strip()
def normalize_legal_text(raw_text:str) -> str:
    text = normalize_unicode(raw_text)
    text = remove_page_markers(text)
    text = normalize_whitespace(text)
    text = join_broken_lines(text)
    text = remove_tail(text)
    text = normalize_whitespace(text)
    return text
#Unicode -> page marker -> whitespace -> nối dòng gãy -> bỏ đuôi -> whitespace lần cuối
def normalize_folder(input: str, output:str):
    input_dir = Path(input)
    output_dir = Path(output)
    output_dir.mkdir(parents=True,exist_ok=True)
    for input_path in input_dir.glob("*.txt"):
        raw = input_path.read_text(encoding = "utf-8",errors = "ignore")
        clean = normalize_legal_text(raw)
        output_path= output_dir/input_path.name
        output_path.write_text(clean,encoding = "utf-8")
        print(f"Done:{input_path.name}")
if __name__ == "__main__":
    normalize_folder("/Users/apple/Downloads/App_chatbot/hybrid_output/texts","/Users/apple/Downloads/App_chatbot/clean_text/normalize_texts")

