from io_detect.taxonomy.tagging import tag


def test_tag_maps_signals_to_techniques():
    assert tag({"has_corepost": True, "has_automation": True}) == ["T0037", "T0040"]


def test_tag_empty_when_no_signals():
    assert tag({}) == []
