#!/bin/python

import re


class system:

    def __init__(self):

        self.moons = []

    def get_moons():

        for line in iter(input, ""):
            res = re.findall(r"x=(-?[0-9]+).+y=(-?[0-9]+).+z=(-?[0-9])", line)
            self.moons.append(moon(x=res[0][0], y=res[0][1], z=res[0][2]))

    def step():
        for moon in self.moons():
            for target_moon in self.moons():
                if moon != target_moon:
                    moon.updateVelocity(target_moon)


class moon:

    def __init__(self, x=0, y=0, z=0, v_x=0, v_y=0, v_z=0):

        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

    def updateVelocity(self, moon):
        return


print(get_moons())
