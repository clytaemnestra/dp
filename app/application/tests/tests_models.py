def test_new_rule(new_rule):
    assert new_rule.support == "0.50"
    assert new_rule.confidence == "0.25"
    assert new_rule.lift == "0.15"


def test_new_measure(new_measure):
    assert new_measure.name == "School closing"
    assert new_measure.value == "1"
    assert new_measure.description == "Closing of schools"


def test_new_rule_measure(new_rule_measure):
    assert new_rule_measure.rule_id == 1
    assert new_rule_measure.measure_id == 1
