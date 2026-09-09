# io-detect

Detection-as-code for coordinated inauthentic behavior. It runs on labeled
influence-operation data with documented organic controls and reports
precision and recall against that ground truth.

## Measured results

Scored on the Indiana University "Russia_2" campaign file against the
`is_control` labels that ship with it, at account granularity: precision 0.5436,
recall 0.6731 (243 true positives, 204 false positives, 118 false
negatives, 361 IO-labeled accounts). See `docs/writeup.md` for the full run
output, how the control set is built, and what the number does and
doesn't mean.

Precision 0.54 is a lab-sample number. It is not a guarantee for anything
running against live traffic. Russia_2 is enriched to 91% IO rows by
construction, and precision degrades fast as the real-world base rate of IO
drops toward its natural, much lower level. Treat this as an upper bound on
a curated dataset: it does not predict what a live feed would produce.

## Ingest

Two source datasets ingest into one canonical schema: the Indiana University
release (`load_iu`, `load_iu_parquet`) and the Clemson/Linvill-Warren IRA
tweet release (`load_clemson`). Every detection and scoring module reads
that canonical schema, not either source format directly. See
`docs/schema/crosswalk.md` for the field-by-field mapping and the gaps each
source leaves (Clemson has no control class and no repost linkage, IU's
`application_name` is anonymized on this release).

## What this is not

It does not detect live campaigns in the wild, and it does not attribute
operations to actors. The signals it flags (co-repost timing, duplicate
content, hashtag floods, mention swarming) measure coordination. They say
nothing about authenticity or viewpoint, and a flagged account still needs
a human in the loop before anyone acts on it.
