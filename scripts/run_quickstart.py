# scripts/run_quickstart.py
import argparse, json, csv, math
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]

def ensure_dirs():
    for d in ["docs","docs/figures","data/raw","data/processed","outputs"]:
        (ROOT/d).mkdir(parents=True, exist_ok=True)

def write_tiny_demo():
    frkg = ROOT/"data/processed/FRKG_label.csv"
    if frkg.exists():
        return
    rows = [
        # S, P, O, SL, OL, Fuzzy
        ["US#1","Defines","G#1","User_Story","Goal",1.0],
        ["U#1","Proposes","R#1","User","Requirement",1.0],
        ["G#1","Specifies","R#1","Goal","Requirement",1.0],
        ["R#1","RelatesTo","R#2","Requirement","Requirement",0.8],
        ["U#2","Proposes","R#2","User","Requirement",1.0],
        ["US#2","Defines","G#2","User_Story","Goal",1.0],
        ["G#2","Specifies","R#2","Goal","Requirement",1.0],
    ]
    with open(frkg,"w",encoding="utf-8",newline="") as f:
        w = csv.writer(f);
        w.writerow(["Subject","Predicate","Object","SubjectLabels","ObjectLabels","Fuzzy"])
        w.writerows(rows)
    print(f"[OK] 写出 demo FRKG：{frkg}")

def load_frkg(path: Path):
    E = []
    with open(path,"r",encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            E.append(row)
    return E

def simple_closure(edges):
    # 只做一次 Specifies 传递： (G->R) & (R->R)  => (G->R) 新增
    specifies = [(e["Subject"], e["Object"], float(e.get("Fuzzy") or 1.0))
                 for e in edges if e["Predicate"]=="Specifies"]
    relates   = [(e["Subject"], e["Object"], float(e.get("Fuzzy") or 1.0))
                 for e in edges if e["Predicate"]=="RelatesTo"]

    inferred = []
    for g,r1,f1 in specifies:
        for r2,r3,f2 in [(a,b,c) for (a,b,c) in relates if a==r1]:
            inferred.append({
                "Subject": g, "Predicate":"Specifies", "Object": r3,
                "SubjectLabels":"Goal","ObjectLabels":"Requirement",
                "Fuzzy": f1*f2, "Rule":"FSTO_siso"
            })
    # 合并：原 + 新
    key = lambda e: (e["Subject"], e["Predicate"], e["Object"])
    seen = set()
    all_edges = []
    for e in edges + inferred:
        k = key(e)
        if k in seen:
            continue
        seen.add(k); all_edges.append(e)
    stats = {
        "original_edge": len(edges),
        "overall_edge": len(all_edges),
        "added": len(inferred),
        "Novelty": round(len(inferred)/max(1,len(all_edges)),4),
    }
    return all_edges, stats

def build_scores(edges):
    # 用三元组计数构造 5 个准则（非常小而足够验证的 demo 逻辑）：
    # 商业价值: Goal->Requirement 的数量
    # 用户优先级: User->Requirement
    # 可行性: Technology->Function or Function->Requirement（若无，置 0）
    # 依赖性: Requirement->Requirement
    # 成本: Structure->Function（若无，置 0）
    req_scores = defaultdict(lambda: dict(biz=0.0, userp=0.0, feas=0.0, dep=0.0, cost=0.0))

    for e in edges:
        s,p,o = e["Subject"], e["Predicate"], e["Object"]
        sl, ol = e.get("SubjectLabels",""), e.get("ObjectLabels","")
        fz = float(e.get("Fuzzy") or 1.0)
        if p=="Specifies" and "Goal" in sl and "Requirement" in ol:
            req_scores[o]["biz"] += fz
        if p=="Proposes" and "User" in sl and "Requirement" in ol:
            req_scores[o]["userp"] += fz
        if p in ("Achieves","Supports") or ("Function" in sl and "Requirement" in ol):
            req_scores[o]["feas"] += fz
        if p=="RelatesTo" and "Requirement" in sl and "Requirement" in ol:
            req_scores[s]["dep"] += fz
        if p=="Composes" and "Structure" in sl and "Function" in ol:
            # 这里没真实数据；保留接口，遇到就累计
            req_scores[o]["cost"] += fz

    # 归一化到 [0,1]
    keys = ["biz","userp","feas","dep","cost"]
    maxv = {k:max([v[k] for v in req_scores.values()] or [1.0]) for k in keys}
    for r,v in req_scores.items():
        for k in keys:
            v[k] = v[k] / max(1e-9, maxv[k])
    return req_scores

def gra_rank(score_map):
    # 参考序列取全 1；rho=0.5
    rho = 0.5
    ranks = []
    for req,sc in score_map.items():
        arr = [sc["biz"], sc["userp"], sc["feas"], sc["dep"], sc["cost"]]
        # 灰色关联系数（简化版）
        # distance = |1 - x_i|；系数 = (min+rho*max)/(d+rho*max)
        distances = [abs(1.0 - x) for x in arr]
        dmin, dmax = (min(distances), max(distances)) if distances else (0.0, 1.0)
        gra = [(dmin+rho*dmax)/(d+rho*dmax) for d in distances]
        score = sum(gra)/len(gra) if gra else 0.0
        ranks.append((req, score))
    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks

def write_outputs(ranks, stats):
    out_csv = ROOT/"outputs/ranking_top10.csv"
    out_json = ROOT/"outputs/expansion_stats.json"
    with open(out_csv,"w",encoding="utf-8",newline="") as f:
        w = csv.writer(f); w.writerow(["Requirement","GRA_Score"])
        for req,sc in ranks[:10]:
            w.writerow([req, f"{sc:.4f}"])
    with open(out_json,"w",encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[OK] 排名输出：{out_csv}")
    print(f"[OK] 统计输出：{out_json}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", action="store_true", help="创建 docs/, data/, outputs/ 等目录")
    ap.add_argument("--demo", action="store_true", help="读取 FRKG -> 简单闭包 -> GRA 排序")
    args = ap.parse_args()

    if args.init:
        ensure_dirs()
        write_tiny_demo()
        print("[OK] 初始化完成")

    if args.demo:
        ensure_dirs()
        frkg = ROOT/"data/processed/FRKG_label.csv"
        if not frkg.exists():
            write_tiny_demo()
        edges = load_frkg(frkg)
        all_edges, stats = simple_closure(edges)
        sc = build_scores(all_edges)
        ranks = gra_rank(sc)
        write_outputs(ranks, stats)

if __name__ == "__main__":
    main()
