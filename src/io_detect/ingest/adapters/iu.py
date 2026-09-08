import polars as pl
from io_detect.ingest.schema import CANONICAL_SCHEMA, validate_frame

_RENAME = {
    "postid": "post_id", "accountid": "account_id", "post_time": "timestamp",
    "post_text": "text", "post_language": "language",
    "in_reply_to_postid": "in_reply_to_post_id",
    "in_reply_to_accountid": "in_reply_to_account_id",
    "reposted_accountid": "reposted_account_id",
    "reposted_postid": "reposted_post_id",
    "account_mentions": "mentions", "application_name": "application",
    "account_creation_date": "account_created",
    "follower_count": "followers", "following_count": "following",
}


def _split(col: str) -> pl.Expr:
    return (
        pl.when(pl.col(col).is_null() | (pl.col(col) == ""))
        .then(pl.lit([], dtype=pl.List(pl.Utf8)))
        .otherwise(pl.col(col).str.split(","))
        .alias(col)
    )


def load_iu(path: str) -> pl.DataFrame:
    df = pl.read_csv(path, infer_schema_length=10000)
    df = df.rename(_RENAME)
    df = df.with_columns([
        pl.col("timestamp").str.to_datetime(strict=False),
        pl.col("account_created").str.to_datetime(strict=False),
        _split("hashtags"), _split("urls"), _split("mentions"),
    ])
    df = df.with_columns(pl.lit("iu_2411.10609").alias("source"))
    df = df.select([pl.col(c).cast(t) for c, t in CANONICAL_SCHEMA.items()])
    return validate_frame(df)


def load_iu_parquet(path_glob: str) -> pl.DataFrame:
    """Load real IU parquet parts. List columns already List(String); no comma-splitting."""
    df = pl.read_parquet(path_glob)
    df = df.rename(_RENAME)
    df = df.with_columns(pl.lit("iu_2411.10609").alias("source"))
    df = df.select([pl.col(c).cast(t) for c, t in CANONICAL_SCHEMA.items()])
    return validate_frame(df)
