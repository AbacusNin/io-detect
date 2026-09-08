import polars as pl
from io_detect.detect.graph import build_graph


def test_build_graph_sums_weights():
    f1 = pl.DataFrame({"account_a": ["a1"], "account_b": ["a2"], "n_shared": [2]})
    f2 = pl.DataFrame({"account_a": ["a1"], "account_b": ["a2"], "n_shared": [3]})
    g = build_graph(f1, f2)
    assert g["a1"]["a2"]["weight"] == 5
