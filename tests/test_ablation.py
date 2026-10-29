from io_detect.eval.ablation import SIGNALS, ablate
from io_detect.ingest.adapters.iu import load_iu


def test_ablate_reports_the_shipped_graph_and_each_signal_alone():
    rows = ablate(load_iu("tests/fixtures/synthetic.csv"))
    assert [r["variant"] for r in rows] == ["both signals", *SIGNALS]


def test_single_signal_graphs_never_outreach_the_pair():
    rows = {r["variant"]: r for r in ablate(load_iu("tests/fixtures/synthetic.csv"))}
    both = rows["both signals"]
    # Dropping a signal only removes edges, so neither variant can flag an account the
    # full graph missed. A single-signal run scoring higher recall means build_graph is
    # losing edges when it merges the two frames.
    for name in SIGNALS:
        assert rows[name]["recall"] <= both["recall"]
        assert rows[name]["pairs"] <= both["pairs"]
