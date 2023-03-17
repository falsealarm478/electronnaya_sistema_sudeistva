from app import app, Race, Tracks, db
from flask import request, jsonify, render_template
from random import *
import matplotlib.pyplot as plt
from datetime import datetime
from time import *
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

def get_telemetry(id, start_time, end_time, pilot2):
    vremya = end_time - start_time
    vremya = int(vremya.total_seconds()) * 10

    time_mass = []
    angle_mass = []
    angle = 0

    angle_mass1 = []
    angle1 = 0
    while vremya != 0:
        a = randint(0, 2)

        if a == 0 and angle > -120:
            angle -= 3
        elif a == 2 and angle < 120:
            angle += 3

        if pilot2:
            a1 = randint(0, 2)

            if a1 == 0 and angle1 > -120:
                angle1 -= 3
            elif a1 == 2 and angle1 < 120:
                angle1 += 3

            angle_mass1.append(angle1)

        angle_mass.append(angle)
        time_mass.append(vremya)
        vremya -= 1

    time_mass.reverse()

    if pilot2:
        fig, ax = plt.subplots()

        ax.plot(time_mass, angle_mass, color='blue', label='pilot1')
        ax.plot(time_mass, angle_mass1, color='green', label='pilot2')

        ax.set_xlabel('Время')
        ax.set_ylabel('Угол')
        ax.set_title('Зависимость угла от времени')

        ax.legend()
    else:
        plt.plot(time_mass, angle_mass)
        plt.xlabel('Время')
        plt.ylabel('Угол')
        plt.title('Зависимость угла от времени')

    path = f'static/track_{id}.jpg'
    plt.savefig(path)
    return path


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
    content = request.get_json()
    pilot1 = content['pilot1']
    pilot2 = content.get('pilot2') if content.get('pilot2') else None
    race_type = content['race_type']
    race_id = int(content['race_id'])

    start_time_date = content['start_time'].split()[0]
    start_time_time = content['start_time'].split()[1]

    end_time_date = content['end_time'].split()[0]
    end_time_time = content['end_time'].split()[1]

    start_time = datetime(year=int(start_time_date.split('.')[2]), month=int(start_time_date.split('.')[1]),
                 day=int(start_time_date.split('.')[0]), hour=int(start_time_time.split(':')[0]),
                 minute=int(start_time_time.split(':')[1]), second=int(start_time_time.split(':')[2]))

    end_time = datetime(year=int(end_time_date.split('.')[2]), month=int(end_time_date.split('.')[1]),
                 day=int(end_time_date.split('.')[0]), hour=int(end_time_time.split(':')[0]),
                 minute=int(end_time_time.split(':')[1]), second=int(end_time_time.split(':')[2]))

    track = Tracks(pilot1=pilot1, pilot2=pilot2, race_type=race_type, start_time=start_time, end_time=end_time, race_id=race_id)
    db.session.add(track)
    db.session.commit()

    future = executor.submit(get_telemetry, track.id, start_time, end_time, pilot2=pilot2)

    # Wait for the task to complete and get the result
    path = future.result()

    track.telemetry = path
    db.session.commit()
    db.session.close()

    return '200'


@app.route('/get_competitions')
def get_competition():
    response = ''

    races = Race.query.all()

    return render_template('competitions_1.html', races=races)


