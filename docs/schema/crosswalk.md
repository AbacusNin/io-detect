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
