#!/bin/python

import re
from functools import reduce

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

class system:
    def __init__(self, debug=0):

        self.debug = debug
        self.moons = []
        self._getMoons()
        self.steps = 0

    def _getMoons(self):

        for line in iter(input, ""):
            res = re.findall(r"x=(-?[0-9]+).+y=(-?[0-9]+).+z=(-?[0-9]+)", line)
            self.moons.append(
                moon(x=int(res[0][0]),
                     y=int(res[0][1]),
                     z=int(res[0][2]),
                     debug=self.debug))

    def _getVelocityDeltas(self):

        for moon in self.moons:
            for target_moon in self.moons:
                if moon != target_moon and not moon.period_found:
                    moon.calculateVelocityDeltas(target_moon)

    def _applyVelocityDeltas(self):

        for moon in self.moons:
            if not moon.period_found:
                moon.applyVelocityDeltas()

    def _stepMoons(self):
        ret = True

        for moon in self.moons:
            if not moon.period_found:
                if not moon.step(self.steps):
                    ret = False

        return ret

    def _step(self):

        self._getVelocityDeltas()
        self._applyVelocityDeltas()
        return self._stepMoons()


    def _printSystem(self, step):

        print("After {} step{}".format(step, 's' if step != 1 else ''))
        for moon in self.moons:
            moon.print()

    def stepSystem(self):

        while True:
            if self.debug == 1 and not (i % 10):
                self._printSystem(i)
            elif self.debug >= 2:
                self._printSystem(i)

            self.steps += 1

            if self._step():
                return


        self._printSystem(step_count)

    def printPeriods(self):

        periods = []
        for moon in self.moons:
            periods.append(moon.period)
            print("period: {}".format(moon.period))

        print("LCM {}".format(lcmm(periods[0], periods[1], periods[2], periods[3])))

    def printSystemEnergy(self):

        total_of_totals = 0

        for moon in self.moons:
            print("pot: {}, kin: {}, total: {}".format(moon.ke, moon.pe,
                                                       moon.te))
            total_of_totals += moon.te

        print("Total energy = {}".format(total_of_totals))


class moon:
    def __init__(self, x=0, y=0, z=0, v_x=0, v_y=0, v_z=0, debug=0):

        self.debug = debug

        self.initial_x = x
        self.initial_y = y
        self.initial_z = z

        self.x = x
        self.v_dx = 0
        self.y = y
        self.v_dy = 0
        self.z = z
        self.v_dz = 0
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

        self.pe = 0
        self.ke = 0
        self.te = 0

        self.period_found = False
        self.period = 0

    def _updatePE(self):

        self.pe = abs(self.x) + abs(self.y) + abs(self.z)

    def _updateKE(self):

        self.ke = abs(self.v_x) + abs(self.v_y) + abs(self.v_z)

    def _upodateTE(self):

        self.te = self.pe * self.ke

    def _updateAxis(self, axis, other_moons_axis):

        if abs(other_moons_axis - axis):
            if axis > other_moons_axis:
                return -1
            else:
                return 1

        return 0

    def _updateEnergies(self):

        if self.debug >= 3:
            prev_ke = self.ke
            prev_pe = self.pe
            prev_te = self.te

        self._updatePE()
        self._updateKE()
        self._upodateTE()

        if self.debug >= 3:
            print("Energy updated KE:{}->{}, PE:{}->{}, TE:{}->{}".format(
                prev_ke, self.ke, prev_pe, self.pe, prev_te, self.te))

    def _check(self, step):

        if self.period_found:
            return True

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

    def applyVelocityDeltas(self):

        if self.debug >= 3:
            prev_x = self.v_x
            prev_y = self.v_y
            prev_z = self.v_z

        self.v_x += self.v_dx
        self.v_dx = 0
        self.v_y += self.v_dy
        self.v_dy = 0
        self.v_z += self.v_dz
        self.v_dz = 0

        if self.debug >= 3:
            print("Updated moon ({},{},{}) -> ({},{},{})".format(
                prev_x, prev_y, prev_z, self.v_x, self.v_y, self.v_z))

    def calculateVelocityDeltas(self, moon):

        self.v_dx += self._updateAxis(self.x, moon.x)
        self.v_dy += self._updateAxis(self.y, moon.y)
        self.v_dz += self._updateAxis(self.z, moon.z)

        if self.debug >= 3:
            print(
                "Deltas calculated to be ({},{},{}) between ({},{},{}) & ({},{},{})"
                .format(self.v_dx, self.v_dy, self.v_dz, self.x, self.y,
                        self.z, moon.x, moon.y, moon.z))

    def step(self, cur_step):

        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z
        self._updateEnergies()
        return self._check(cur_step)

    def print(self):

        print(
            "pos=<x={: d}, y={: d}, z={: d}>, vel=<x={: d}, y={: d}, z={: d}>".
            format(self.x, self.y, self.z, self.v_x, self.v_y, self.v_z))


sys = system(debug=0)
sys.stepSystem()
sys._printSystem(sys.steps)
sys.printPeriods()
