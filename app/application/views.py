from flask import Blueprint, render_template, request, redirect
import logging
from .models import db, Measure
from .search import (
    exact_search,
    loose_search,
    transform_query_data_to_list,
    get_related_metrics_and_measures,
)

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.DEBUG)

app = Blueprint("app", __name__)


@app.errorhandler(404)
def page_not_found(e):
    """Returns error template, if user enters wrong URL."""
    return render_template("404.html"), 404


@app.route("/", methods=["GET", "POST"])
def get_measures():
    """Gets list of all measures."""
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
    Gets list of rules for selected measures. The search algorithms works in the following way:
    1. gets selected measures & their values
    2. if checobox "exact search" is selected, exact search is performed - the algorithm searches for all rules, which contain all selected measures & measures contain selected values
    3. if checkbox is not selected, loose search is performed - the algorithm searches for all rules, which contain one of the selected measures & selected values
    4. support, confidence & lift are added for all rules
    5. for all rules are added all other related measures & their values
    6. query set data is transformed to a dictionary
    7. the dictionary is passed to the front-end
    """
    f = request.form
    selected_values = {}
    for key in f.keys():
        if key != "checkbox":
            for value in f.getlist(key):
                if value != "Choose one option":
                    selected_values[key] = value

    # checks if checkbox for exact search if checked
    if request.form.get("checkbox") == "1":
        rule_id = exact_search(selected_values)
    else:
        rule_id = loose_search(selected_values)

    rules_list = transform_query_data_to_list(rule_id)
    rules_dict = get_related_metrics_and_measures(rules_list)

    return render_template("results.html", rules_dict=rules_dict)
