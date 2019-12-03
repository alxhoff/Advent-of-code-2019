#! /bin/python

import math


def get_fuel(mass):
    return int(math.floor(mass / 3.0)) - 2


total_fuel = 0

for line in iter(input, ""):
    total_fuel += get_fuel(int(line))

print("Done")

print(total_fuel)
