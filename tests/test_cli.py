import pytest
from io_detect.cli import build_parser, LOADERS
from io_detect.ingest.adapters.iu import load_iu, load_iu_parquet
from io_detect.ingest.adapters.clemson import load_clemson


def test_unknown_source_rejected():
    p = build_parser()
    with pytest.raises(SystemExit):
        p.parse_args(["detect", "--input", "x", "--source", "bogus"])


def test_source_defaults_to_iu():
    p = build_parser()
    args = p.parse_args(["detect", "--input", "x"])
    assert args.source == "iu"


def test_loaders_map_known_sources():
    assert LOADERS["iu"] is load_iu
    assert LOADERS["iu-parquet"] is load_iu_parquet
    assert LOADERS["clemson"] is load_clemson
