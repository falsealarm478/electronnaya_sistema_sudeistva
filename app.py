from flask import Flask
from flask_migrate import Migrate
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from secretKeys import *
from generator import get_telemetry

app = Flask(__name__)
app.config.from_object(Configuration)
app.secret_key = secret_key
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Race(db.Model):
    __tablename__ = 'race'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    date = db.Column(db.DateTime)
    organizer = db.Column(db.String(40))
    place = db.Column(db.String(160))
    tracks = db.relationship('Tracks', backref='race', lazy=True)

    def __init__(self, name, date, organizer, place):
        self.name = name
        self.date = date
        self.organizer = organizer
        self.place = place


    def __repr__(self):
        return '<Competition %r>' % self.competition_name

    def __str__(self):
        return f'{self.id}, {self.name}'
class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pilot1 = db.Column(db.Integer)
    pilot2 = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    race_type = db.Column(db.String(40))
    telemetry = db.Column(db.String(100), nullable=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'), nullable=False)

    def __init__(self, pilot1, pilot2, start_time, end_time, race_type):
        self.pilot1 = pilot1
        self.pilot2 = pilot2
        self.start_time = start_time
        self.end_time = end_time
        self.race_type = race_type




