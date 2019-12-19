#! /bin/python
import threading
from enum import Enum


class parameterMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2


class parameter:
    def __init__(self,
                 program,
                 position,
                 value,
                 mode=parameterMode.POSITION_MODE):

        self.program = program
        self.position = position
        self.value = value
        self.mode = mode

    def checkIndex(self, index):
        if index >= len(self.program):
            for i in range(index - len(self.program) + 1):
                self.program.append(0)

    def getIndex(self, relative_base=None):
        if self.mode == parameterMode.POSITION_MODE.value:
            self.checkIndex(self.value)
            return self.value
        elif self.mode == parameterMode.IMMEDIATE_MODE.value:
            self.checkIndex(self.position)
            return self.position
        elif self.mode == parameterMode.RELATIVE_MODE.value:
            if not relative_base:
                raise Exception("Relative base not given")
            self.checkIndex(relative_base + self.value)
            return relative_base + self.value

    def getValue(self, relative_base=None):
        if self.mode == parameterMode.POSITION_MODE.value:
            self.checkIndex(self.value)
            return self.program[self.value]
        elif self.mode == parameterMode.IMMEDIATE_MODE.value:
            self.checkIndex(self.position)
            return self.program[self.position]
        elif self.mode == parameterMode.RELATIVE_MODE.value:
            if not relative_base:
                raise Exception("Relative base not given")
            self.checkIndex(relative_base + self.value)
            return self.program[relative_base + self.value]

    def setValue(self, value, relative_base=None):
        if self.mode == parameterMode.POSITION_MODE.value:
            self.checkIndex(self.value)
            self.program[self.value] = value
        elif self.mode == parameterMode.IMMEDIATE_MODE.value:
            self.checkIndex(self.position)
            self.program[self.position] = value
        elif self.mode == parameterMode.RELATIVE_MODE.value:
            if not relative_base:
                raise Exception("Relative base not given")
            self.checkIndex(relative_base + self.value)
            self.program[relative_base + self.value] = value


class intCodeComputer(threading.Thread):
    def __init__(self,
                 ID=0,
                 program=None,
                 program_str=None,
                 phase=None,
                 arg1=None,
                 arg2=None,
                 input_queue=None,
                 output_queue=None,
                 debug=0,
                 exit_semaphore=None):
        threading.Thread.__init__(self)

        self.exit_semaphore = exit_semaphore
        if self.exit_semaphore:
            self.exit_semaphore.acquire()

        self.id = ID
        self.relative_base = 0
        self.phase = phase
        self.pc = 0
        self.parameter_modes = 0
        if program:
            self.program = program
        else:
            if program_str:
                self.program = self.get_program(str_input=program_str)
            else:
                self.program = self.get_program()
        self.initial_program = self.program.copy()
        self.output = None
        if arg1:
            program[1] = arg1
        if arg2:
            program[2] = arg2
        if self.phase:
            self.phase_set = False
        else:
            self.phase_set = True
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.debug = debug

    def get_program(self, str_input=None):

        if not str_input:
            program = input("Program $> ").split(",")
        else:
            program = str_input.split(",")

        for entry in range(len(program)):
            program[entry] = int(program[entry])

        return program

    def patchProgram(self, location, value):
        self.program[location] = value

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
            return parameter(program=self.program,
                             position=position,
                             value=self.program[position],
                             mode=override_mode.value)
        else:
            return parameter(program=self.program,
                             position=position,
                             value=self.program[position],
                             mode=self.getSingleParameterMode(n))

    def printState(self):
        print("pc: {}".format(self.pc))

    def printProgram(self):
        print(self.program)

    def endProgram(self):
        self.output = self.program[0]
        if self.output_queue:
            self.output_queue.put(self.output)
        if self.exit_semaphore:
            self.exit_semaphore.release()

    def getOpValue(self, op):
        return op.getValue(self.relative_base)

    def setOpValue(self, op, value):
        return op.setValue(value, self.relative_base)

    def runInitialProgram(self):
        self.program = self.initial_program.copy()
        self.runProgram()

    def runProgram(self):
        self.pc = 0
        while True:
            opcode = self.getOpcode()
            if opcode in [1, 2, 7, 8]:  # 3 operand instructions
                op1 = self.getOperand(0)
                op2 = self.getOperand(1)
                op3 = self.getOperand(2)
                op1_i = self.getOpValue(op1)
                op2_i = self.getOpValue(op2)
                if opcode == 1:  # Addition
                    res = op1_i + op2_i
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] + {}[{}]' -> [{}] <- {}".format(
                            opcode, self.pc, op1_i,
                            op1.getIndex(self.relative_base), op2_i,
                            op2.getIndex(self.relative_base),
                            op3.getIndex(self.relative_base),
                            self.getOpValue(op3)))
                elif opcode == 2:  # Multiplication
                    res = op1_i * op2_i
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] * {}[{}]' -> [{}] <- {}".format(
                            opcode, self.pc, op1_i,
                            op1.getIndex(self.relative_base), op2_i,
                            op2.getIndex(self.relative_base),
                            op3.getIndex(self.relative_base),
                            self.getOpValue(op3)))
                elif opcode == 7:  # Less than
                    if op1_i < op2_i:
                        res = 1
                    else:
                        res = 0
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] < {}[{}]' -> [{}] <- {}".format(
                            opcode, self.pc, op1_i,
                            op1.getIndex(self.relative_base), op2_i,
                            op2.getIndex(self.relative_base),
                            op3.getIndex(self.relative_base),
                            self.getOpValue(op3)))
                elif opcode == 8:  # Equals
                    if self.getOpValue(op1) == self.getOpValue(op2):
                        res = 1
                    else:
                        res = 0
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] == {}[{}]' -> [{}] <- {}".format(
                            opcode, self.pc, op1_i,
                            op1.getIndex(self.relative_base), op2_i,
                            op2.getIndex(self.relative_base),
                            op3.getIndex(self.relative_base),
                            self.getOpValue(op3)))
                self.pc += 4
            elif opcode in [5, 6]:  # 2 operand instructions
                op1 = self.getOperand(0)
                op2 = self.getOperand(1)
                pc = self.pc
                if opcode == 5:  # Jump-if-true, if op1 non-zero set pc to op2 value
                    res = self.getOpValue(op1)
                    if res:
                        self.pc = self.getOpValue(op2)
                    else:
                        self.pc += 3
                    if self.debug >= 2:
                        print(
                            "{}@{}: non-zero:'{}' @ [{}], pc {} -> {}".format(
                                opcode, pc, res,
                                op1.getIndex(self.relative_base), pc, self.pc))
                elif opcode == 6:  # Jump-if-false if op1 is zero set pc to op2 value
                    res = self.getOpValue(op1)
                    if not res:
                        self.pc = self.getOpValue(op2)
                    else:
                        self.pc += 3
                    if self.debug >= 2:
                        print("{}@{}: zero:'{}' @ [{}], pc {} -> {}".format(
                            opcode, pc, res, op1.getIndex(self.relative_base),
                            pc, self.pc))
            elif opcode in [3, 4, 9]:  # 1 operand instructions
                if opcode == 3:  # Input
                    op1 = self.getOperand(
                        0)  # , override_mode=parameterMode.POSITION_MODE)
                    if not self.phase_set:
                        self.setOpValue(op1, self.phase)
                        self.phase_set = True
                    else:
                        if self.input_queue:
                            if self.debug >= 1:
                                print("Waiting for input from queue")
                            inp = int(self.input_queue.get(block=True))
                            if self.debug >= 1:
                                print("Got '{}' from intput queue".format(inp))
                        else:
                            inp = int(input("Input $> "))
                        self.setOpValue(op1, inp)
                        if self.debug >= 2:
                            print("{}@{}: Input '{}' -> [{}]".format(
                                opcode, self.pc, inp,
                                op1.getIndex(self.relative_base)))
                elif opcode == 4:  # Output
                    op1 = self.getOperand(0)
                    outp = self.getOpValue(op1)
                    if self.output_queue:
                        self.output_queue.put(outp)
                        if self.debug >= 1:
                            print("Put '{}' into output queue".format(outp))
                    else:
                        print("Output @{} $> {}".format(self.pc, outp))
                    if self.debug >= 2:
                        print("{}@{}: Output from [{}]-> '{}'".format(
                            opcode, self.pc, op1.getIndex(self.relative_base),
                            outp))
                elif opcode == 9:
                    op1 = self.getOperand(0)
                    prev = self.relative_base
                    inc = self.getOpValue(op1)
                    self.relative_base += inc
                    if self.debug >= 2:
                        print("{}@{}: {} + {}@[{}] -> {}".format(
                            opcode, self.pc, prev, inc,
                            op1.getIndex(self.relative_base),
                            self.relative_base))

                self.pc += 2
            elif opcode == 99:
                self.endProgram()
                break
