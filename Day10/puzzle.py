#!/bin/python

import math


class coord:
    def __init__(self, x, y):

        self.x = x
        self.y = y


class trajectory:
    def __init__(self, coord1, coord2):

        x = coord2.x - coord1.x
        y = coord2.y - coord1.y
        self.mag = math.sqrt(x**2 + y**2)
        self.angle = -math.atan2(y, x)  # In radians


class asteroid:
    def __init__(self, x, y):

        self.coords = coord(x, y)
        self.trajectories = dict()
        self.los = 0

    def calculateTrajectory(self, other_asteroid):

        traj = trajectory(self.coords, other_asteroid.coords)
        if not str(traj.angle) in self.trajectories:
            self.trajectories[str(traj.angle)] = []

        angle_traj_list = self.trajectories[str(traj.angle)]
        angle_traj_list.append([traj.mag, other_asteroid])
        angle_traj_list = sorted(angle_traj_list, key=lambda tup: tup[0])

    def getAsteroid(self, angle):
        if str(angle) in self.trajectories:
            return self.trajectories[str(angle)][-1][1]

    def destroyAsteroid(self, angle):
        angle_traj_list = self.trajectories[str(angle)]
        if len(angle_traj_list) > 0:
            del angle_traj_list[-1]
            return True
        return False


asteroids = []

# Generate asteroid objects array from input
for y, line in enumerate(iter(input, "")):
    for x, item in enumerate(line):
        if item == '#':
            asteroids.append(asteroid(x, y))

# Trajectories from each asteroid to others
# Each trajectory is stored in a dict with the angle as a key, therefore
# multiple trajectories on the same angle will be stored with the same key meaning
# for each key in a dict you get one unique LOS
for asteroid in asteroids:
    for other_asteroid in asteroids:
        if other_asteroid != asteroid:
            asteroid.calculateTrajectory(other_asteroid)

# Check each asteroid and each of its trajectories
max_los = [0, None]

for asteroid in asteroids:
    asteroid.los = len(asteroid.trajectories.keys())
    if asteroid.los > max_los[0] or not max_los[1]:
        max_los = [asteroid.los, asteroid]

print("Max los ({}) asteroid position: {}, {}".format(max_los[0], max_los[1].coords.x, max_los[1].coords.y))

laser_asteroid = max_los[1]

asteroid_trajectories = sorted(list(float(i) for i in laser_asteroid.trajectories), reverse=True)

starting_index = math.radians(90)

for i in range(len(asteroid_trajectories) - 2):
    if asteroid_trajectories[i] >= starting_index > asteroid_trajectories[i + 1]:
        starting_index = i
        break

asteroids_destroyed = 0
i = starting_index

while True:

    if asteroids_destroyed == 199:
        the_last_asteroid = laser_asteroid.getAsteroid(asteroid_trajectories[i])
        print("Result: {}".format(the_last_asteroid.coords.x * 100 + the_last_asteroid.coords.y))
        break

    if laser_asteroid.destroyAsteroid(asteroid_trajectories[i]):
        asteroids_destroyed += 1

    i += 1
    if i == len(asteroid_trajectories):
        i = 0
