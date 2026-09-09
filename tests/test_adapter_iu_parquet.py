import datetime

import polars as pl

from io_detect.ingest.adapters.iu import load_iu_parquet


def _iu_parquet_fixture(path):
    pl.DataFrame(
        {
            "postid": ["p1", "p2"],
            "post_text": ["hello", "world"],
            "application_name": ["072f1b0136", "072f1b0136"],
            "post_language": ["en", None],
            "in_reply_to_postid": [None, None],
            "in_reply_to_accountid": [None, None],
            "post_time": [
                datetime.datetime(2022, 3, 1, 10, 0, 0),
                datetime.datetime(2022, 3, 2, 11, 0, 0),
            ],
            "accountid": ["a1", "a3"],
            "account_profile_description": [None, None],
            "follower_count": [10, 100],
            "following_count": [5, 20],
            "account_creation_date": [
                datetime.date(2021, 1, 1),
                datetime.date(2020, 6, 15),
            ],
            "is_repost": [False, True],
            "reposted_accountid": [None, "a4"],
            "reposted_postid": [None, "p3"],
            "hashtags": [["war", "news"], []],
            "urls": [[], []],
            "account_mentions": [["a2"], []],
            "is_control": [True, False],
        },
        schema_overrides={
            "post_time": pl.Datetime(time_unit="ns"),
            "account_creation_date": pl.Date,
            "hashtags": pl.List(pl.Utf8),
            "urls": pl.List(pl.Utf8),
            "account_mentions": pl.List(pl.Utf8),
        },
    ).write_parquet(path)


def test_load_iu_parquet_maps_to_canonical(tmp_path):
    p = tmp_path / "iu.parquet"
    _iu_parquet_fixture(p)
    df = load_iu_parquet(str(p))

    row = df.row(0, named=True)
    assert row["post_id"] == "p1"
    assert row["hashtags"] == ["war", "news"]
    assert row["mentions"] == ["a2"]
    assert row["urls"] == []
    assert row["source"] == "iu_2411.10609"
    assert row["is_control"] is True
    assert row["label"] == "control"
    assert row["label_scheme"] == "iu_2411.10609"
    assert row["actor_role"] is None
    assert row["account_region"] is None

    row2 = df.row(1, named=True)
    assert row2["hashtags"] == []
    assert row2["mentions"] == []
    assert row2["is_control"] is False
    assert row2["label"] == "io"

    # dtype conformance, including the Date -> Datetime cast for account_created
    assert df.schema["timestamp"] == pl.Datetime
    assert df.schema["account_created"] == pl.Datetime
    assert df.schema["hashtags"] == pl.List(pl.Utf8)
    assert df.schema["urls"] == pl.List(pl.Utf8)
    assert df.schema["mentions"] == pl.List(pl.Utf8)
