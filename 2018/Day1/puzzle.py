#!/bin/python

import copy

puzzle_input = []

for line in iter(input, ""):
    puzzle_input.append(line)

frequency = 0
frequencies = [0]

for number in puzzle_input:
    freq = int(number[1:])
    if number[0] == '+':
        frequency += freq
    else:
        frequency -= freq

    if frequency in frequencies:
        print("Repeated freq: {}".format(frequency))
        break
    else:
        frequencies.append(copy.copy(frequency))

print(frequencies)
