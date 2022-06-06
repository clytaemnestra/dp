from .models import db, Measure, Rule, RuleMeasure
from sqlalchemy import select


def exact_search(selected_values):
    """Returnes rules, where """
    statement = select(Rule.id)
    for key, value in selected_values.items():
        statement = statement.where(
            select(RuleMeasure.id)
            .join(Measure)
            .where(RuleMeasure.rule_id == Rule.id)
            .where(Measure.name == key)
            .where(Measure.description == value)
            .exists()
        )

    rule_id = db.session.execute(statement).all()
    return rule_id


def loose_search(measure_name, measure_description):
    rule_id = (
        db.session.query(RuleMeasure.rule_id)
        .join(Measure, RuleMeasure.measure_id == Measure.id)
        .filter(
            Measure.name == measure_name, Measure.description == measure_description
        )
        .all()
    )
    return rule_id


def transform_query_data_to_dict(rule_id):
    """Every rule returned by functions 'loose_search' and 'exact_search' is in the form of a tuple. It's necessary
    to transform it to dictionary, so it could be used by front-end."""
    # converts tuples to list
    rules_list = [v[0] for v in rule_id]
    rules_dict = {}
    metrics_list = []

    # finds support, confidence & lift for given rules
    for r in rules_list:
        metrics = (
            db.session.query(Rule.support, Rule.confidence, Rule.lift)
            .join(RuleMeasure, Measure.id == RuleMeasure.measure_id)
            .join(Measure, RuleMeasure.measure_id == Measure.id)
            .filter(Rule.id == r)
            .distinct()
            .all()
        )
        metrics_list.append(metrics)

        # adds metrics as value for rule id
        rules_dict[r] = []
        for i in metrics:
            rules_dict[r].append(i)

        # finds all other measures which are connected with the given rule id
        measures = (
            db.session.query(Measure.name, Measure.description)
            .join(RuleMeasure, Measure.id == RuleMeasure.measure_id)
            .filter(RuleMeasure.rule_id == r)
            .all()
        )
        # adds measures to the final dict
        for j in measures:
            rules_dict[r].append(j)
    return rules_dict
