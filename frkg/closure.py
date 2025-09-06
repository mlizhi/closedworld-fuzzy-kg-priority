from .fuzzy_rules import fsto_siso, fsto_simo, fsto_miso, fsto_mimo

def closure_expand(g, max_iter=5):
    """按算法3.1思想迭代直到无新增或到达上限"""
    total_added = 0
    for _ in range(max_iter):
        added = 0
        added += fsto_siso(g)
        added += fsto_simo(g)
        added += fsto_miso(g)
        added += fsto_mimo(g)
        total_added += added
        if added == 0:
            break
    return total_added
