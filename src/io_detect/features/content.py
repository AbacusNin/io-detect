import polars as pl

def _norm(col: str) -> pl.Expr:
    return (
        pl.col(col).str.to_lowercase()
        .str.replace_all(r"[^\w\s]", "")
        .str.replace_all(r"\s+", " ")
        .str.strip_chars()
        .alias("norm")
    )

def duplicate_pairs(df: pl.DataFrame) -> pl.DataFrame:
    d = df.select(["account_id", _norm("text")]).filter(pl.col("norm") != "")
    j = d.join(d, on="norm", suffix="_b").filter(pl.col("account_id") < pl.col("account_id_b"))
    return (
        j.group_by(["account_id", "account_id_b"])
        .agg(pl.col("norm").n_unique().alias("n_shared"))
        .rename({"account_id": "account_a", "account_id_b": "account_b"})
    )

def hashtag_flood(df: pl.DataFrame, window_seconds: int = 300) -> pl.DataFrame:
    e = df.explode("hashtags").rename({"hashtags": "hashtag"}).filter(pl.col("hashtag").is_not_null())
    e = e.with_columns(pl.col("timestamp").dt.truncate(f"{window_seconds}s").alias("window_start"))
    return e.group_by(["hashtag", "window_start"]).agg(
        pl.len().alias("n_posts"),
        pl.col("account_id").n_unique().alias("n_accounts"),
    )
