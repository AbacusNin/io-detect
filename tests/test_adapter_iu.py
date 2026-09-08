import polars as pl
from io_detect.ingest.adapters.iu import load_iu


def _iu_fixture(path):
    pl.DataFrame({
        "postid": ["p1", "p2"], "accountid": ["a1", "a3"],
        "post_time": ["2022-03-01 10:00:00", "2022-03-02 11:00:00"],
        "post_text": ["hello", "world"],
        "post_language": ["en", "en"], "in_reply_to_postid": [None, None],
        "in_reply_to_accountid": [None, None], "is_repost": [False, True],
        "reposted_accountid": [None, "a4"], "reposted_postid": [None, "p3"],
        "hashtags": ["war,news", None], "urls": ["", ""], "account_mentions": ["a2", None],
        "application_name": ["web", "mobile"], "account_creation_date": ["2021-01-01 00:00:00", "2020-06-15 14:30:00"],
        "follower_count": [10, 100], "following_count": [5, 20], "is_control": [True, False],
    }).write_csv(path)


def test_load_iu_maps_to_canonical(tmp_path):
    p = tmp_path / "iu.csv"
    _iu_fixture(p)
    df = load_iu(str(p))

    # Test first row
    row = df.row(0, named=True)
    assert row["post_id"] == "p1"
    assert row["hashtags"] == ["war", "news"]
    assert row["mentions"] == ["a2"]
    assert row["urls"] == []  # Empty string must map to empty list
    assert row["source"] == "iu_2411.10609"
    assert row["is_control"] is True

    # Test dtype conformance
    assert df.schema["timestamp"] == pl.Datetime
    assert df.schema["account_created"] == pl.Datetime

    # Test genuine-null case: p2 has None for hashtags and mentions
    row2 = df.row(1, named=True)
    assert row2["hashtags"] == []  # None must map to empty list
    assert row2["mentions"] == []  # None must map to empty list
    assert row2["urls"] == []  # Empty string must map to empty list
