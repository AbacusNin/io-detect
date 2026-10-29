# Roadmap

io-detect v1 is built and measured. The next work turns one measured run into a small evaluation suite. Three items, in the order I plan to tackle them.

## 1. Ablation

Run `io_detect ablate` to turn each graph signal off in turn and re-score. Done for the two
signals that build the graph. On Russia_2:

| Graph built from | Account pairs | Flagged | Precision | Recall |
|---|---|---|---|---|
| Both signals, as shipped | 11,309 | 447 | 0.5436 | 0.6731 |
| Duplicate text only | 11,146 | 443 | 0.5485 | 0.6731 |
| Co-repost timing only | 163 | 36 | 0.8056 | 0.0803 |

Duplicate text carries the result, and co-repost timing is precise and nearly blind. The
163 pairs it contributes sit against duplicate text's 11,146.

Still open: whether hashtag flooding, swarming and automation earn a place in the graph as
pairwise edges. Today they feed only the DISARM tags and triage roles. That leaves the
flagged set untouched, so there is nothing in them yet to ablate.

## 2. Baseline

Right now the headline numbers (precision about 0.54, recall about 0.67 on Russia_2) sit against chance only: flagging the same 447 accounts at random would score about 0.14 precision. This item adds at least one real comparison on the same data and the same split: a simple account-level classifier on the same features, or an existing published coordination-detection method. The output is the pipeline's numbers reported beside the baseline's.

## 3. Generalization

Measure on one campaign and test on another. The Indiana dataset covers 26 campaigns, not only Russia_2, so this needs no new source, though each campaign file is a separate gated download. The output is whether the result holds when the tool meets a campaign it was not tuned on. A drop here would be a real result worth reporting.

## Ceiling (unchanged)

All of this stays inside the same claim the tool already makes: measured detection on labeled data with documented controls. Not live-campaign detection. Not attribution.
