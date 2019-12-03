#! /bin/python
import math

program = []


def set_register(offset, value):
    global program
    if offset < len(program):
        program[offset] = value


def get_register(offset):
    global program
    if offset < len(program):
        return program[offset]

    return 0


def execute_instruction(instruction):
    if instruction[0] == 1:  # Addition
        op1 = get_register(instruction[1])
        op2 = get_register(instruction[2])
        set_register(instruction[3], op1 + op2)
        return 0
    elif instruction[0] == 2:  #Multiplication
        op1 = get_register(instruction[1])
        op2 = get_register(instruction[2])
        set_register(instruction[3], op1 * op2)
        return 0
    elif instruction[0] == 99:
        return -1


def modify_program():
    global program
    program[1] = 12
    program[2] = 2


def run_program():
    global program
    instructions = []
    program = input("").split(",")

    modify_program()

    for entry in range(len(program)):
        program[entry] = int(program[entry])

    for i in range(math.ceil(len(program) / 4)):
        if execute_instruction(program[0 + (i * 4):4 + (i * 4)]) == -1:
            return


run_program()

print("Done")
print(program[0])
