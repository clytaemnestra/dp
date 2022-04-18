from flask import Blueprint, render_template, request, redirect
import logging
from .models import db, Measure
from sqlalchemy import engine
import pandas as pd
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
        measures = db.session.query(Measure.name, Measure.value).all()
        measures_list = []
        for measure_name in measures:
            if measure_name[0] not in measures_list:
                measures_list.append(measure_name[0])
        for measure_name in measures_list:
            for measure in measures:
                if measure[0] == measure_name:
                    measures_dict[measure[0]] = []
        for measure_name in measures_dict:
            for measure_value in measures:
                if measure_name == measure_value[0]:
                    measures_dict[measure_name].append(measure_value[1])
    return render_template("index.html", measures_dict=measures_dict)
