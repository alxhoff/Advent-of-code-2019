#!/bin/python

import numpy as np
from queue import Queue
from intCodeComp import intCodeComputer

grid = np.full((50, 50), 0)

inp_q = Queue()
outp_q = Queue()

program = "109,424,203,1,21101,11,0,0,1105,1,282,21101,18,0,0,1105,1,259,2101,0,1,221,203,1,21101,31,0,0,1106,0,282,21102,1,38,0,1106,0,259,21002,23,1,2,22102,1,1,3,21101,0,1,1,21101,0,57,0,1105,1,303,1202,1,1,222,21002,221,1,3,20102,1,221,2,21102,259,1,1,21101,0,80,0,1105,1,225,21101,104,0,2,21101,0,91,0,1106,0,303,2101,0,1,223,20102,1,222,4,21101,0,259,3,21102,1,225,2,21102,1,225,1,21102,1,118,0,1106,0,225,20102,1,222,3,21101,67,0,2,21102,133,1,0,1105,1,303,21202,1,-1,1,22001,223,1,1,21102,148,1,0,1105,1,259,1202,1,1,223,20102,1,221,4,21001,222,0,3,21101,0,18,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21101,195,0,0,105,1,109,20207,1,223,2,21001,23,0,1,21101,-1,0,3,21102,214,1,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1202,-4,1,249,22101,0,-3,1,22102,1,-2,2,21202,-1,1,3,21101,250,0,0,1106,0,225,21202,1,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,21201,-2,0,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21202,-2,1,3,21102,343,1,0,1106,0,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21101,384,0,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21201,1,0,-4,109,-5,2106,0,0"

ic = intCodeComputer(program_str=program,
                     input_queue=inp_q,
                     output_queue=outp_q)


def clearOutputQueue():

    while not outp_q.empty():
        outp_q.get()


def request(x, y):
    inp_q.put(x)
    inp_q.put(y)
    clearOutputQueue()
    ic.runInitialProgram()
    ret = outp_q.get(block=True)
    print("{},{} -> {}".format(x, y, ret))
    return ret


# part 1
print_str = ""

for y, row in enumerate(grid):
    for x, col in enumerate(row):
        print("{},{}".format(x, y))
        grid[y][x] = request(x, y)
        print_str += '#' if grid[y][x] else '.'
    print_str += '\n'

print(print_str)

result = sum(list(filter(lambda x: x == 1, grid.flatten())))

print("Result = {}".format(result))

# part 2

# Search algorithm - brute force
# Starting from (400,700)
# While not finished
#   If current is 1
#       If x - 1 is also 1:
#           x -= 20
#               continue
#       If the point with the y-99 and x+99 also have a #
#           Finished
#   else

cur_x = 0
cur_y = 100
square_size = 100
coord_diff = square_size - 1
finished = False
while not finished:
    print("move x")
    if request(cur_x, cur_y):
        print("check opposite corner")
        if request(cur_x + coord_diff, cur_y - coord_diff):
            finished = True
            break
        cur_y += 1
    else:
        cur_x += 1

print("Result: ({},{}) -> {}".format(cur_x, cur_y - 99,
                                     cur_x * 10000 + cur_y - coord_diff))
