#! /bin/python

import math


def get_fuel(mass):
    fuel = int(math.floor(mass / 3.0)) - 2
    if fuel > 0:
        return fuel + get_fuel(fuel)
    else:
        return 0


total_fuel = 0

for line in iter(input, ""):
    total_fuel += get_fuel(int(line))

print("Done")

print(total_fuel)
