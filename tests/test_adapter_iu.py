import polars as pl
from io_detect.ingest.adapters.iu import load_iu


def _iu_fixture(path):
    pl.DataFrame({
        "postid": ["p1"], "accountid": ["a1"],
        "post_time": ["2022-03-01 10:00:00"], "post_text": ["hello"],
        "post_language": ["en"], "in_reply_to_postid": [None],
        "in_reply_to_accountid": [None], "is_repost": [False],
        "reposted_accountid": [None], "reposted_postid": [None],
        "hashtags": ["war,news"], "urls": [""], "account_mentions": ["a2"],
        "application_name": ["web"], "account_creation_date": ["2021-01-01 00:00:00"],
        "follower_count": [10], "following_count": [5], "is_control": [True],
    }).write_csv(path)


def test_load_iu_maps_to_canonical(tmp_path):
    p = tmp_path / "iu.csv"
    _iu_fixture(p)
    df = load_iu(str(p))
    row = df.row(0, named=True)
    assert row["post_id"] == "p1"
    assert row["hashtags"] == ["war", "news"]
    assert row["mentions"] == ["a2"]
    assert row["source"] == "iu_2411.10609"
    assert row["is_control"] is True
