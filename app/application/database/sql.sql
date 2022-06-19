SELECT rule.id 
FROM rule 
WHERE (EXISTS (SELECT rule_measure.id 
FROM rule_measure JOIN measure ON measure.id = rule_measure.measure_id 
WHERE rule_measure.rule_id = rule.id AND measure.name = 'tempCategories' AND measure.description = '10.0, 20.0')) AND 
(EXISTS (SELECT rule_measure.id 
FROM rule_measure JOIN measure ON measure.id = rule_measure.measure_id 
WHERE rule_measure.rule_id = rule.id AND measure.name = 'C3_Cancel public events_general' AND measure.description = 'recommend cancelling')) AND
(EXISTS (SELECT rule_measure.id 
FROM rule_measure JOIN measure ON measure.id = rule_measure.measure_id 
WHERE rule_measure.rule_id = rule.id AND measure.name = 'C7_Restrictions on internal movement_general' AND measure.description = 'from no measures to internal movement restrictions in place ')) AND
(EXISTS (SELECT rule_measure.id 
FROM rule_measure JOIN measure ON measure.id = rule_measure.measure_id 
WHERE rule_measure.rule_id = rule.id AND measure.name = 'C8_International travel controls' AND measure.description = 'ban on arrivals from some regions')) AND
(EXISTS (SELECT rule_measure.id 
FROM rule_measure JOIN measure ON measure.id = rule_measure.measure_id 
WHERE rule_measure.rule_id = rule.id AND measure.name = 'C5_Close public transport_general' AND measure.description = 'no measures '));

'tempCategories', '10.0, 20.0', 'C3_Cancel public events_general', 'recommend cancelling'
C7_Restrictions on internal movement_general 0.0, 2.0
C5_Close public transport_general 0.0

CREATE INDEX measure_name 
ON measure(name, description);







































SELECT rule_measure.rule_id, rule.support AS rule_measure_rule_id 
FROM rule_measure JOIN measure ON rule_measure.measure_id = measure.id 
JOIN rule ON rule_measure.rule_id = rule.id 
WHERE measure.name = 'C2_Workplace closing_general' AND measure.description = ' from work from home for all except of intrastructure critical employees to work from home for some exployee categories' 
OR measure.name = 'C1_School closing_general' AND measure.description = 'closing of all levels'
ORDER BY rule.support DESC;















