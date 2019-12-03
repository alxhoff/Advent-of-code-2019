#! /bin/python

import numpy as np


def generate_coords(corner_list):
    coord = []
    current_loc = np.array([0, 0])
    for turn in corner_list:
        direction = turn[0]
        distance = int(turn[1:])
        move = np.array([0, 0])
        if direction == 'R':
            move[0] = 1
        elif direction == 'L':
            move[0] = -1
        elif direction == 'U':
            move[1] = 1
        elif direction == 'D':
            move[1] = -1

        for i in range(distance):
            current_loc += move
            coord.append(tuple(np.array(current_loc)))

    return coord


wire1 = generate_coords(input("Wire1: ").split(","))
wire2 = generate_coords(input("Wire2: ").split(","))

crossovers = list(set(wire1) & set(wire2))

req_steps = 0

for crossover in crossovers:
    steps_wire1 = min([i for i, j in enumerate(wire1) if j == crossover])
    steps_wire2 = min([i for i, j in enumerate(wire2) if j == crossover])

    steps = steps_wire1 + steps_wire2

    if req_steps == 0 or steps < req_steps:
        req_steps = steps

req_steps += 2

print(req_steps)
