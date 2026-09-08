from io_detect.ingest.adapters.iu import load_iu
from io_detect.pipeline import run


def test_pipeline_flags_planted_cluster():
    df = load_iu("tests/fixtures/synthetic.csv")
    out = run(df)
    assert len(out["clusters"]) >= 1
    assert "T0040" in out["tags"]
    assert out["metrics"]["recall"] > 0.5
