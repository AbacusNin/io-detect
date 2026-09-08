from io_detect.taxonomy.disarm import TECHNIQUES

_MAP = {
    "has_corepost": "T0040",
    "has_duplicate_flood": "T0044",
    "has_hashtag_flood": "T0043",
    "has_swarm": "T0041",
    "has_automation": "T0037",
}


def tag(signals: dict) -> list[str]:
    ids = {tid for key, tid in _MAP.items() if signals.get(key)}
    assert ids <= set(TECHNIQUES)
    return sorted(ids)
