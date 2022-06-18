import pytest
from application import create_app
from ..models import Rule, Measure, RuleMeasure


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def new_rule():
    rule = Rule(support="0.50", confidence="0.25", lift="0.15")
    return rule


@pytest.fixture(scope="module")
def new_measure():
    measure = Measure(
        name="School closing", value="1", description="Closing of schools"
    )
    return measure


@pytest.fixture(scope="module")
def new_rule_measure():
    rule_measure = RuleMeasure(rule_id=1, measure_id=1)
    return rule_measure
