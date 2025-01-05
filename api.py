from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fermentation.db' # Using SQLite for simplicity
db = SQLAlchemy(app)

class Fermentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Fermentation {self.name} from {self.startDate}>'

@app.route('/')
def home():
    return "Welcome to the Home Page!"

if __name__ == '__main__':
    app.run(debug=True) # This will start the Flask web server in debug mode
