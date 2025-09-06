from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class Node:
    id: str
    labels: tuple  # e.g. ("Requirement",)
    attrs: Dict[str, Any] = None   # may include mu_beta (attribute confidence)

@dataclass(frozen=True)
class Edge:
    s: str
    p: str
    o: str
    mu_alpha: float = 1.0  # predicate fuzziness
    meta: Optional[Dict[str, Any]] = None
