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

Scoring runs per account. The account-level base rate is 14.2%, with 361 of
the file's 2,536 accounts IO-labeled. Flagging 447 accounts at random would
score about 0.14 precision and 0.18 recall, so 0.54 is roughly 3.8 times
chance.

### Which signal carries it

`io_detect ablate` turns each graph signal off in turn and re-scores. On Russia_2:

| Graph built from | Account pairs | Flagged | Precision | Recall |
|---|---|---|---|---|
| Both signals, as shipped | 11,309 | 447 | 0.5436 | 0.6731 |
| Duplicate text only | 11,146 | 443 | 0.5485 | 0.6731 |
| Co-repost timing only | 163 | 36 | 0.8056 | 0.0803 |

Duplicate text carries the result. Dropping co-repost timing leaves recall
identical and nudges precision up. Co-repost timing alone is precise and
nearly blind, and it contributes 163 account pairs against duplicate text's
11,146. Read 0.5436 as a duplicate-text number.

Precision 0.54 is still a lab-sample number. Russia_2 is curated: 91% of its
posts are IO, and no live feed holds anything like 14% IO accounts. Precision
degrades as that base rate drops toward its natural, much lower level. Treat
0.54 as an upper bound on a curated dataset. It does not predict what a live
feed would produce.

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
operations to actors. Two signals decide which accounts get flagged:
co-repost timing and duplicate content. The hashtag-flood and mention-swarm
checks only feed the DISARM tags, which describe the whole file and point at
no particular account. All of these measure coordination. They say nothing
about authenticity or viewpoint, and a flagged account still needs a human
in the loop before anyone acts on it.
