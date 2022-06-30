from ..models import Rule, db, Measure, RuleMeasure
import ast

file = open("/home/mia/Documents/repos/skola/dp/app/application/formatted_rules", "r")
contents = file.readlines()

# add rule ids, support, confidence & lift
rules_list = []
for item in contents:
    rules_list.append(eval(item))

for rule in rules_list:
    try:
        support = [
            desired_dict["support"]
            for desired_dict in rule
            if "support" in desired_dict
        ]
        support.append(support)
        confidence = [
            desired_dict["confidence"]
            for desired_dict in rule
            if "confidence" in desired_dict
        ]
        lift = [
            desired_dict["uplist"] for desired_dict in rule if "uplist" in desired_dict
        ]
        new_rule = Rule(support=support, confidence=confidence, lift=lift)
        db.session.add(new_rule)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
file.close()

# add rule measures
rules = file.readlines()
all_measures_from_rules = []
measures_with_unique_values = {}
for index, rule in enumerate(rules):
    rules_dict = ast.literal_eval(rule)
    for key in rules_dict.keys():
        # if key not in all_measures_from_rules + ['support', 'confidence', 'uplift']:
        #     all_measures_from_rules.append(key)

        if key not in ["support", "confidence", "uplift"]:
            measure_id = (
                db.session.query(Measure.id)
                .filter(Measure.name == key, Measure.value == rules_dict[key])
                .one()
            )
            new_rule_measure = RuleMeasure(rule_id=index + 1, measure_id=measure_id[0])
            db.session.add(new_rule_measure)
            db.session.commit()
file.close()
