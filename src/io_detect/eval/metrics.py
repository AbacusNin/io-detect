import polars as pl


def account_labels(df: pl.DataFrame) -> dict[str, bool]:
    # IO account if >= 50% of its posts are non-control
    agg = df.group_by("account_id").agg((~pl.col("is_control")).mean().alias("io_share"))
    return {r["account_id"]: r["io_share"] >= 0.5 for r in agg.iter_rows(named=True)}


def score(flagged: set[str], labels: dict[str, bool]) -> dict:
    positives = {a for a, is_io in labels.items() if is_io}
    tp = len(flagged & positives)
    fp = len(flagged - positives)
    fn = len(positives - flagged)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "n_positive": len(positives),
    }
