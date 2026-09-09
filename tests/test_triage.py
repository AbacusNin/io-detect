import polars as pl
from io_detect.detect.triage import triage


def test_triage_labels_core_and_amplifier():
    auto = pl.DataFrame({
        "account_id": ["a1", "a2"],
        "automated_share": [0.9, 0.1], "post_count": [10, 10],
    })
    out = triage({"a1", "a2"}, auto)
    roles = dict(zip(out["account_id"], out["role"]))
    assert roles["a1"] == "automated_core"
    assert roles["a2"] == "amplifier"


def test_triage_boundary_at_half_is_automated_core():
    auto = pl.DataFrame({
        "account_id": ["a1"],
        "automated_share": [0.5], "post_count": [10],
    })
    out = triage({"a1"}, auto)
    roles = dict(zip(out["account_id"], out["role"]))
    assert roles["a1"] == "automated_core"


def test_triage_excludes_accounts_outside_cluster():
    auto = pl.DataFrame({
        "account_id": ["a1", "a2"],
        "automated_share": [0.9, 0.1], "post_count": [10, 10],
    })
    out = triage({"a1"}, auto)
    assert set(out["account_id"]) == {"a1"}
