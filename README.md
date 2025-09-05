# FRKG-Symbolic-Priority

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
