#   Closeworld-Fuzzy-KG-Priority

> **Closed-world fuzzy requirement analysis** using **Symbolic Logic + FRKG** with a **NEV** case study.  
> Ontology → FRKG → Rule-based expansion → Grey Relational Analysis (GRA) multi-criteria ranking → Baseline comparisons.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](#)

## ✨ Highlights
- **Fuzzy Requirement KG (FRKG)**: predicates carry fuzziness $μ^α$, attributes carry confidence $μ^β$.
- **Symbolic rules**: $FSEO$ / $FSSO$ / $FSTO$ / $FSIO$ + $FSTO^{siso/simo/miso/mimo}$ closure (Algorithm 3.1).
- **Multi-criteria ranking**: GRA over heterogeneous features (symbolic/real/semantic/interval).
- **Reproducible NEV case** with data, code, and figures matching the dissertation (Chapter 3).

## 🚀 Quickstart (5 min)
Choose either A (quick demo) or B (your real data).

```bash
git clone https://github.com/mlizhi/closedworld-fuzzy-kg-priority.git
cd closedworld-fuzzy-kg-priority

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### A) Minimal runnable demo
```bash
# 1) create folders (docs/, data/, outputs/)
python scripts/run_quickstart.py --init
# 2) create a tiny demo FRKG and run closure + GRA
python scripts/run_quickstart.py --demo
# results:
# - outputs/ranking_top10.csv
# - outputs/expansion_stats.json
```

### B) Run with your real UAV data
1. Put your raw file into: data/raw/02.用户故事及其类类别278条.xls
2. Generate structured CSV:
```bash
python scripts/UserStoryExtracted.py
```
3. Build KG in Neo4j (optional): see Neo4j (optional) section.
4. Export FRKG with fuzziness to `data/processed/FRKG_label.csv`
   (columns: `Subject, Predicate, Object, SubjectLabels, ObjectLabels, Fuzzy`)
5. Run:
   ```bash
   python scripts/run_quickstart.py --demo
   ```
   (This script will use your `FRKG_label.csv`.)
   >- If you prefer `scripts/run_ranking.py`, keep that entry and mirror the same parameters.
   

## 📂 Repo Structure
```bash
frkg/                  # core library (rules, closure, distances, GRA, metrics)
  ├─ frkg_types.py
  ├─ io_loader.py
  ├─ fuzzy_rules.py
  ├─ closure.py
  ├─ distance.py
  └─ gra.py
scripts/
  ├─ run_quickstart.py # init folders, demo data, closure, GRA
  └─ UserStoryExtracted.py
neo4j/                 # Cypher init & rule expansion (optional)
data/
  ├─ raw/              # 02.用户故事及其类类别278条.xls  (🔶 TODO: place file)
  ├─ processed/        # User_story278.csv, RE_RE.csv, FRKG_label.csv
  └─ README_demo.md
docs/
  ├─ method_overview.md
  └─ figures/          # 🔶 TODO: key figures (e.g., heatmaps)
outputs/               # ranking_top10.csv, expansion_stats.json
```

## 🧠 Method Overview
**中文（对应博士论文第三章《基于模糊知识图谱逻辑推理的专业领域复杂产品需求排序》）**
流程：**本体 → BKG → FRKG(μ^α/μ^β) → 符号规则闭包 → 多准则(GRA)排序**。
- **本体**：定义 Classes / ObjectProperties / DataProperties（见论文表3.1/3.2）。
- **BKG 构建**：从用户故事抽取 User / User_Story / Requirement / Goal 等并建三元组。
- **FRKG**：给谓词边赋模糊度 μ^α；给属性节点赋置信度 μ^β。
- **符号规则**：FSEO/FSSO/FSTO/FSIO 与 FSTO^{siso/simo/miso/mimo} 扩展闭包（算法3.1）。
- **排序**：GRA 综合五个准则（商业价值、用户优先级、可行性、依赖性、成本）。
**English (short)**
Ontology → BKG → FRKG (μ^α/μ^β) → Symbolic rule closure → GRA over five criteria.

## 🧰 Neo4j (optional)
- Init & import (see `neo4j/cypher_init.cypher`)
- FRKG import (fuzzy edge attr `Fuzzy`) + rules (see `neo4j/cypher_rules.cypher`)
- Example snippet (browser):
```cypher
// example: preview inferred edges
MATCH (n)-[r:Inferred]->(m)
RETURN n.name AS Start, r.rule AS Rule, r.Fuzzy AS Fuzzy, type(r) AS Type, m.name AS End
LIMIT 20;
```
>- If you cannot use Neo4j, the pure Python pipeline under `frkg/` runs closure & GRA without a graph database.

## 📊 Results
- `outputs/ranking_top10.csv`: Top-K ranked requirements (GRA).
- `outputs/expansion_stats.json`: counts for **Novelty / ExtraCoverage / Soundness** (per Ch.3 metrics).
- (🔶 TODO) `docs/figures/fig_heatmap.png`: per-criterion score heatmap.
Reproduce figures via notebooks (🔶 TODO: add) or small plotting script (🔶 TODO).

## 📑 Citing
If this repository helps your work, please cite:
```bibtext
@article{ma2024multicriteria,
  title={Multicriteria requirement ranking based on uncertain knowledge representation and reasoning},
  author={Ma, Yufeng and Dou, Yajie and Xu, Xiangqian and Jiang, Jiang and Yang, Kewei and Tan, Yuejin},
  journal={Advanced Engineering Informatics},
  volume={59},
  pages={102329},
  year={2024},
  publisher={Elsevier}
}
```

