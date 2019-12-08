#! /bin/python
import threading
import math
from queue import Queue
from enum import Enum


class parameterMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1


def get_program():
    program = input("Program $> ").split(",")

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


class intCodeComputer(threading.Thread):
    def __init__(self, ID, phase, program, arg1=None, arg2=None, input_queue=None, output_queue=None):
        threading.Thread.__init__(self)

        self.id = ID
        self.phase = phase
        self.pc = 0
        self.parameter_modes = 0
        self.program = program.copy()
        self.output = None
        if arg1:
            program[1] = arg1
        if arg2:
            program[2] = arg2
        self.phase_set = False
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        self.runProgram()

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

    def runProgram(self):
        self.pc = 0
        while True:
            try:
                opcode = self.getOpcode()
            except Exception:
                return 0
            if opcode in [1, 2, 7, 8]:  # 3 operand instructions
                op1 = self.getOperand(0)
                op2 = self.getOperand(1)
                op3 = self.getOperand(2)
                if opcode == 1:  # Addition
                    try:
                        op3.setValue(op1.getValue() + op2.getValue())
                    except Exception:
                        return -1
                elif opcode == 2:  # Multiplication
                    try:
                        op3.setValue(op1.getValue() * op2.getValue())
                    except Exction:
                        return -1
                elif opcode == 7:  # Less than
                    if op1.getValue() < op2.getValue():
                        op3.setValue(1)
                    else:
                        op3.setValue(0)
                elif opcode == 8:  # Equals
                    if op1.getValue() == op2.getValue():
                        op3.setValue(1)
                    else:
                        op3.setValue(0)
                self.pc += 4
            elif opcode in [5, 6]:  # 2 operand instructions
                op1 = self.getOperand(0)
                op2 = self.getOperand(1)
                if opcode == 5:  # Jump-if-true, if op1 non-zere set pc to op2 value
                    if op1.getValue():
                        self.pc = op2.getValue()
                    else:
                        self.pc += 3
                elif opcode == 6:  # Jump-if-false if op1 is zero set pc to op2 value
                    if not op1.getValue():
                        self.pc = op2.getValue()
                    else:
                        self.pc += 3
            elif opcode in [3, 4]:  # 1 operand instructions
                if opcode == 3:  # Input
                    op1 = self.getOperand(0, override_mode=parameterMode.POSITION_MODE)
                    if not self.phase_set:
                        op1.setValue(self.phase)
                        self.phase_set = True
                    else:
                        if self.input_queue:
                            inp = int(self.input_queue.get(block=True))
                            op1.setValue(inp)
                        else:
                            op1.setValue(int(input("Input $> ")))
                elif opcode == 4:  # Output
                    op1 = self.getOperand(0)
                    if self.output_queue:
                        outp = op1.getValue()
                        self.output_queue.put(outp)
                    else:
                        print("Output @{} $> {}".format(self.pc, op1.getValue()))
                self.pc += 2
            elif opcode == 99:
                self.endProgram()
                break


def permutation(lst):

    if len(lst) == 0:
        return []

    if len(lst) == 1:
        return [lst]

    l = []

    for i in range(len(lst)):
        m = lst[i]

        remLst = lst[:i] + lst[i+1:]

        for p in permutation(remLst):
            l.append([m] + p)
    return l


program = get_program()


max_val = 0

phases = [5, 6, 7, 8, 9]
phases = permutation(phases)


for phase in phases:

    queue1 = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()
    queue5 = Queue()

    queue5.put(0)

    comp1 = intCodeComputer(1, phase[0], program, input_queue=queue5, output_queue=queue1)
    comp2 = intCodeComputer(2, phase[1], program, input_queue=queue1, output_queue=queue2)
    comp3 = intCodeComputer(3, phase[2], program, input_queue=queue2, output_queue=queue3)
    comp4 = intCodeComputer(4, phase[3], program, input_queue=queue3, output_queue=queue4)
    comp5 = intCodeComputer(5, phase[4], program, input_queue=queue4, output_queue=queue5)

    comp1.start()
    comp2.start()
    comp3.start()
    comp4.start()
    comp5.start()

    comp5.join()

    result = queue5.get(block=True)
    queue5.put(result)

    if result > max_val:
        max_val = result

print("Result: {}".format(max_val))
