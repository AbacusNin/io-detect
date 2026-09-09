# Roadmap

io-detect v1 is built and measured. The next work turns one measured run into a small evaluation suite. Three items, in the order I plan to tackle them.

## 1. Ablation

Turn each behavioral signal off one at a time (repost synchrony, content duplication, hashtag flooding, swarming, automation) and re-score against the controls. The pipeline already computes every signal, so this is mostly a matter of toggling flags and rerunning the metrics, which makes it the cheapest item on this list. The output is a table of precision and recall with each signal removed, showing which signals actually carry the result.

## 2. Baseline

Right now the headline numbers (precision about 0.54, recall about 0.67 on Russia_2) sit against nothing. This item adds at least one comparison on the same data and the same split: a simple account-level classifier on the same features, or an existing published coordination-detection method. The output is the pipeline's numbers reported beside the baseline's.

## 3. Generalization

Measure on one campaign and test on another. The Indiana dataset covers 26 campaigns, not only Russia_2, so this needs no new source, though each campaign file is a separate gated download. The output is whether the result holds when the tool meets a campaign it was not tuned on. A drop here would be a real result worth reporting.

## Ceiling (unchanged)

All of this stays inside the same claim the tool already makes: measured detection on labeled data with documented controls. Not live-campaign detection. Not attribution.
