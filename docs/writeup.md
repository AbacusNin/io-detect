# io-detect

Detection-as-code for coordinated inauthentic behavior, measured against labeled influence-operation data.

## Data

| | |
|---|---|
| Dataset | Indiana University, "Labeled Datasets for Research on Information Operations" |
| DOI | 10.5281/zenodo.14141549 |
| License | CC-BY-NC-ND-4.0 |
| Access | Restricted. Login and academic affiliation required, one file per researcher per day. |
| Campaign scored | Russia_2, 21 gzip-parquet parts |
| Archive | 14189072.zip, 150,597,200 bytes |
| Archive sha256 | 0ce1ce1e197b63faa4cdc158215f31eb1323e0287359e785e104420a1a65628c |

I commit no data to this repository. Fetch the campaign file yourself, place it under `data/raw/`, and verify the sha256 above with `io_detect.ingest.integrity` before use.

A second dataset ingests through the same canonical schema, the FiveThirtyEight release of the Clemson/Linvill-Warren IRA tweets. It is positives-only, with no control class. I score nothing on it.

## Method

1. Normalize the source into one canonical record schema.
2. Compute behavioral signals. Co-repost timing and duplicate text are scored per account pair, automation per account, and hashtag flooding and mention or reply swarming across the whole file.
3. Build a weighted co-activity network from the two pairwise signals, co-repost timing and duplicate text. Those two are the only signals that decide which accounts get flagged.
4. Extract dense clusters from that network. A coordinated group knots together into a small, heavily weighted cluster. Ordinary accounts sit in a sparse web, and the extraction keys on that difference.
5. Sort each flagged cluster into a likely-automated core and the accounts that amplify it, using each account's automation share.
6. Record which DISARM techniques show up anywhere in the file.
7. Score the flagged set against the published labels.

The pipeline outputs DISARM tags and never reads them back. No tag or label reaches `features/`, `detect/`, or `eval/` to decide what gets flagged.

The tags describe the file as a whole. Each one fires when its signal turns up anywhere in the data, even once. Two accounts sharing one hashtag in the same five-minute window are enough to fire T0043. So a tag says that a behavior exists somewhere in the file. It does not tie that behavior to a cluster or an account. On Russia_2, the 2,175 control accounts on their own produce exactly the same four tags as the full file.

## Results

I scored Russia_2 at account granularity.

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
| Precision at chance (447 random flags) | 0.1424 |

The file holds 1,011,052 posts across 21 parts, 920,761 of them IO rows and 90,291 control rows. Those span 2,536 unique accounts: 361 IO-labeled, 2,175 control-labeled. Loading took 0.29s and the full pipeline 4.04s.

Cluster sizes: 147, 64, 54, 43, 16, 16, 14, 10, 9, 9, 9, 8, 8, 7, 6, 5, 4, 4, 4, 4, 3, 3.

To see which signal produces that number, `io_detect ablate` turns each graph signal off in turn and re-scores:

| Graph built from | Account pairs | Flagged | Precision | Recall |
|---|---|---|---|---|
| Both signals, as shipped | 11,309 | 447 | 0.5436 | 0.6731 |
| Duplicate text only | 11,146 | 443 | 0.5485 | 0.6731 |
| Co-repost timing only | 163 | 36 | 0.8056 | 0.0803 |

Duplicate text carries the result. Dropping co-repost timing leaves recall identical and nudges precision up. Co-repost timing on its own is precise and nearly blind, with 163 account pairs against duplicate text's 11,146. I read 0.5436 as a duplicate-text number.

I publish no per-account identifiers or cluster memberships here. The license is no-derivatives.

## Scoring and controls

The negative class comes from the `is_control` field that ships with the data. Indiana includes organic control posts beside the campaign posts. Those come from accounts discussing the same topics in the same windows. Without a native control class the detector has nothing to be wrong about, so no honest precision figure exists.

The pipeline flags accounts, so I score at account level. `account_labels()` takes a majority vote over each account's posts. An account counts as IO when at least half its posts carry `is_control = False`. `score()` then compares the flagged set against those labels.

## Limits

Lab metrics like these set an upper bound. This dataset is curated and labeled, with a native control class built in. Live traffic has none of that structure.

Indiana built Russia_2 at 91% IO rows. I score accounts, though, and the account-level base rate is lower: 361 of 2,536 accounts, or 14.2%. Read precision against that rate. Flagging 447 accounts at random would score about 0.14 precision and 0.18 recall, so 0.54 is roughly 3.8 times chance. No real feed carries 14% IO accounts either. Precision degrades as the base rate drops toward natural, much lower levels of IO, because the same false-positive rate produces much worse precision at that lower rate. The 0.54 above describes Russia_2. It does not predict what a live feed would produce.

Co-repost timing, duplicate content, hashtag floods and mention swarms signal coordination. They say nothing about authenticity. A tightly organized genuine community trips the same thresholds a paid one does, so a flag from this pipeline is not attribution. Neither is it proof that an account is fake. Someone still has to look at it before anyone acts on the result.

The parquet release hashes `application_name` instead of shipping a readable client string. That kills the automation signal on this data. Russia_2 carries 304 distinct hash values, and none match the literal markers `automation_scores()` looks for. `automated_share` comes back 0.0 for every account, T0037 never fires, and triage gets no automation signal here. That zero came out of the anonymized field. It says nothing about whether Russia_2 actually used automation, and I did not invent automation results to fill the gap.

## Schema notes

The second source forced three decisions.

The two sources don't share a control class. Indiana has one; Clemson is positives-only. A bare boolean would have hidden that difference. `label` plus `label_scheme` records where the class came from. `is_control` survives as a projection of `label == "control"`, so the scoring code did not change. A third source writes its own `label_scheme`.

Repost linkage and entity fields do not survive Clemson. Indiana gives `reposted_postid` and `reposted_accountid` per retweet. Clemson's `retweet` column is a bare flag with no pointer back to the original, so those fields stay null. Clemson also embeds hashtags and mentions in the tweet text instead of shipping them as fields. Both come back empty. A detector reading those fields sees a real absence.

`actor_role` only annotates. `account_category` holds Linvill and Warren's analyst-coded persona label (RightTroll, NewsFeed, and so on). It exists only on Clemson rows. Nothing in the detection path reads it, because building on it would make my results source-dependent.

Field-by-field mapping: `docs/schema/crosswalk.md`.

## Build

I wrote the tool in Python. polars handles the data work and networkx builds the graph. I developed it test-first, so it ships with 30 tests. I license it under Apache 2.0. `make demo` runs the full pipeline on a small synthetic fixture, so the tool runs without the gated dataset.
