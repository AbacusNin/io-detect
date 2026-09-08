from io_detect.taxonomy.disarm import TECHNIQUES, requires_fields


def test_v1_technique_set():
    assert set(TECHNIQUES) == {"T0040", "T0044", "T0043", "T0041", "T0037"}


def test_repost_technique_needs_repost_fields():
    fields = requires_fields("T0040")
    assert "is_repost" in fields and "reposted_post_id" in fields
