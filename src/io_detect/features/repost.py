import polars as pl

def coreposts(df: pl.DataFrame, window_seconds: int = 60) -> pl.DataFrame:
    r = df.filter(pl.col("is_repost") & pl.col("reposted_post_id").is_not_null())
    r = r.select(["account_id", "reposted_post_id", "timestamp"])
    j = r.join(r, on="reposted_post_id", suffix="_b")
    j = j.filter(pl.col("account_id") < pl.col("account_id_b"))
    j = j.filter(
        (pl.col("timestamp") - pl.col("timestamp_b")).dt.total_seconds().abs()
        <= window_seconds
    )
    return (
        j.group_by(["account_id", "account_id_b"])
        .agg(pl.len().alias("n_shared"))
        .rename({"account_id": "account_a", "account_id_b": "account_b"})
    )
