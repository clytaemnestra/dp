from flask import Blueprint, render_template
import logging

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.DEBUG)

app = Blueprint("app", __name__)


@app.errorhandler(404)
def page_not_found(e):
    """Returns error template, if user enters wrong URL."""
    return render_template("404.html"), 404
