def novelty(original_edges:int, overall_edges:int)->float:
    # 式(3-11)
    return abs(overall_edges - original_edges) / max(overall_edges,1)

def extra_coverage(original_size:int, overall_size:int)->float:
    # 式(3-12)
    return abs(overall_size - original_size) / max(original_size,1)

def soundness(valid_implicit:int, original_edges:int, overall_edges:int)->float:
    # 式(3-13)
    denom = abs(overall_edges - original_edges)
    return (valid_implicit / denom) if denom>0 else 0.0
