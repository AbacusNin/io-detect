# io-detect

Detection-as-code for coordinated inauthentic behavior, measured against labeled influence-operation data.

## Data

| | |
|---|---|
| Corpus | Indiana University, "Labeled Datasets for Research on Information Operations" |
| DOI | 10.5281/zenodo.14141549 |
| License | CC-BY-NC-ND-4.0 |
| Access | Restricted. Login and academic affiliation required, one file per researcher per day. |
| Campaign scored | Russia_2, 21 gzip-parquet parts |
| Archive | 14189072.zip, 150,597,200 bytes |
| Archive sha256 | 0ce1ce1e197b63faa4cdc158215f31eb1323e0287359e785e104420a1a65628c |

No data is committed to this repository. Fetch the campaign file, place it under `data/raw/`, and verify the sha256 above with `io_detect.ingest.integrity` before use.

A second corpus, the FiveThirtyEight release of the Clemson/Linvill-Warren IRA tweets, ingests through the same canonical schema. It is positives-only and carries no control class, so nothing is scored on it.

## Method

1. Normalize the source into one canonical record schema.
2. Compute behavioral signals per account and per account pair: co-repost timing, duplicate text, hashtag flooding, mention and reply swarming, automation.
3. Build a weighted co-activity network from those signals.
4. Extract dense clusters from that network. A coordinated group knots together into a small, heavily weighted cluster that stands out from the sparse web ordinary accounts sit in.
5. Sort each flagged cluster into a likely-automated core and the accounts that amplify.
6. Tag behaviors with DISARM techniques and score the flagged set against the corpus labels.

DISARM tags are output. Nothing in `features/`, `detect/`, or `eval/` reads a tag or a label to decide what to flag.

## Results

Russia_2, scored at account granularity.

| Metric | Value |
|---|---|
| Precision | 0.5436 |
| Recall | 0.6731 |
| True positives | 243 |
| False positives | 204 |
| False negatives | 118 |
| IO-labeled accounts | 361 |
| Accounts flagged | 447 |
| Clusters detected | 22 |

Corpus: 1,011,052 posts across 21 parts. 920,761 IO rows, 90,291 control rows. 2,536 unique accounts, of which 361 are IO-labeled and 2,175 control-labeled. Load 0.29s, pipeline 4.04s.

Cluster sizes: 147, 64, 54, 43, 16, 16, 14, 10, 9, 9, 9, 8, 8, 7, 6, 5, 4, 4, 4, 4, 3, 3.

Per-account identifiers and cluster memberships are not published here. The corpus license is no-derivatives.

## Scoring and controls

The negative class is the corpus's own `is_control` field: Indiana ships organic control posts beside the campaign posts, drawn from accounts discussing the same topics in the same windows. Without a native control class there is nothing for the detector to be wrong about, so there is no honest precision figure to report.

The pipeline flags accounts, so scoring happens at account level. `account_labels()` takes a majority vote over each account's posts: an account is IO if at least half its posts carry `is_control = False`. `score()` compares the flagged set against those labels.

## Limits

Lab metrics like these are an upper bound: this is a fixed, curated, labeled historical corpus with a native control class, and live traffic has none of that structure.

Russia_2 is built to be 91% IO rows, far above what any real feed looks like, and precision degrades as the base rate drops toward natural, much lower levels of IO. The same false-positive rate produces much worse precision at that lower rate. The 0.54 above describes this corpus. It does not predict what a live feed would produce.

Co-repost timing, duplicate content, hashtag floods and mention swarms are signals of coordination. They say nothing about authenticity, and a tightly organized genuine community can trip the same thresholds as a paid one. A flag from this pipeline is not attribution, and it is not proof that an account is fake. Someone still has to look at it before anyone acts on the result.

`application_name` in the parquet release is hashed rather than a readable client string, which kills the automation signal on this corpus. Russia_2 carries 304 distinct hash values, none matching the literal markers `automation_scores()` looks for, so `automated_share` comes back 0.0 for every account, T0037 never fires, and triage gets no automation signal here. The zero is an artifact of the anonymized field, not evidence about the campaign: it says nothing about whether Russia_2 actually used automation, and no automation results were invented to fill the gap.

## Schema notes

The second source forced three decisions.

The two sources don't share a control class. Indiana has one; Clemson is positives-only. A bare boolean would have hidden that difference. `label` plus `label_scheme` records where the class came from, and `is_control` survives as a projection of `label == "control"`, so the scoring code did not change. A third source writes its own `label_scheme` rather than overloading an existing one.

Repost linkage and entity fields do not survive Clemson. Indiana gives `reposted_postid` and `reposted_accountid` per retweet. Clemson's `retweet` column is a bare flag with no pointer back to the original, so those fields stay null. Clemson also embeds hashtags and mentions in the tweet text rather than shipping them as fields, so both come back empty instead of guessed at, and a detector reading those fields sees a real absence, not a fabricated value.

`actor_role` is annotation. `account_category` is Linvill and Warren's analyst-coded persona label (RightTroll, NewsFeed, and so on). It exists only on Clemson rows, and nothing in the detection path reads it. Building on it would make results source-dependent.

Field-by-field mapping: `docs/schema/crosswalk.md`.

## Build

Python. polars for data, networkx for graphs. Test-first, 30 tests. Apache 2.0. `make demo` runs the full pipeline on a small synthetic fixture, so the tool is runnable without the gated corpus.
