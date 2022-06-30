from .models import db, Measure, Rule, RuleMeasure
from sqlalchemy import select, desc


def exact_search(selected_values):
    """Returns rules, where there is exact search between selected measures & their values."""
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


def loose_search(selected_values):
    """Returns all rules, where there is at least one selected measure & it's value."""
    temp_rule_list = []
    for key, value in selected_values.items():
        one_rule_id = (
            db.session.query(RuleMeasure.rule_id)
            .join(Measure, RuleMeasure.measure_id == Measure.id)
            .join(Rule, RuleMeasure.rule_id == Rule.id)
            .filter(Measure.name == key, Measure.description == value)
            .order_by(desc(Rule.support))
            .all()
        )
        temp_rule_list.append(one_rule_id)
    rule_id = [elem for tup in temp_rule_list for elem in tup]
    return rule_id


def transform_query_data_to_list(rule_id):
    """Every rule returned by functions 'loose_search' and 'exact_search' is in the form of a tuple. It's necessary
    to transform it to list, so it'd could be afterwards transformed to dictionary."""
    rules_list = [v[0] for v in rule_id]
    return rules_list


def get_related_metrics_and_measures(rules_list):
    """Gets related metrics & measures and returns them to a dictionary, which is then passed tho the front-end."""
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
