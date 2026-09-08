import networkx as nx
from io_detect.detect.cluster import detect_clusters


def test_detects_dense_cluster_not_loose_pair():
    g = nx.Graph()
    for a, b in [("x1", "x2"), ("x1", "x3"), ("x2", "x3")]:
        g.add_edge(a, b, weight=5)
    g.add_edge("y1", "y2", weight=1)
    clusters = detect_clusters(g, min_size=3, min_avg_weight=2.0)
    assert {"x1", "x2", "x3"} in clusters
    assert all("y1" not in c for c in clusters)


def test_empty_graph_returns_empty_list():
    g = nx.Graph()
    clusters = detect_clusters(g)
    assert clusters == []
