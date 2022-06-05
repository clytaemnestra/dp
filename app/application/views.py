from flask import Blueprint, render_template, request, redirect
import logging
from .models import db, Measure
from .search import exact_search, loose_search, transform_query_data_to_dict

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
    """
    Gets list of all measures. The search algorithm works in the following way:
    1.
    2.
    3.
    4.
    5.
     """
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
    """Gets list of rules for given measures."""
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

    # rule_id = exact_search(selected_values)
    rule_id = loose_search(measure_name, measure_description)
    rules_dict = transform_query_data_to_dict(rule_id)

    return render_template("results.html", rules_dict=rules_dict)
