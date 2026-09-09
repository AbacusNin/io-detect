# Canonical schema crosswalk

Where each canonical field comes from in the two source adapters. IU is
`load_iu` / `load_iu_parquet` (Zenodo 10.5281/zenodo.14141549). Clemson is
`load_clemson` (the FiveThirtyEight release of the Clemson/Linvill-Warren IRA
tweet corpus).

| Canonical field | IU source | Clemson source |
|---|---|---|
| `post_id` | `postid` | `tweet_id` (cast to str) |
| `account_id` | `accountid` | `author` (the handle) |
| `timestamp` | `post_time` | `publish_date`, parsed `%m/%d/%Y %H:%M` |
| `text` | `post_text` | `content` |
| `language` | `post_language` | `language` |
| `in_reply_to_post_id` | `in_reply_to_postid` | (none) |
| `in_reply_to_account_id` | `in_reply_to_accountid` | (none) |
| `is_repost` | `is_repost` | `retweet == 1` |
| `reposted_account_id` | `reposted_accountid` | (none) |
| `reposted_post_id` | `reposted_postid` | (none) |
| `hashtags` | `hashtags`, comma-split (CSV) or native list (parquet) | (none, empty list) |
| `urls` | `urls`, comma-split (CSV) or native list (parquet) | built from `tco1_step1`, `tco2_step1`, `tco3_step1` |
| `mentions` | `account_mentions` | (none, empty list) |
| `application` | `application_name` | (none) |
| `account_created` | `account_creation_date` | (none) |
| `followers` | `follower_count` | `followers` |
| `following` | `following_count` | `following` |
| `is_control` | native `is_control` | always `false` |
| `label` | `"control"` if `is_control` else `"io"` | always `"io"` |
| `label_scheme` | `"iu_2411.10609"` | `"clemson_ira_positives"` |
| `actor_role` | (none) | `account_category` |
| `actor_role_scheme` | (none) | `"clemson_linvill_warren"` |
| `account_region` | (none) | `region` |
| `source` | `"iu_2411.10609"` | `"clemson_538_ira"` |

## Lessons folded into the schema

**Control is not a universal concept.** IU ships organic control posts
alongside its IO posts, drawn from real accounts talking about the same
topics in the same windows. Clemson does not; it is a positives-only release,
every row in it is IRA. Trying to force both sources into a single boolean
without saying where the boolean came from would have hidden that difference.
`label` plus `label_scheme` makes the provenance explicit, and `is_control`
stays as a projection of `label == "control"` so the existing metrics code in
`eval/metrics.py` did not need to change. Any adapter that adds a third
source with its own definition of "control" writes its own `label_scheme`
value rather than overloading the ones already in use.

**Repost linkage and hashtags/mentions do not survive the trip from
Clemson.** IU gives structured `reposted_accountid` / `reposted_postid` for
each retweet; Clemson's `retweet` column is a bare flag with no pointer back
to the original post or account, so `reposted_post_id` and
`reposted_account_id` stay null for every Clemson row. Clemson also embeds
hashtags and mentions inside the raw tweet text instead of shipping them as
separate fields, so `hashtags` and `mentions` come back empty rather than
guessed at by parsing text here. A detector reading those fields on a
Clemson-sourced frame gets an honest absence, not a silent zero standing in
for real data.

**`actor_role` is annotation, not a detection input.** `account_category`
is Linvill and Warren's own analyst-coded label for what kind of persona an
account was running (RightTroll, NewsFeed, and so on). It is useful for
downstream analysis and reporting, but nothing in `features/`, `detect/`, or
`eval/metrics.py` reads it, and it should not start being read there: the
whole point of the detection pipeline is to find coordination and automation
signals without needing a prior label, and `actor_role` only exists on
Clemson-sourced rows in the first place, so building a detector around it
would make results source-dependent in exactly the way `is_control` already
had to work around.
