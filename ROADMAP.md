# Roadmap

io-detect v1 is built and measured. The next work turns one measured run into a small evaluation suite. Three items, in the order I plan to tackle them.

## 1. Ablation

Two signals build the graph that decides what gets flagged: repost synchrony and content duplication. Turn each off in turn and re-score against the controls. Hashtag flooding, swarming and automation only feed the DISARM tags and triage, so removing them cannot move precision or recall as the pipeline stands. The second half of this item tests whether those three earn a place in the graph as pairwise edges. The pipeline already computes every signal, which makes this the cheapest item on the list. The output is a table of precision and recall for each variant, showing which signals actually carry the result.

## 2. Baseline

Right now the headline numbers (precision about 0.54, recall about 0.67 on Russia_2) sit against chance only: flagging the same 447 accounts at random would score about 0.14 precision. This item adds at least one real comparison on the same data and the same split: a simple account-level classifier on the same features, or an existing published coordination-detection method. The output is the pipeline's numbers reported beside the baseline's.

## 3. Generalization

Measure on one campaign and test on another. The Indiana dataset covers 26 campaigns, not only Russia_2, so this needs no new source, though each campaign file is a separate gated download. The output is whether the result holds when the tool meets a campaign it was not tuned on. A drop here would be a real result worth reporting.

## Ceiling (unchanged)

All of this stays inside the same claim the tool already makes: measured detection on labeled data with documented controls. Not live-campaign detection. Not attribution.
