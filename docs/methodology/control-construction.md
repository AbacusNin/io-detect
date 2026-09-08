# Control construction

The negative class for every reported precision and recall number is the
Indiana corpus's own `is_control` field, not a synthetic or self-generated
baseline. Zenodo record 10.5281/zenodo.14141549 ships each campaign file with
organic control posts alongside the labeled influence-operation posts, drawn
from accounts discussing the same topics in the same windows as the campaign.
That is what makes an honest precision and recall claim possible here at all;
without a native control class the detector would have nothing to be wrong
about.

## Scoring granularity

The pipeline flags accounts, not individual posts, so scoring happens at the
account level. `account_labels()` in `src/io_detect/eval/metrics.py` takes a
majority vote over each account's own posts: an account is labeled IO if 50%
or more of its posts are `is_control = False`, and control otherwise. `score()`
then compares the pipeline's flagged-account set against that label dict and
reports precision, recall, tp, fp, fn, and n_positive.

For Russia_2 this yields 361 IO-labeled accounts and 2,175 control-labeled
accounts out of 2,536 unique accounts in the file, against 920,761 IO rows
and 90,291 control rows at the post level (1,011,052 rows total).

## Honesty caveats

These carry into every number in `results/Russia_2-metrics.json` and any
future campaign file scored the same way:

- **Lab metrics are an upper bound.** This is scored on a fixed, curated,
  labeled historical dataset with a native control class. Field performance
  on live, unlabeled traffic will be lower; there is no control class in the
  wild to check against, and no guarantee that new campaigns share this
  corpus's coordination patterns.
- **Real IO is rare, so precision degrades at low base rates.** Russia_2 is
  91% IO rows by construction (an intentionally enriched sample). Any
  real-world stream will run far closer to natural IO prevalence, and at a
  lower base rate the same false-positive rate produces much worse precision.
  Do not read this run's precision as a forecast for a live feed.
- **Authentic-but-partisan accounts can be swept in.** The detection signals
  here (co-repost timing, duplicate content, hashtag floods, mention
  swarming) are coordination signals, not authenticity or viewpoint signals.
  A tightly organized but genuine political community can trip the same
  thresholds as a coordinated inauthentic one. Flags from this pipeline are
  not attribution and are not proof of inauthenticity; they need a human in
  the loop before any action is taken on a flagged account.

## application_name is anonymized on this corpus

`application_name` in the parquet release is hashed, not a readable client
string ("web", "bot", "TweetDeck", and so on). Russia_2 has 304 distinct
hash values and none of them match the literal automation markers
(`bot`, `api`, `scheduler`) that `automation_scores()` looks for. The result
is that `automated_share` is 0.0 for every account in this file, T0037
(Create Cyborg or Bot Accounts) never fires, and the automation column in
per-account triage carries no signal on this corpus. This is a limitation of
the anonymized field, not evidence that no automated posting occurred in the
underlying campaign. It is reported here plainly rather than papered over;
no automation results are fabricated to fill the gap.
