import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


def _avg_internal_weight(graph: nx.Graph, nodes: set[str]) -> float:
    sub = graph.subgraph(nodes)
    if sub.number_of_edges() == 0:
        return 0.0
    return sum(d["weight"] for _, _, d in sub.edges(data=True)) / sub.number_of_edges()


def detect_clusters(graph, min_size: int = 3, min_avg_weight: float = 2.0) -> list[set[str]]:
    if graph.number_of_edges() == 0:
        return []
    out = []
    for comm in greedy_modularity_communities(graph, weight="weight"):
        nodes = set(comm)
        if len(nodes) >= min_size and _avg_internal_weight(graph, nodes) >= min_avg_weight:
            out.append(nodes)
    return out
