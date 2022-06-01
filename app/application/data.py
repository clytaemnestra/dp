from models import Rule, db

file = open("/home/mia/Documents/repos/skola/dp/app/application/formatted_rules", "r")
contents = file.readlines()
rules_list = []
for item in contents:
    rules_list.append(eval(item))

support = []
for rule in rules_list:
    try:
        support = [desired_dict["support"] for desired_dict in rule if "support" in desired_dict]
        support.append(support)
        confidence = [desired_dict["confidence"] for desired_dict in rule if "confidence" in desired_dict]
        lift = [desired_dict["uplist"] for desired_dict in rule if "uplist" in desired_dict]
        new_rule = Rule(support=support, confidence=confidence, lift=lift)
        db.session.add(new_rule)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
print(support)
    # break

    # print(type(rules_list))
file.close()

# with open("formatted_rules") as inputfile:
#     rows = [line.split() for line in inputfile]
# columns = zip(*rows)
#
# print(rows[0])


"""
read lines 

for every rule create a new Rule and add support confidence and lift
how to add? 
dictionary key - value 

for every rule 
for every measure
create a new RuleMeasure
find measure.id based on measure.name = measure a measure.value = measure.value
add rule.id
add measure.id
"""