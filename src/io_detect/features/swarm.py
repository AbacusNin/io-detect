import polars as pl


def swarm_targets(df: pl.DataFrame, window_seconds: int = 300) -> pl.DataFrame:
    m = df.explode("mentions", empty_as_null=True).rename({"mentions": "target"}).select(
        ["account_id", "target", "timestamp"]
    )
    reps = df.filter(pl.col("in_reply_to_account_id").is_not_null()).select([
        "account_id",
        pl.col("in_reply_to_account_id").alias("target"),
        "timestamp",
    ])
    both = pl.concat([m, reps]).filter(pl.col("target").is_not_null())
    both = both.with_columns(pl.col("timestamp").dt.truncate(f"{window_seconds}s").alias("window_start"))
    return both.group_by(["target", "window_start"]).agg(
        pl.col("account_id").n_unique().alias("n_attackers")
    )
