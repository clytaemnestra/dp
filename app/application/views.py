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
    return redirect("/results")


@app.route("/results", methods=["GET", "POST"])
def get_results():
    f = request.form
    selected_values = {}
    for key in f.keys():
        for value in f.getlist(key):
            if value != "Choose one option":
                selected_values[key] = value
    # print(selected_values)
    measure_name = ""
    measure_description = ""
    for key, value in selected_values.items():
        measure_name = key
        measure_description = value
        print("mn", measure_name)
        print("md", measure_description)
    rule_id = db.session.query(RuleMeasure.rule_id)\
        .join(Measure, RuleMeasure.measure_id == Measure.id)\
        .filter(Measure.name == measure_name, Measure.description == measure_description).all()

    print("r_id", rule_id)

    rules_list = [v[0] for v in rule_id]
    print("rl", rules_list)
    # print("rl", rules_list)
    rules_dict = {}
    for r in rules_list:
        metrics = db.session.query(Rule.support, Rule.confidence, Rule.lift)\
            .join(RuleMeasure, Measure.id == RuleMeasure.measure_id)\
            .join(Measure, RuleMeasure.measure_id == Measure.id)\
            .filter(RuleMeasure.rule_id == r)\
            .distinct()\
            .all()
        rules_dict[r] = []
        for i in metrics:
            rules_dict[r].append(i)
            # print("i", i)

        measures = db.session.query(Measure.name, Measure.description)\
            .join(RuleMeasure, Measure.id == RuleMeasure.measure_id)\
            .filter(RuleMeasure.rule_id == r).all()
        # print("ms", measures)
        for j in measures:
            rules_dict[r].append(j)
            # print("j", j)

    print("rules dict", rules_dict)
    return render_template("results.html")

"""

>>> r3 = db.session.query(Measure.name, Measure.description).join(RuleMeasure, Measure.id==RuleMeasure.measure_id).filter(RuleMeasure.rule_id=="1").all()
INFO:sqlalchemy.engine.Engine:[generated in 0.00027s] ('1',)
>>> r3
[('Temperature Category', 'from 0 to 10'), ('Restrictions on Internal Movement', 'internal movement restrictions in place '), ('Public Information Campaigns', None), ('Cancel Public Events', 'recommend cancelling ')]

>>> r5 = db.session.query(Rule.support, Rule.confidence, Rule.lift).join(RuleMeasure, Measure.id==RuleMeasure.measure_id).join(Measure, RuleMeasure.measure_id==Measure.id).filter(RuleMeasure.rule_id=="1").distinct().all()
INFO:sqlalchemy.engine.Engine:SELECT DISTINCT rule.support AS rule_support, rule.confidence AS rule_confidence, rule.lift AS rule_lift 
FROM rule JOIN rule_measure ON measure.id = rule_measure.measure_id JOIN measure ON rule_measure.measure_id = measure.id 
WHERE rule_measure.rule_id = ?
INFO:sqlalchemy.engine.Engine:[generated in 0.00027s] ('1',)
>>> r5
[(0.04154302670623145, 0.4022988505747126, 0.046488625123639965)]

>>> r = db.session.query(Rule.id).join(RuleMeasure, Measure.id==RuleMeasure.measure_id).join(Measure, RuleMeasure.measure_id==Measure.id).filter(Measure.name=="Temperature Category", Measure.description=="from 0 to 10").all()
INFO:sqlalchemy.engine.Engine:SELECT rule.id AS rule_id 
FROM rule JOIN rule_measure ON measure.id = rule_measure.measure_id JOIN measure ON rule_measure.measure_id = measure.id 
WHERE measure.name = ? AND measure.description = ?
INFO:sqlalchemy.engine.Engine:[generated in 0.00025s] ('Temperature Category', 'from 0 to 10')
>>> r
[(1,)]


najdi vsechny pravidla Rule.id kde se objevuje jako Measure.description a Measure.value neco
r

pro vsechny pravidla vypis support, conf, lift 
r5

pro kazde pravidlo najdi vsechny Measure.name a Measure.description 
r3

"""