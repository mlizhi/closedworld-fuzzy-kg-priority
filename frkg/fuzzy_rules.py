import networkx as nx

def _add_edge(g,u,p,v,mu,rule):
    existing = [d for _,_,d in g.edges(u, data=True) if d.get("p")==p and _==v]
    if existing:
        # keep the max mu_alpha
        for d in existing:
            d["mu_alpha"] = max(d.get("mu_alpha",1.0), mu)
            d["inferred"] = True
            d["rule"] = rule
        return False
    g.add_edge(u,v,key=p,p=p,mu_alpha=mu,inferred=True,rule=rule)
    return True

def fsto_siso(g: nx.MultiDiGraph) -> int:
    added = 0
    for x,y,dr in g.edges(data=True):
        for z,_,dp in g.in_edges(x, data=True):
            mu = dr.get("mu_alpha",1.0)*dp.get("mu_alpha",1.0)
            if _add_edge(g,z,dr["p"],y,mu,"FSTO_siso"): added+=1
    return added

def fsto_simo(g: nx.MultiDiGraph) -> int:
    added = 0
    for x,y,dr in g.edges(data=True):
        for _,z,dp in g.edges(x, data=True):
            mu = dr.get("mu_alpha",1.0)*dp.get("mu_alpha",1.0)
            if _add_edge(g,z,dr["p"],y,mu,"FSTO_simo"): added+=1
    return added

def fsto_miso(g: nx.MultiDiGraph) -> int:
    added = 0
    for x,y,dr1 in g.edges(data=True):
        for z1,_,dr2 in g.in_edges(x, data=True):
            mu = dr1.get("mu_alpha",1.0)*dr2.get("mu_alpha",1.0)
            if _add_edge(g,z1,dr1["p"],y,mu,"FSTO_miso"): added+=1
    return added

def fsto_mimo(g: nx.MultiDiGraph) -> int:
    added = 0
    for x,y,dr1 in g.edges(data=True):
        for z1,_,dr2 in g.in_edges(x, data=True):
            for _,z2,dr3 in g.edges(y, data=True):
                mu = dr1.get("mu_alpha",1.0)*dr2.get("mu_alpha",1.0)*dr3.get("mu_alpha",1.0)
                added += int(_add_edge(g,z1,dr1["p"],y,mu,"FSTO_mimo"))
                added += int(_add_edge(g,z2,dr1["p"],x,mu,"FSTO_mimo"))
    return added
