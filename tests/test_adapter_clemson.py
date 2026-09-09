import polars as pl
from io_detect.ingest.adapters.clemson import load_clemson
from io_detect.ingest.schema import CANONICAL_SCHEMA


def _clemson_fixture(path):
    pl.DataFrame({
        "external_author_id": ["906000000000000000", "906000000000000000", "906000000000000000"],
        "author": ["10_GOP", "10_GOP", "10_GOP"],
        "content": ["first tweet text", "retweeted text", "no urls here"],
        "region": ["Unknown", "Unknown", "United States"],
        "language": ["English", "English", "English"],
        "publish_date": ["10/1/2017 19:58", "10/1/2017 22:43", "10/2/2017 08:00"],
        "harvested_date": ["10/1/2017 19:59", "10/1/2017 22:43", "10/2/2017 08:01"],
        "following": [1052, 1054, 1060],
        "followers": [9636, 9637, 9640],
        "updates": [253, 254, 260],
        "post_type": [None, "RETWEET", None],
        "account_type": ["Right", "Right", "Right"],
        "retweet": [0, 1, 0],
        "account_category": ["RightTroll", "RightTroll", "NewsFeed"],
        "new_june_2018": [0, 0, 0],
        "alt_external_id": ["905874659358453760", "905874659358453760", "905874659358453760"],
        "tweet_id": ["914580356430536707", "914621840496189440", "914639143690555392"],
        "article_url": [
            "http://twitter.com/905874659358453760/statuses/914580356430536707",
            "http://twitter.com/905874659358453760/statuses/914621840496189440",
            "http://twitter.com/905874659358453760/statuses/914639143690555392",
        ],
        "tco1_step1": ["https://t.co/gh6g0D1oiC", "https://t.co/mLH1i30LZZ", None],
        "tco2_step1": ["https://t.co/other1", None, None],
        "tco3_step1": [None, None, None],
    }).write_csv(path)


def test_load_clemson_maps_to_canonical(tmp_path):
    p = tmp_path / "clemson.csv"
    _clemson_fixture(p)
    df = load_clemson(str(p))

    assert set(CANONICAL_SCHEMA) <= set(df.columns)

    row = df.row(0, named=True)
    assert row["post_id"] == "914580356430536707"
    assert row["account_id"] == "10_GOP"
    assert row["text"] == "first tweet text"
    assert row["is_repost"] is False
    assert row["urls"] == ["https://t.co/gh6g0D1oiC", "https://t.co/other1"]
    assert row["label"] == "io"
    assert row["label_scheme"] == "clemson_ira_positives"
    assert row["is_control"] is False
    assert row["actor_role"] == "RightTroll"
    assert row["actor_role_scheme"] == "clemson_linvill_warren"
    assert row["account_region"] == "Unknown"
    assert row["source"] == "clemson_538_ira"
    assert row["hashtags"] == []
    assert row["mentions"] == []

    row2 = df.row(1, named=True)
    assert row2["is_repost"] is True
    assert row2["urls"] == ["https://t.co/mLH1i30LZZ"]

    row3 = df.row(2, named=True)
    assert row3["urls"] == []
    assert row3["actor_role"] == "NewsFeed"
    assert row3["account_region"] == "United States"

    assert df.schema["timestamp"] == pl.Datetime
