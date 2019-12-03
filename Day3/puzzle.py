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


def shortest_distance(crossovers):
    min_dist = 0

    for entry in crossovers:
        dist = abs(entry[0]) + abs(entry[1])
        if min_dist == 0 or dist < min_dist:
            min_dist = dist

    return min_dist


wire1 = generate_coords(input("Wire1: ").split(","))
wire2 = generate_coords(input("Wire2: ").split(","))

crossovers = list(set(wire1) & set(wire2))

print(crossovers)

print(shortest_distance(crossovers))
