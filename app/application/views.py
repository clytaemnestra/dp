from flask import Blueprint, render_template, request, redirect
import logging
from .models import db, Measure

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
    """Gets list of all measures"""
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        return redirect("/results"), 303