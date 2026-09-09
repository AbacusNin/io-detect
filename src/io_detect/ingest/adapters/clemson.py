import polars as pl
from io_detect.ingest.schema import CANONICAL_SCHEMA, validate_frame

_RENAME = {
    "tweet_id": "post_id", "author": "account_id", "content": "text",
    "region": "account_region", "account_category": "actor_role",
}

_TCO_COLS = ["tco1_step1", "tco2_step1", "tco3_step1"]


def load_clemson(path_glob: str) -> pl.DataFrame:
    df = pl.read_csv(path_glob, infer_schema_length=10000)
    df = df.rename(_RENAME)
    df = df.with_columns([
        pl.col("publish_date").str.to_datetime("%m/%d/%Y %H:%M", strict=False).alias("timestamp"),
        (pl.col("retweet") == 1).alias("is_repost"),
        pl.concat_list([pl.col(c) for c in _TCO_COLS]).list.drop_nulls().alias("urls"),
        pl.lit([], dtype=pl.List(pl.Utf8)).alias("hashtags"),
        pl.lit([], dtype=pl.List(pl.Utf8)).alias("mentions"),
        pl.lit(None, dtype=pl.Utf8).alias("in_reply_to_post_id"),
        pl.lit(None, dtype=pl.Utf8).alias("in_reply_to_account_id"),
        pl.lit(None, dtype=pl.Utf8).alias("reposted_post_id"),
        pl.lit(None, dtype=pl.Utf8).alias("reposted_account_id"),
        pl.lit(None, dtype=pl.Utf8).alias("application"),
        pl.lit(None, dtype=pl.Datetime).alias("account_created"),
        pl.lit("io").alias("label"),
        pl.lit("clemson_ira_positives").alias("label_scheme"),
        pl.lit(False).alias("is_control"),
        pl.lit("clemson_linvill_warren").alias("actor_role_scheme"),
        pl.lit("clemson_538_ira").alias("source"),
    ])
    df = df.select([pl.col(c).cast(t) for c, t in CANONICAL_SCHEMA.items()])
    return validate_frame(df)
