# results

`Russia_2-metrics.json` is the real output of one full pipeline run against
the Indiana University "Russia_2" influence-operation campaign file
(1,011,052 rows, 21 gzip-parquet parts). Precision and recall in that file
are measured against the corpus's own `is_control` labels, scored at account
granularity; see `docs/methodology/control-construction.md` for exactly how
that control set is built, the honesty caveats that apply to every number in
it, and the corpus limitation that leaves the automation (T0037) signal
inert on this dataset.
