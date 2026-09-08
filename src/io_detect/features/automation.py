import polars as pl


def automation_scores(df: pl.DataFrame,
                      automated_apps=frozenset({"bot", "api", "scheduler"})) -> pl.DataFrame:
    d = df.with_columns(
        pl.col("application").str.to_lowercase().is_in(list(automated_apps)).alias("is_auto")
    )
    return d.group_by("account_id").agg(
        pl.col("is_auto").mean().alias("automated_share"),
        pl.len().alias("post_count"),
    )
