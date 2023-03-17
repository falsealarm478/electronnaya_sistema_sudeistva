from app import app, Race, Tracks, db
from flask import request, jsonify
from datetime import datetime
from generator import get_telemetry
@app.route('/')
def hello():
    return 'hello'
@app.route('/create', methods = ['POST'])
def createRace():
    content = request.get_json()
    date = content["date"].split()[0]
    time = content["date"].split()[1]
    d = datetime(year=int(date.split('.')[2]), month= int(date.split('.')[1]),
                 day= int(date.split('.')[0]), hour=int(time.split(':')[0]),
                 minute= int(time.split(':')[1]))
    r = Race(content["name"], d, content["organizer"], content["place"])

    db.session.add(r)
    db.session.commit()
    db.session.close()
    return '200'

@app.route('/create_track', methods = ['POST'])
def createTrack():
    content = ...
    pilot1 = ...
    pilot2 = ...
    race_type = ...
    start_time = ...
    end_time = ...

    track = Tracks(pilot1=pilot1, pilot2=pilot2, race_type=race_type, start_time=start_time, end_time=end_time)
    track.telemetry = get_telemetry(track.id)

    db.session.add(track)
    db.session.commit()
    db.session.close()
    return '200'
