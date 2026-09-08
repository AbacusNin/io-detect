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

def test_coreposts_handles_duplicate_reposts():
    """
    Test that n_shared counts distinct shared originals, not paired rows.
    a1 reposts the same original twice, a2 reposts it once.
    Should have n_shared=1 (one distinct shared original), not 2 (two paired rows).
    """
    df = pl.DataFrame({
        "account_id": ["a1", "a1", "a2"],
        "reposted_post_id": ["orig", "orig", "orig"],
        "is_repost": [True, True, True],
        "timestamp": [
            datetime(2022, 3, 1, 10, 0, 0),
            datetime(2022, 3, 1, 10, 0, 5),
            datetime(2022, 3, 1, 10, 0, 2),
        ],
    })
    out = coreposts(df, window_seconds=60)
    pair = out.filter((pl.col("account_a") == "a1") & (pl.col("account_b") == "a2"))
    assert pair.height == 1, "Should have exactly one output row for (a1, a2)"
    assert pair["n_shared"][0] == 1, "Should count 1 distinct shared original, not 2 rows"
