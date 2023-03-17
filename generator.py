from random import *
import matplotlib.pyplot as plt
from time import *
import datetime
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



