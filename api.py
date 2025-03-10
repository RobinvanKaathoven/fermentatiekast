from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fermentation.db' # Using SQLite for simplicity
db = SQLAlchemy(app)
api = Api(app)

class Fermentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    startDate = db.Column(db.DateTime, nullable=True)
    endDate = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Fermentation {self.name} from {self.startDate}>'

fermentation_args = reqparse.RequestParser()
fermentation_args.add_argument('name', type=str, help='Name of the fermentation', required=True)
fermentation_args.add_argument('temperature', type=float, help='Requested temperature of the fermentation', required=True)
fermentation_args.add_argument('duration', type=int, help='Duration of the fermentation in days', required=True)
fermentationFields = {
    'id': fields.Integer,
    'name': fields.String,
    'temperature': fields.Float,
    'duration': fields.Integer,
    'startDate': fields.DateTime,
    'endDate': fields.DateTime
}

class FermentationsResource(Resource):
    @marshal_with(fermentationFields)
    def get(self):
        print('get all fermentations')
        fermentations = Fermentation.query.all()
        if not fermentations:
            abort(404, message="No fermentations found")
        return fermentations
    
    @marshal_with(fermentationFields)
    def post(self):
        args = fermentation_args.parse_args()
        fermentation = Fermentation(name=args['name'], temperature=args['temperature'], duration=args['duration'])
        db.session.add(fermentation)
        db.session.commit()
        return fermentation, 201
    
    
class FermentationResource(Resource):

    
    @marshal_with(fermentationFields)
    def get(self, fermentation_id):
        fermentation = Fermentation.query.get(fermentation_id)
        if not fermentation:
            abort(404, message="Fermentation not found")
        return fermentation

    @marshal_with(fermentationFields)
    def patch(self, fermentation_id):
        print(fermentation_id)
        args = fermentation_args.parse_args()
        fermentation = Fermentation.query.get(fermentation_id)
        if not fermentation:
            abort(404, message="Fermentation not found")
        if 'name' in args:
            fermentation.name = args['name']
        if 'temperature' in args:
            fermentation.temperature=args['temperature']
        if 'duration' in args:
            fermentation.duration=args['duration']
        if 'startDate' in args:
            fermentation.startDate=args['startDate']
        if 'endDate' in args:
            fermentation.endDate=args['endDate']      
        db.session.commit()
        return fermentation, 201

api.add_resource(FermentationResource, '/api/fermentation/<int:fermentation_id>')
api.add_resource(FermentationsResource, '/api/fermentation/')

@app.route('/')
def home():
    return "Welcome to the Home Page!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) # This will start the Flask web server in debug