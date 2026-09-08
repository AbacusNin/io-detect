import polars as pl
from datetime import datetime
from io_detect.features.swarm import swarm_targets


def test_swarm_counts_distinct_attackers_on_target():
    df = pl.DataFrame({
        "account_id": ["a1", "a2"],
        "mentions": [["victim"], ["victim"]],
        "in_reply_to_account_id": [None, None],
        "timestamp": [datetime(2022,3,1,10,0,0), datetime(2022,3,1,10,1,0)],
    })
    out = swarm_targets(df, window_seconds=300)
    assert out.filter(pl.col("target")=="victim")["n_attackers"].max() == 2
