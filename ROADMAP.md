# Roadmap

io-detect v1 is built and measured. The next work turns one measured run into a small evaluation suite. Three items, in the order I plan to tackle them. A formal research paper is deliberately not on this list; see the note at the end.

## 1. Ablation

Turn each behavioral signal off one at a time (repost synchrony, content duplication, hashtag flooding, swarming, automation) and re-score against the controls. The pipeline already computes every signal, so this is mostly a matter of toggling them and rerunning the metrics. The output is a table of precision and recall with each signal removed, which shows which signals actually carry the result. This goes first because it is nearly free and tells the most.

## 2. Baseline

Right now the headline numbers (precision about 0.54, recall about 0.67 on Russia_2) sit against nothing. This item adds at least one comparison on the same data and the same split: a simple account-level classifier on the same features, or an existing published coordination-detection method. The output is the pipeline's numbers reported beside the baseline's.

## 3. Generalization

Measure on one campaign and test on another. The Indiana dataset covers 26 campaigns, not only Russia_2, so this needs no new source, though each campaign file is a separate gated download. The output is whether the result holds when the tool meets a campaign it was not tuned on. A drop would be a real finding and would be reported as one.

## Not in scope

A formal research paper. The three items above are worth doing as improvements to this tool on their own. If a paper is ever written it would come from their results, but it is not a goal of this repository.

## Ceiling (unchanged)

All of this stays inside the same claim the tool already makes: measured detection on labeled data with documented controls. Not live-campaign detection, and not attribution.
