import polars as pl
from io_detect.eval.metrics import account_labels, score


def test_account_labels_majority():
    df = pl.DataFrame({"account_id": ["a1", "a1", "a2"], "is_control": [False, False, True]})
    labels = account_labels(df)
    assert labels["a1"] is True   # IO
    assert labels["a2"] is False  # control


def test_score_precision_recall():
    labels = {"a1": True, "a2": True, "a3": False}
    out = score({"a1", "a3"}, labels)
    assert out["tp"] == 1 and out["fp"] == 1 and out["fn"] == 1
    assert abs(out["precision"] - 0.5) < 1e-9
    assert abs(out["recall"] - 0.5) < 1e-9
