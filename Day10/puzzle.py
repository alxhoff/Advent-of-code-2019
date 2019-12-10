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
        self.angle = math.atan2(y, x)  # In radians


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
            return self.trajectories[str(angle)]

    def destroyAsteroid(self, angle):
        angle_traj_list = self.trajectories[str(angle)]
        if len(traj) > 0:
            del angle_traj_list[0]
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
