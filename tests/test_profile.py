import polars as pl
from io_detect.ingest.profile import profile_file

def test_profile_reports_columns(tmp_path):
    p = tmp_path / "s.csv"
    pl.DataFrame({"a": ["x", "x", None], "b": [1, 2, 3]}).write_csv(p)
    prof = profile_file(str(p))
    cols = {c["name"]: c for c in prof["columns"]}
    assert cols["a"]["null_rate"] > 0
    assert cols["b"]["n_unique"] == 3
