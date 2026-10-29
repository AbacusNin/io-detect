import polars as pl

from io_detect.detect.cluster import detect_clusters
from io_detect.detect.graph import build_graph
from io_detect.eval.metrics import account_labels, score
from io_detect.features.content import duplicate_pairs
from io_detect.features.repost import coreposts

# Only these two build the graph, so only these two can move precision or recall.
# Hashtag flooding, swarming and automation set DISARM tags and triage roles, which
# means dropping them leaves the flagged set untouched and makes them nothing to ablate.
SIGNALS = ("co-repost timing", "duplicate text")


def ablate(df: pl.DataFrame) -> list[dict]:
    """Score the shipped graph, then each of its two signals on its own."""
    labels = account_labels(df)
    frames = {"co-repost timing": coreposts(df), "duplicate text": duplicate_pairs(df)}
    variants = [("both signals", SIGNALS)] + [(name, (name,)) for name in SIGNALS]

    rows = []
    for variant, names in variants:
        flagged = set()
        for cluster in detect_clusters(build_graph(*(frames[n] for n in names))):
            flagged |= cluster
        rows.append({
            "variant": variant,
            "pairs": sum(frames[n].height for n in names),
            "flagged": len(flagged),
            **score(flagged, labels),
        })
    return rows
