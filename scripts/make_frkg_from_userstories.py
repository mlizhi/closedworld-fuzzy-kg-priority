# scripts/make_frkg_from_userstories.py
import csv, argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp",  default="data/processed/User_story278.csv", help="输入：用户故事解析CSV")
    ap.add_argument("--outp", default="data/processed/FRKG_label.csv",   help="输出：FRKG 带模糊度")
    args = ap.parse_args()

    inp  = Path(args.inp)
    outp = Path(args.outp)
    outp.parent.mkdir(parents=True, exist_ok=True)

    triples = []
    with open(inp, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for i, row in enumerate(r, start=1):
            us = row.get("用户故事原文", f"用户故事#{i}")
            goal = f"目标#{i}"
            req  = f"需求#{i}"
            user = f"用户#{i}"

            triples += [
                (us, "Defines", goal, "User_Story", "Goal", 1.0),
                (user, "Proposes", req, "User", "Requirement", 1.0),
                (goal, "Specifies", req, "Goal", "Requirement", 1.0),
            ]

    with open(outp, "w", encoding="utf-8", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["Subject","Predicate","Object","SubjectLabels","ObjectLabels","Fuzzy"])
        for s,p,o,sl,ol,fz in triples:
            w.writerow([s,p,o,sl,ol,fz])

    print(f"[OK] 生成 FRKG：{outp}  共 {len(triples)} 条")

if __name__ == "__main__":
    main()
