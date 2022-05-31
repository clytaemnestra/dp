from flask import Blueprint, render_template, request, redirect
import logging
from .models import db, Measure, Rule, RuleMeasure

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

app = Blueprint("app", __name__)


@app.errorhandler(404)
def page_not_found(e):
    """Returns error template, if user enters wrong URL."""
    return render_template("404.html"), 404


@app.route("/", methods=["GET", "POST"])
def get_measures():
    """Gets list of all measures"""
    measures_dict = {}
    if request.method == "GET":
        measures = db.session.query(Measure.name, Measure.description).all()
        measures_list = []
        for measure_name in measures:
            # don't add duplicate measure name
            if measure_name[0] not in measures_list:
                measures_list.append(measure_name[0])
        for measure_name in measures_list:
            for measure in measures:
                if measure[0] == measure_name:
                    measures_dict[measure[0]] = []
        # add measure value
        for measure_name in measures_dict:
            for measure_value in measures:
                if measure_name == measure_value[0]:
                    measures_dict[measure_name].append(measure_value[1])
        return render_template("index.html", measures_dict=measures_dict)
    return redirect("/results")


@app.route("/results", methods=["GET", "POST"])
def get_results():
    """
    The main algorithm, which filters through rules and measures. It works in the following way:
    1. takes all selected measures & values from form on the FE,
    2. finds corresponding rules which contain selected measures & values,
    3. for all rules returns confidence, support & lift,
    4. for all rules finds all other corresponding measures & values.
    """
    f = request.form
    selected_values = {}
    for key in f.keys():
        for value in f.getlist(key):
            if value != "Choose one option":
                selected_values[key] = value
    measure_name = ""
    measure_description = ""
    for key, value in selected_values.items():
        measure_name = key
        measure_description = value
    # finds all corresponding rules
    rule_id = (
        db.session.query(RuleMeasure.rule_id)
        .join(Measure, RuleMeasure.measure_id == Measure.id)
        .filter(
            Measure.name == measure_name, Measure.description == measure_description
        )
        .all()
    )

    # converts tuples to list
    rules_list = [v[0] for v in rule_id]
    rules_dict = {}
    # finds support, confidence & lift for given rules
    for r in rules_list:
        metrics = (
            db.session.query(Rule.support, Rule.confidence, Rule.lift)
            .join(RuleMeasure, Measure.id == RuleMeasure.measure_id)
            .join(Measure, RuleMeasure.measure_id == Measure.id)
            .filter(RuleMeasure.rule_id == r)
            .distinct()
            .all()
        )
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
    return render_template("results.html", rules_dict=rules_dict)
