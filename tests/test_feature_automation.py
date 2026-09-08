import polars as pl
from io_detect.features.automation import automation_scores


def test_automation_share():
    df = pl.DataFrame({
        "account_id": ["a1", "a1", "a2"],
        "application": ["bot", "web", "web"],
    })
    out = automation_scores(df)
    a1 = out.filter(pl.col("account_id")=="a1")
    assert abs(a1["automated_share"][0] - 0.5) < 1e-9
