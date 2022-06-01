from flask import Blueprint, render_template, request, redirect
import logging
from .models import db, Measure, Rule, RuleMeasure
import ast

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

@app.route("/load", methods=["GET", "POST"])
def load():
    file = open("/home/mia/Documents/repos/skola/dp/app/application/database/formatted_rules2", "r")
    # print('aja')
    contents = file.readlines()
    temp_categories = []
    h1 = []

    c7 = []
    c3 = []
    c8 = []
    c5 = []
    c6 = []
    c1 = []
    c2 = []
    c4 = []
    for index, item in enumerate(contents):
        rule_dict = ast.literal_eval(item)
        for key in rule_dict.keys():
            # print(key)
            try:
                temp_categories.append(rule_dict['tempCategories'])
                h1.append(rule_dict['H1_Public information campaigns_general'])
                c7.append(rule_dict['C7_Restrictions on internal movement_general'])
                c3.append(rule_dict['C3_Cancel public events_general'])
                c8.append(rule_dict['C8_International travel controls'])
                c5.append(rule_dict['C5_Close public transport_general'])
                c6.append(rule_dict['C6_Stay at home requirements_general'])
                c1.append(rule_dict['C1_School closing_general'])
                c2.append(rule_dict['C2_Workplace closing_general'])
                c4.append(rule_dict['C4_Restrictions on gatherings_general'])
            except KeyError:
                continue
    # print('set is', index, set(h1))
    # exit()
    # print(h1)
    h1_set = list(set(h1))
    for i in h1_set:
        print("i", i)
        new_measure = Measure(name='H1_Public information campaigns_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    c7_set = list(set(c7))
    for i in c7_set:
        new_measure = Measure(name='C7_Restrictions on internal movement_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c3):
        new_measure = Measure(name='C3_Cancel public events_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c8):
        new_measure = Measure(name='C8_International travel controls', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c5):
        new_measure = Measure(name='C5_Close public transport_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c6):
        new_measure = Measure(name='C6_Stay at home requirements_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c1):
        new_measure = Measure(name='C1_School closing_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c2):
        new_measure = Measure(name='C2_Workplace closing_general', value=i)
        db.session.add(new_measure)
        db.session.commit()
    for i in set(c4):
        new_measure = Measure(name='C4_Restrictions on gatherings_general', value=i)
        db.session.add(new_measure)
        db.session.commit()

    #print(set(temp_categories))
    #print(set(h1))
        #values_list.append()
            # new_measure = Measure(name=)


    #     # print(rule_dict.keys())
    #     # print(rule_dict.values())
    #     # rules_list.append(eval(item))
    #     # support = rules_list['support']
    #
    #     for key in rule_dict.keys():
    #         # break
    #
    #         keys_to_db = (rule_dict[key],)
    #         print(keys_to_db)
    #         if key not in ['support', 'confidence', 'uplift']:
    #             print(key)
    #             print(rule_dict[key])
    #             # is_already_in_db = db.session.query(Measure.)
    #             # new_measure = Measure(name=key, value=rule_dict[key])
    #             # db.session.add(new_measure)
    #             # db.session.commit()
    #             # measure = (db.session.query(Measure.id).filter(Measure.name==key, Measure.value==int(rule_dict[key])).all())
    #             # print(measure)
    #             # new_rule_measure = RuleMeasure(rule_id=index + 1, measure_id=measure)
    #             # db.session.add(new_rule_measure)
    #             # db.session.commit()
    #
    #
    #
    #
    #     break


    # for index, rule in enumerate(rules_list):
        # try:
        # support = [desired_dict["support"] for desired_dict in rule if "support" in desired_dict][0][0]
        # print("support: ", support)
        # confidence = [desired_dict["confidence"] for desired_dict in rule if "confidence" in desired_dict][0][0]
        # print("confidence: ", confidence)
        # lift = [desired_dict["uplift"] for desired_dict in rule if "uplift" in desired_dict][0][0]
        # print("lift: ", lift)
        # new_rule = Rule(support=support, confidence=confidence, lift=lift)
        # print("newrule: ", new_rule)
        # db.session.add(new_rule)
        # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        # print("support", support[:5])
        # print(index+1, rule)
        # for measure in rule:
            #print("measure", measure)
            #measure_key = measure.keys()[]
            # print(measure.keys)

            #print(measure[measure_key])
            #measure = db.session.query(Measure.id).filter(Measure.name=measure.keys(), Measure.value=measure.value())

            #new_rule_measure = RuleMeasure(rule_id=index+1, measure_id)
        # break


    file.close()
    return redirect("/")

