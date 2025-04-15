from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from util.db import db

from ruleEngine.RuleEngine import RuleEngine
from ruleEngine.RelaisController import relaisController

class Relay(db.Model):
    port = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Relay {self.port}>'
    
relay_args = reqparse.RequestParser()
relay_args.add_argument('name', type=str, help='Name of the relay', required=True)
relay_args.add_argument('port', type=int, help='Port of the relay', required=True)
relayFields = {
    'name': fields.String,
    'port': fields.Integer,
    'status': fields.Boolean
}

class RelaysResource(Resource):
    @marshal_with(relayFields)
    def get(self):
        print('get all relays')
        relays = Relay.query.all()
        for relay in relays:
            relay.status = relaisController.getPortStatus(relay.port)

        if not relays:
            abort(404, message="No relays found")
        return relays
    
    @marshal_with(relayFields)
    def post(self):
        args = relay_args.parse_args()
        relay = Relay(name=args['name'], port=args['port'])
        db.session.add(relay)
        db.session.commit()

        relaisController.addRelais(relay.port)
        print(relaisController.getPorts())
        return relay, 201
    
class RelayResource(Resource):
    @marshal_with(relayFields)
    def get(self, relay_port):
        relay = Relay.query.get(relay_port)
        if not relay:
            abort(404, message="Relay not found")
        return relay

    @marshal_with(relayFields)
    def delete(self, relay_port):
        relay = Relay.query.get(relay_port)
        if not relay:
            abort(404, message="Relay not found")
        db.session.delete(relay)
        db.session.commit()
        return '', 204
    