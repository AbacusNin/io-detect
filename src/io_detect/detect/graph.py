import networkx as nx
import polars as pl


def build_graph(*pair_frames: pl.DataFrame, min_weight: int = 1) -> nx.Graph:
    g = nx.Graph()
    for frame in pair_frames:
        for row in frame.iter_rows(named=True):
            a, b, w = row["account_a"], row["account_b"], row["n_shared"]
            if g.has_edge(a, b):
                g[a][b]["weight"] += w
            else:
                g.add_edge(a, b, weight=w)
    if min_weight > 1:
        drop = [(a, b) for a, b, d in g.edges(data=True) if d["weight"] < min_weight]
        g.remove_edges_from(drop)
    return g
