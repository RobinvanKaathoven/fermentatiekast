from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from util.db import db
from ruleEngine.RuleEngine import ruleEngine


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    variant = db.Column(db.String(80), nullable=True)
    # Foreign key to Relay table
    relay = db.Column(db.Integer, db.ForeignKey('relay.port'), nullable=False)
    # Relationship to Relay table
    relay_ref = db.relationship('Relay', backref='relay', lazy=True)

    temperature = db.Column(db.Float, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    interval = db.Column(db.Integer, nullable=True)
    threshold = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<Rule {self.name}>'

rule_args = reqparse.RequestParser()
rule_args.add_argument('name', type=str, help='Name of the rule', required=True)
rule_args.add_argument('type', type=str, help='Type of the rule', required=True)
rule_args.add_argument('variant', type=str, help='Variant of the rule', required=False)
rule_args.add_argument('relay', type=int, help='Relay ID', required=True)
rule_args.add_argument('temperature', type=float, help='Temperature of the rule', required=False)
rule_args.add_argument('duration', type=int, help='Duration of the rule', required=False)
rule_args.add_argument('interval', type=int, help='Interval of the rule', required=False)
rule_args.add_argument('threshold', type=float, help='Threshold of the rule', required=False)
ruleFields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'variant': fields.String,
    'relay': fields.Integer,
    'temperature': fields.Float,
    'duration': fields.Integer,
    'interval': fields.Integer,
    'threshold': fields.Float
}

class RulesResource(Resource):
    @marshal_with(ruleFields)
    def get(self):
        print('get all rules')
        rules = Rule.query.all()
        if not rules:
            abort(404, message="No rules found")
        return rules
    
    @marshal_with(ruleFields)
    def post(self):
        args = rule_args.parse_args()
        rule = Rule(name=args['name'], type=args['type'], variant=args['variant'], relay=args['relay'], temperature=args['temperature'], duration=args['duration'], interval=args['interval'], threshold=args['threshold'])
        ruleEngine.addRule(rule)
        db.session.add(rule)
        db.session.commit()
        return rule, 201
    
class RuleResource(Resource):
    @marshal_with(ruleFields)
    def get(self, rule_id):
        rule = Rule.query.get(rule_id)
        if not rule:
            abort(404, message="Rule not found")
        return rule

    @marshal_with(ruleFields)
    def put(self, rule_id):
        args = rule_args.parse_args()
        rule = Rule.query.get(rule_id)
        if not rule:
            abort(404, message="Rule not found")
        rule.name = args['name']
        rule.type = args['type']
        rule.variant = args['variant']
        rule.relay = args['relay']
        rule.temperature = args['temperature']
        rule.duration = args['duration']
        rule.interval = args['interval']
        rule.threshold = args['threshold']
        db.session.commit()

        ruleEngine.addRule(rule)
        return rule
    
    @marshal_with(ruleFields)
    def delete(self, rule_id):
        rule = Rule.query.get(rule_id)
        if not rule:
            abort(404, message="Rule not found")
        db.session.delete(rule)
        db.session.commit()
        ruleEngine.removeRule(rule)
        return rule