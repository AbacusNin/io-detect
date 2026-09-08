from dataclasses import dataclass


@dataclass(frozen=True)
class Technique:
    id: str
    name: str
    observables: list[str]
    feature: str
    detection: str


TECHNIQUES: dict[str, Technique] = {
    "T0040": Technique(
        "T0040",
        "Bots Amplify via Automated Forwarding and Reposting",
        ["is_repost", "reposted_post_id", "reposted_account_id", "timestamp", "application"],
        "repost synchrony and automated-client share",
        "coordinated reposting clusters",
    ),
    "T0044": Technique(
        "T0044",
        "Flood Information Space",
        ["text", "timestamp", "account_id"],
        "content duplication rate and cadence",
        "mass-duplicate flooding bursts",
    ),
    "T0043": Technique(
        "T0043",
        "Flood Existing Hashtag",
        ["hashtags", "timestamp", "account_id"],
        "hashtag volume spike and concentration",
        "coordinated hashtag flooding",
    ),
    "T0041": Technique(
        "T0041",
        "Conduct Swarming",
        ["mentions", "in_reply_to_account_id", "timestamp"],
        "mention and reply convergence on a target",
        "swarming bursts",
    ),
    "T0037": Technique(
        "T0037",
        "Create Cyborg or Bot Accounts",
        ["application", "account_created", "timestamp"],
        "automation likelihood and creation-date clustering",
        "per-account automation triage",
    ),
}


def requires_fields(technique_id: str) -> list[str]:
    return TECHNIQUES[technique_id].observables
