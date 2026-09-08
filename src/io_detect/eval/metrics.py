import polars as pl


def account_labels(df: pl.DataFrame) -> dict[str, bool]:
    """Derive per-account IO vs control labels by majority vote over posts.

    IO account = not control. An account is IO if the share of its non-control
    posts is >= 0.5.

    Args:
        df: DataFrame with columns account_id and is_control

    Returns:
        dict mapping account_id to bool (True = IO, False = control)
    """
    agg = df.group_by("account_id").agg((~pl.col("is_control")).mean().alias("io_share"))
    return {r["account_id"]: r["io_share"] >= 0.5 for r in agg.iter_rows(named=True)}


def score(flagged: set[str], labels: dict[str, bool]) -> dict:
    """Score flagged accounts against ground-truth labels.

    Args:
        flagged: set of flagged account IDs
        labels: dict mapping account_id to bool (True = IO, False = control)

    Returns:
        dict with keys: precision, recall, tp, fp, fn, n_positive
    """
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
