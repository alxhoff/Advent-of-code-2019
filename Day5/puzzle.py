#! /bin/python
import math
from enum import Enum


class parameterMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1


def get_program():
    program = input("").split(",")

    for entry in range(len(program)):
        program[entry] = int(program[entry])

    return program


class parameter:
    def __init__(self, program, position, value, mode=parameterMode.POSITION_MODE):

        self.program = program
        self.position = position
        self.value = value
        self.mode = mode

    def getValue(self):
        if self.mode == parameterMode.POSITION_MODE.value:
            return self.program[self.value]
        elif self.mode == parameterMode.IMMEDIATE_MODE.value:
            return self.program[self.position]

    def setValue(self, value):
        if self.mode == parameterMode.POSITION_MODE.value:
            self.program[self.value] = value
        elif self.mode == parameterMode.IMMEDIATE_MODE.value:
            self.program[self.position] = value


class intCodeComputer:
    def __init__(self, program, arg1=None, arg2=None):

        self.pc = 0
        self.parameter_modes = 0
        self.program = program
        self.output = None
        if arg1:
            program[1] = arg1
        if arg2:
            program[2] = arg2

    def getOpcode(self):
        self.getParameterModes()
        return self.program[self.pc] % 100

    def getParameterModes(self):
        self.parameter_modes = self.program[self.pc] // 10**2

    def getSingleParameterMode(self, n):
        return self.parameter_modes // 10**n % 10

    def getOperand(self, n, override_mode=None):
        position = self.pc + n + 1
        if override_mode:
            return parameter(program=self.program, position=position, value=self.program[position], mode=override_mode.value)
        else:
            return parameter(program=self.program, position=position, value=self.program[position], mode=self.getSingleParameterMode(n))

    def printState(self):
        print("pc: {}".format(self.pc))

    def printProgram(self):
        print(self.program)

    def endProgram(self):
        self.output = self.program[0]
        print("Program Output: {}".format(self.output))

    def runProgram(self):
        self.pc = 0
        while True:
            if self.pc == 208:
                print("wait here")
            try:
                opcode = self.getOpcode()
            except Exception:
                return 0
            if opcode == 1 or opcode == 2:  #3 operand instructions
                op1 = self.getOperand(0)
                op2 = self.getOperand(1)
                op3 = self.getOperand(2)
                if opcode == 1:  #Addition
                    try:
                        op3.setValue(op1.getValue() + op2.getValue())
                    except Exception:
                        return -1
                elif opcode == 2:  #Multiplication
                    try:
                        op3.setValue(op1.getValue() * op2.getValue())
                    except Exction:
                        return -1
                self.pc += 4
            elif opcode == 3 or opcode == 4:  #1 operand instructions
                if opcode == 3:  #Input
                    op1 = self.getOperand(0, override_mode=parameterMode.POSITION_MODE)
                    op1.setValue(int(input("Input $>")))
                elif opcode == 4:  #Output
                    op1 = self.getOperand(0)
                    print("Output @{} $>{}".format(self.pc, op1.getValue()))
                self.pc += 2
            elif opcode == 99:
                self.endProgram()
                break


program = get_program()

comp = intCodeComputer(program)

comp.runProgram()
