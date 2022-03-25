from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    support = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    lift = db.Column(db.Float, nullable=False)


class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)


class RuleMeasure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_id = db.Column(db.Integer, db.ForeignKey(Rule.id), nullable=False)
    measure_id = db.Column(db.Integer, db.ForeignKey(Measure.id), nullable=False)