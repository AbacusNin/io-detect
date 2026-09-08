import polars as pl
from datetime import datetime
from io_detect.features.repost import coreposts

def test_coreposts_counts_shared_targets():
    df = pl.DataFrame({
        "account_id": ["a1", "a2", "a3"],
        "reposted_post_id": ["orig", "orig", "other"],
        "is_repost": [True, True, True],
        "timestamp": [datetime(2022,3,1,10,0,0), datetime(2022,3,1,10,0,30),
                      datetime(2022,3,1,10,0,10)],
    })
    out = coreposts(df, window_seconds=60)
    pair = out.filter((pl.col("account_a") == "a1") & (pl.col("account_b") == "a2"))
    assert pair["n_shared"][0] == 1
    assert out.filter(pl.col("account_b") == "a3").height == 0
