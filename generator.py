from random import *
import matplotlib.pyplot as plt
from time import *
def get_telemetry(id):
    vremya = 600
    time_mass = []
    angle_mass = []
    angle = 0

    angle_mass1 = []
    angle1 = 0
    while vremya != 0:
        a = randint(0, 2)
        a1 = randint(0,2)

        if a == 0 and angle > -120:
            angle -= 3
        elif a == 2 and angle < 120:
            angle += 3

        if a1 == 0 and angle1 > -120:
            angle1 -= 3
        elif a1 == 2 and angle1 < 120:
            angle1 += 3

        angle_mass.append(angle)
        angle_mass1.append(angle1)
        time_mass.append(vremya)
        vremya -= 1

    time_mass.reverse()
    fig, ax = plt.subplots()

    ax.plot(time_mass, angle_mass, color='blue', label='pilot1')
    ax.plot(time_mass, angle_mass1, color='green', label='pilot2')

    ax.set_xlabel('Время')
    ax.set_ylabel('Угол')
    ax.set_title('Зависимость угла от времени')

    ax.legend()

    path = f'static/track_{id}.jpg'
    plt.savefig(path)  # сохранение графика в указанном пути

    return path



