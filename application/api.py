import os, sys
import time
from flask import Flask
from flask import render_template 

from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_swagger_ui import get_swaggerui_blueprint
from util import db

from ruleEngine.RuleEngine import ruleEngine
from sensors.temperature import TemperatureSensor
from threading import Thread

from ruleEngine.Rule import Rule
from fermentation.FermentationResource import *
from ruleEngine.RelayResource import *
from ruleEngine.RuleResource import *

import json

DEBUG_MODE = True
print("Things have been imported")

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fermentation.db' # Using SQLite for simplicity
db.init_app(app)
api = Api(app)

temperatureSensor = TemperatureSensor(4)

api.add_resource(FermentationResource, '/api/fermentation/<int:fermentation_id>')
api.add_resource(FermentationsResource, '/api/fermentation/')
api.add_resource(RelayResource, '/api/relay/<int:relay_port>')
api.add_resource(RelaysResource, '/api/relays/')
api.add_resource(RulesResource, '/api/rules/')
api.add_resource(RuleResource, '/api/rule/<int:rule_id>')


sensor_args = reqparse.RequestParser()
sensor_args.add_argument('temperature', type=float, help='Temperature of the mock sensor', required=True)
sensor_args.add_argument('humidity', type=int, help='Humidity of the mock sensor', required=True)
sensorFields = {
    'temperature': fields.Float,
    'humidity': fields.Integer
}

testRelais_args = reqparse.RequestParser()
testRelais_args.add_argument('number', type=int, help='Number of the relais to test', required=True)
testRelais_args.add_argument('status', type=bool, help='turn off or on', required=True)
testRelaisFields = {    
    'number': fields.Integer,
    'status': fields.Boolean
}

class TestRelaisResource(Resource):
    @marshal_with(testRelaisFields)
    def post(self):
        args = testRelais_args.parse_args()
        number = args['number']
        status = args['status']
        if status:
            ruleEngine.testOn(number)
        else:
            ruleEngine.testOff(number)
        return {'number': number, 'status': status}
if DEBUG_MODE:
    api.add_resource(TestRelaisResource, '/api/testrelais/')

class MockResource(Resource):
    @marshal_with(sensorFields)
    def get(self):
        return {'temperature': temperatureSensor.temperature, 'humidity': temperatureSensor.humidity}

    @marshal_with(sensorFields)
    def post(self):
        args = sensor_args.parse_args()
        temperatureSensor.set(args['temperature'], args['humidity'])
        return {'temperature': temperatureSensor.temperature, 'humidity': temperatureSensor.humidity}
if DEBUG_MODE:
    api.add_resource(MockResource, '/api/mock/')

class TargetResource(Resource):
    @marshal_with(sensorFields)
    def get(self):
        return {'temperature': ruleEngine.getTargetTemperature(), 'humidity': ruleEngine.getTargetHumidity()}

    @marshal_with(sensorFields)
    def post(self):
        args = sensor_args.parse_args()
        ruleEngine.setTargetTemperature(args['temperature'])
        ruleEngine.setTargetHumidity(args['humidity'])
        return {'temperature': ruleEngine.getTargetTemperature(), 'humidity': ruleEngine.getTargetHumidity()}
api.add_resource(TargetResource, '/api/target/')

@app.route('/')
def home():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route('/relays')
def relays():
    message = "Hello, World"
    return render_template('relays.html', message=message)

@app.route('/rules')
def rules():
    message = "Hello, World"
    return render_template('rules.html', message=message)


@app.route("/metrics")
def metrics():
    metrics = temperatureSensor.read()
    result = [metric.to_prometheus() for metric in metrics]
    return "\n".join(result), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/api/current")
def current():
    data = temperatureSensor.readJson()
    return json.dumps(data)


#swagger configs
swaggerUrl = '/swagger' # URL for the Swagger UI
apiUrl = '/static/swagger.json' # URL for the API"
swaggerBlueprint = get_swaggerui_blueprint(
    swaggerUrl,
    apiUrl,
    config={
        'app_name': "Fermentation API"
    }
)

app.register_blueprint(swaggerBlueprint, url_prefix=swaggerUrl)
counter = 0
def ruleEvaluation():
    while True:
        global counter
        counter += 1
        values = temperatureSensor.read()
        print(f"{counter} Eval for Temperature: {values[0].value}, Humidity: {values[1].value}")
        ruleEngine.evaluateRules(values[0].value, values[1].value)
        time.sleep(10)
        
if __name__ == '__main__':
    with app.app_context():
        relays = Relay.query.all()
        relaisController.setPorts([relay.port for relay in relays])
        rules = Rule.query.all()
        for rule in rules:
            ruleEngine.addRule(rule)

        # Start the rule evaluation thread
        ruleEvaluationThread = Thread(target=ruleEvaluation)
        ruleEvaluationThread.start()
    
    app.run(host='0.0.0.0', debug=True) # This will start the Flask web server in debug

