#! /bin/python
import math


def get_program():
    program = input("").split(",")

    for entry in range(len(program)):
        program[entry] = int(program[entry])

    return program


def run_program(program):
    for i in range(math.ceil(len(program) / 4)):
        instruction = program[0 + (i * 4):4 + (i * 4)]
        if instruction[0] == 1:  # Addition
            op1 = program[instruction[1]]
            op2 = program[instruction[2]]
            try:
                program[instruction[3]] = op1 + op2
            except Exception:
                return -1
        elif instruction[0] == 2:  #Multiplication
            op1 = program[instruction[1]]
            op2 = program[instruction[2]]
            try:
                program[instruction[3]] = op1 * op2
            except Exction:
                return -1
        elif instruction[0] == 99:
            return 0


program = get_program()

for noun in range(100):
    for verb in range(100):
        test_program = program.copy()
        test_program[1] = noun
        test_program[2] = verb
        if run_program(test_program) == 0:
            if test_program[0] == 19690720:
                print("Noun: {}, verb: {}, output: {}".format(
                    noun, verb, test_program[0]))
                print("Result: {}".format(100 * noun + verb))
