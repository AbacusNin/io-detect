import polars as pl

class SchemaError(ValueError):
    pass

CANONICAL_SCHEMA: dict[str, pl.DataType] = {
    "post_id": pl.Utf8,
    "account_id": pl.Utf8,
    "timestamp": pl.Datetime,
    "text": pl.Utf8,
    "language": pl.Utf8,
    "in_reply_to_post_id": pl.Utf8,
    "in_reply_to_account_id": pl.Utf8,
    "is_repost": pl.Boolean,
    "reposted_account_id": pl.Utf8,
    "reposted_post_id": pl.Utf8,
    "hashtags": pl.List(pl.Utf8),
    "urls": pl.List(pl.Utf8),
    "mentions": pl.List(pl.Utf8),
    "application": pl.Utf8,
    "account_created": pl.Datetime,
    "followers": pl.Int64,
    "following": pl.Int64,
    "is_control": pl.Boolean,
    "source": pl.Utf8,
    "label": pl.Utf8,
    "label_scheme": pl.Utf8,
    "actor_role": pl.Utf8,
    "actor_role_scheme": pl.Utf8,
    "account_region": pl.Utf8,
}

def validate_frame(df: pl.DataFrame) -> pl.DataFrame:
    missing = [c for c in CANONICAL_SCHEMA if c not in df.columns]
    if missing:
        raise SchemaError(f"missing columns: {missing}")
    return df
