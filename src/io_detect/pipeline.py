import polars as pl

from io_detect.features.repost import coreposts
from io_detect.features.content import duplicate_pairs, hashtag_flood
from io_detect.features.swarm import swarm_targets
from io_detect.features.automation import automation_scores
from io_detect.detect.graph import build_graph
from io_detect.detect.cluster import detect_clusters
from io_detect.detect.triage import triage
from io_detect.taxonomy.tagging import tag
from io_detect.eval.metrics import account_labels, score


def run(df: pl.DataFrame) -> dict:
    cr = coreposts(df)
    dup = duplicate_pairs(df)
    graph = build_graph(cr, dup)
    clusters = detect_clusters(graph)
    auto = automation_scores(df)

    flagged = set()
    triaged = []
    for c in clusters:
        flagged |= c
        triaged.append(triage(c, auto))

    signals = {
        "has_corepost": cr.height > 0,
        "has_duplicate_flood": dup.height > 0,
        "has_hashtag_flood": hashtag_flood(df).filter(pl.col("n_accounts") > 1).height > 0,
        "has_swarm": swarm_targets(df).filter(pl.col("n_attackers") > 1).height > 0,
        "has_automation": auto.filter(pl.col("automated_share") > 0).height > 0,
    }
    tag_ids = tag(signals)
    metrics = score(flagged, account_labels(df))

    return {
        "clusters": [sorted(c) for c in clusters],
        "flagged_accounts": flagged,
        "tags": tag_ids,
        "metrics": metrics,
        "triage": triaged,
    }
