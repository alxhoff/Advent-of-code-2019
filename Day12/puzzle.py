#!/bin/python

import re
import copy


class system:
    def __init__(self, debug=0):

        self.debug = debug

        self.moons = self._getMoons()

        self.steps = 0

    def _getMoons(self):

        moons = []
        for line in iter(input, ""):
            res = re.findall(r"x=(-?[0-9]+).+y=(-?[0-9]+).+z=(-?[0-9]+)", line)
            moons.append(
                moon(x=int(res[0][0]),
                     y=int(res[0][1]),
                     z=int(res[0][2]),
                     debug=self.debug))

        return moons

    def _getVelocityDeltas(self):

        for i in range(len(self.moons)):
            if not self.moons[i].period_found:
                for j in range(len(self.moons)):
                    if i != j:
                        self.moons[i].calculateVelocityDeltas(self.moons[j])

    # If all moons have found their periods return True
    def _stepMoons(self):

        ret = True

        for i in range(len(self.moons)):
            if not self.moons[i].period_found:
                #  Returns if the moon is back to its initial position
                if not self.moons[i].step(self.steps):
                    ret = False

        return ret

    def _step(self):

        self._getVelocityDeltas()

        #  Return true when all moons' periods have been found
        return self._stepMoons()

    def _printSystem(self, initial=False):

        if initial:
            for moon in self.initial_positions:
                moon.print()
        else:
            print("After {} step{}".format(self.steps,
                                           's' if self.steps != 1 else ''))
            for moon in self.moons:
                moon.print()

    #  Run until all moons have found their periods
    def stepSystem(self, steps=0):

        while True:

            if self._step():
                return
            self.steps += 1

            if self.steps == steps:
                return

            if not self.steps % 100000:
                self._printSystem()
                print("step: {}".format(self.steps))


        period = []
        for moon in self.moons:
            period.append(moon.period)

        print("Periods = {}, {}, {}, {}".format(period[0], period[1], period[2], period[3]))


class moon:
    def __init__(self, x=0, y=0, z=0, v_x=0, v_y=0, v_z=0, debug=0):

        self.debug = debug

        self.initial_x = x
        self.initial_y = y
        self.initial_z = z

        self.x = x
        self.y = y
        self.z = z

        self.v_dx = 0
        self.v_dy = 0
        self.v_dz = 0

        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

        self.period_found = False
        self.period = 0

    def _updateAxis(self, axis, other_moons_axis):

        if abs(other_moons_axis - axis):
            if axis > other_moons_axis:
                return -1
            else:
                return 1

        return 0

    def _update(self):

        if not self.period_found:
            self.v_x += self.v_dx
            self.x += self.v_x
            self.v_dx = 0

            self.v_y += self.v_dy
            self.y += self.v_y
            self.v_dy = 0

            self.v_z += self.v_dz
            self.z += self.v_z
            self.v_dz = 0

    #  Returns true is moon is back in original position
    def _check(self, step):

        if step==2772 or step==2771:
            print("wait here")

        if self.x != self.initial_x:
            return False
        if self.y != self.initial_y:
            return False
        if self.z != self.initial_z:
            return False

        # Initial velocity is zero
        if self.v_x != 0:
            return False
        if self.v_y != 0:
            return False
        if self.v_z != 0:
            return False

        self.period_found = True
        self.period = step

        print("Period found! {}".format(step))

        return True

    def calculateVelocityDeltas(self, moon):

        if not self.period_found:
            self.v_dx += self._updateAxis(self.x, moon.x)
            self.v_dy += self._updateAxis(self.y, moon.y)
            self.v_dz += self._updateAxis(self.z, moon.z)

    def step(self, step):

        self._update()
        return self._check(step)

    def print(self):

        print(
            "pos=<x={: d}, y={: d}, z={: d}>, vel=<x={: d}, y={: d}, z={: d}>".
            format(self.x, self.y, self.z, self.v_x, self.v_y, self.v_z))

    def printInitial(self):

        print(
            "pos=<x={: d}, y={: d}, z={: d}>, vel=<x=0, y=0, z=0>".
            format(self.initial_x, self.initial_y, self.initial_z))

sys = system()
sys.stepSystem(3000)
