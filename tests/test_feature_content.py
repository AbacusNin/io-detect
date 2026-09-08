import polars as pl
from datetime import datetime
from io_detect.features.content import duplicate_pairs, hashtag_flood

def test_duplicate_pairs_matches_identical_text():
    df = pl.DataFrame({
        "account_id": ["a1", "a2", "a3"],
        "text": ["Vote NOW!!!", "vote now !!!", "different"],
    })
    out = duplicate_pairs(df)
    assert out.filter((pl.col("account_a")=="a1") & (pl.col("account_b")=="a2")).height == 1

def test_hashtag_flood_counts_accounts():
    df = pl.DataFrame({
        "account_id": ["a1", "a2"],
        "hashtags": [["war"], ["war"]],
        "timestamp": [datetime(2022,3,1,10,0,0), datetime(2022,3,1,10,1,0)],
    })
    out = hashtag_flood(df, window_seconds=300)
    assert out.filter(pl.col("hashtag")=="war")["n_accounts"].max() == 2

def test_duplicate_pairs_handles_duplicate_texts():
    """
    Test that n_shared counts distinct shared texts, not paired rows.
    a1 posts the same normalized text twice, a2 posts it once.
    Should have n_shared=1 (one distinct shared text), not 2 (two paired rows).
    """
    df = pl.DataFrame({
        "account_id": ["a1", "a1", "a2"],
        "text": ["Vote NOW!!!", "vote now !!!", "vote now"],
    })
    out = duplicate_pairs(df)
    pair = out.filter((pl.col("account_a") == "a1") & (pl.col("account_b") == "a2"))
    assert pair.height == 1, "Should have exactly one output row for (a1, a2)"
    assert pair["n_shared"][0] == 1, "Should count 1 distinct shared text, not 2 rows"
