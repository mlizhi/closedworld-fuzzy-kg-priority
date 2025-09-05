#   Closeworld-Fuzzy-KG-Priority

> **Closed-world fuzzy requirement analysis** using **Symbolic Logic + FRKG** with a **NEV** case study.  
> Ontology → FRKG → Rule-based expansion → Grey Relational Analysis (GRA) multi-criteria ranking → Baseline comparisons.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](#)

## ✨ Highlights
- **Fuzzy Requirement KG (FRKG)**: predicates carry fuzziness μ^α, attributes carry confidence μ^β.
- **Symbolic rules**: FSEO / FSSO / FSTO / FSIO + FSTO^{siso/simo/miso/mimo} closure (Algorithm 3.1).
- **Multi-criteria ranking**: GRA over heterogeneous features (symbolic/real/semantic/interval).
- **Reproducible NEV case** with data, code, and figures matching the dissertation (Chapter 3).

## 🚀 Quickstart (5 min)
```bash
git clone https://github.com/<yourname>/FRKG-Symbolic-Priority.git
cd FRKG-Symbolic-Priority
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_ranking.py --demo
```
This runs: ontology load → FRKG build → rule expansion → GRA ranking → top-K outputs.


## 📂 Repo Structure
- `frkg/`: core library (rules, closure, distances, GRA, metrics)
- `notebooks/`: step-by-step demos
- `neo4j/`: Cypher init & queries (optional)
- `data/demo/`: minimal runnable demo dataset (anonymized or synthetic)
- `docs/`: method overview + figures

## 🧠 Method Overview
- FRKG definition with μ^α (predicate fuzziness) & μ^β (attribute confidence).
- Symbolic closure adds implicit edges; we report **Novelty, ExtraCoverage, Soundness**.
- Ranking uses GRA with five criteria: business value, user priority, feasibility, dependency, cost.

## 📊 Results (Demo)
- Heatmap of per-criterion scores, Top-10 ranked requirements, baseline comparisons.
- Reproduce figures via `notebooks/40_multi_criteria_gra.ipynb and scripts/export_figures.py`.

## 🧪 Baselines
TOPSIS / VIKOR / MULTIMOORA are provided in `notebooks/50_baselines_compare.ipynb`.

## 📑 Citing
If this repository helps your work, please cite:
Ma, Yufeng, et al. "Multicriteria requirement ranking based on uncertain knowledge representation and reasoning." Advanced Engineering Informatics 59 (2024): 102329.

