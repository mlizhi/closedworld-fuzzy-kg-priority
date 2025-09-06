import pandas as pd
import networkx as nx

def load_frkg_from_csv(path: str) -> nx.MultiDiGraph:
    """CSV columns: Subject, Predicate, Object, SubjectLabels, ObjectLabels, Fuzzy"""
    df = pd.read_csv(path)
    g = nx.MultiDiGraph()
    for _, row in df.iterrows():
        sl = tuple(map(str.strip, str(row.get("SubjectLabels","")).replace("[","").replace("]","").split(","))) if pd.notna(row.get("SubjectLabels")) else ()
        ol = tuple(map(str.strip, str(row.get("ObjectLabels","")).replace("[","").replace("]","").split(","))) if pd.notna(row.get("ObjectLabels")) else ()
        g.add_node(row["Subject"], labels=sl)
        g.add_node(row["Object"], labels=ol)
        g.add_edge(row["Subject"], row["Object"], key=row["Predicate"], p=row["Predicate"],
                   mu_alpha=float(row.get("Fuzzy",1)) if pd.notna(row.get("Fuzzy")) else 1.0,
                   inferred=False, rule=None)
    return g

def to_edge_list(g: nx.MultiDiGraph):
    for u,v,k,data in g.edges(keys=True, data=True):
        yield (u, data.get("p",k), v, data.get("mu_alpha",1.0), data.get("inferred",False), data.get("rule"))
