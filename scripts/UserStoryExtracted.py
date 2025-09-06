# scripts/UserStoryExtracted.py
import argparse, csv, os, sys, re
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    pd = None

def parse_story(st: str) -> str:
    """
    从“作为一名X， 我想Y， 以便Z”中抽取 Y。
    更稳健：优先找 “，” 之后到 “以便/以” 之前的内容；都没有就回空。
    """
    if not st:
        return ""
    st = str(st).strip()
    # 统一中文逗号
    first_comma = st.find("，")
    if first_comma == -1:
        return ""
    # “以便”优先、再退化到“以”
    end = st.find("以便", first_comma + 1)
    if end == -1:
        end = st.find("以", first_comma + 1)
    if end == -1:
        return ""
    return st[first_comma + 1 : end].replace("我想", "").replace("希望", "").strip(" ，。;；")

def read_rows(in_path: Path):
    ext = in_path.suffix.lower()
    if ext in [".xls", ".xlsx"]:
        if pd is None:
            print("需要 pandas 才能读取 Excel。请先 pip install pandas openpyxl", file=sys.stderr)
            sys.exit(1)
        df = pd.read_excel(in_path)
        # 默认第一列为用户故事，如果有“用户故事”列名则优先
        col = "用户故事" if "用户故事" in df.columns else df.columns[0]
        for v in df[col].tolist():
            yield str(v)
    else:  # csv
        # 自动尝试 gbk/utf-8
        for enc in ("utf-8", "gbk"):
            try:
                with open(in_path, "r", encoding=enc, newline="") as f:
                    r = csv.reader(f)
                    header = next(r, None)
                    for row in r:
                        if not row:
                            continue
                        yield row[0]
                break
            except UnicodeDecodeError:
                continue

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="data/raw/02.用户故事及其类类别278条.xls",
                    help="输入文件（CSV/XLS/XLSX），默认按论文路径")
    ap.add_argument("--out", dest="outp", default="data/processed/User_story278.csv",
                    help="输出 CSV（解析后的用户故事内容）")
    args = ap.parse_args()

    in_path = Path(args.inp); out_path = Path(args.outp)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["用户故事原文", "提取的内容"])
        for s in read_rows(in_path):
            w.writerow([s, parse_story(s)])

    print(f"[OK] 写出：{out_path}")

if __name__ == "__main__":
    main()
