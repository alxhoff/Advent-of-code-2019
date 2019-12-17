#!/bin/python

import re
from functools import reduce
from enum import Enum


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


class DIMENSION(Enum):

    X = 0
    Y = 1
    Z = 2

    def __str__(self):
        return str(self.name)


class SolarSystem:
    def __init__(self, debug=0):

        self.debug = debug
        self.moons = self._getMoons()
        self.steps_taken = 0
        self.periods = [0, 0, 0]
        self.dimensions = [DIMENSION.X, DIMENSION.Y, DIMENSION.Z]

    def _getMoons(self):

        moons = []

        for line in iter(input, ""):
            res = re.findall(r"x=(-?[0-9]+).+y=(-?[0-9]+).+z=(-?[0-9]+)", line)
            moons.append(
                Moon(x=int(res[0][0]), y=int(res[0][1]), z=int(res[0][2])))
        return moons

    def _updateMoonVelocities(self, dimension):

        for moon in self.moons:
            for target_moon in self.moons:
                if moon != target_moon:
                    moon.updateVelocity(target_moon, dimension)

    def _stepMoons(self, dimension):
        ret = True

        self._updateMoonVelocities(dimension)

        for moon in self.moons:
            if not moon.step(dimension):
                ret = False

        return ret

    def _printSystem(self):

        print("After {} step{}".format(self.steps_taken,
                                       's' if self.steps_taken != 1 else ''))
        for moon in self.moons:
            moon.printMoon()

    def findPeriods(self, steps=0):

        if steps:
            for i in range(steps):
                for dimension in self.dimensions:
                    self._stepMoons(dimension)
                self.steps_taken += 1
                self._printSystem()
            return

        self._printSystem()
        for dimension in self.dimensions:
            self.steps_taken = 0
            while not self._stepMoons(dimension):
                self.steps_taken += 1
            self.steps_taken += 1
            self.periods[dimension.value] = self.steps_taken
            print("Found period {} for {} axis".format(self.steps_taken,
                                                       str(dimension)))

        print("LCM: {}".format(
            lcmm(self.periods[0], self.periods[1], self.periods[2])))


class Moon:
    def __init__(self, x=0, y=0, z=0):

        self.initial = [x, y, z]
        self.position = [x, y, z]
        self.v = [0, 0, 0]

    def _updateAxis(self, axis, other_moons_axis):

        if abs(other_moons_axis - axis):
            if axis > other_moons_axis:
                return -1
            else:
                return 1

        return 0

    def _check(self, dimension):

        if self.position[dimension.value] != self.initial[
                dimension.value] or self.v[dimension.value] != 0:
            return False

        return True

    def _applyVelocity(self, dimension):

        self.position[dimension.value] += self.v[dimension.value]

    def updateVelocity(self, moon, dimension):

        self.v[dimension.value] += self._updateAxis(
            self.position[dimension.value], moon.position[dimension.value])

    def step(self, dimension):

        self._applyVelocity(dimension)
        return self._check(dimension)

    def printMoon(self):

        print(
            "pos=<x={: d}, y={: d}, z={: d}>, vel=<x={: d}, y={: d}, z={: d}>".
            format(self.position[0], self.position[1], self.position[2],
                   self.v[0], self.v[1], self.v[2]))


sys = SolarSystem(debug=0)
sys.findPeriods()
