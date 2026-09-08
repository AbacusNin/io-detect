import polars as pl
import pytest
from io_detect.ingest.schema import CANONICAL_SCHEMA, validate_frame, SchemaError

def _valid_df():
    return pl.DataFrame(
        {c: [] for c in CANONICAL_SCHEMA}, schema=CANONICAL_SCHEMA
    )

def test_valid_frame_passes():
    df = _valid_df()
    assert validate_frame(df) is df

def test_missing_column_raises():
    df = _valid_df().drop("is_control")
    with pytest.raises(SchemaError):
        validate_frame(df)
