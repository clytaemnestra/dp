import ast

file = open("/home/mia/Documents/repos/skola/dp/app/application/database/formatted_rules", "r")
contents = file.read()
dictionary = ast.literal_eval(contents)
file.close()

print(type(dictionary))


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