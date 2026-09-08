import polars as pl


def triage(cluster: set[str], automation_df: pl.DataFrame) -> pl.DataFrame:
    sub = automation_df.filter(pl.col("account_id").is_in(list(cluster)))
    return sub.with_columns(
        pl.when(pl.col("automated_share") >= 0.5)
        .then(pl.lit("automated_core"))
        .otherwise(pl.lit("amplifier"))
        .alias("role")
    ).select(["account_id", "automated_share", "role"])
