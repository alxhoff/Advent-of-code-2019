#! /bin/python
import threading
import copy
import math
import matplotlib.pyplot as plt
import hashlib
from queue import Queue
from enum import Enum


class parameterMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2


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
    def __init__(self, ID, program, phase=None, arg1=None, arg2=None, input_queue=None, output_queue=None, debug=False, exit_semaphore=None):
        threading.Thread.__init__(self)

        self.id = ID
        self.relative_base = 0
        self.phase = phase
        self.pc = 0
        self.parameter_modes = 0
        self.program = program.copy()
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
        self.exit_semaphore = exit_semaphore
        if self.exit_semaphore:
            self.exit_semaphore.acquire()

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
        self.exit_semaphore.release()

    def getOpValue(self, op):
        return op.getValue(self.relative_base)

    def setOpValue(self, op, value):
        return op.setValue(value, self.relative_base)

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
                        print("{}@{}: '{}[{}] + {}[{}]' -> [{}] <- {}".format(opcode, self.pc, op1_i, op1.getIndex(self.relative_base), op2_i, op2.getIndex(self.relative_base), op3.getIndex(self.relative_base), self.getOpValue(op3)))
                elif opcode == 2:  # Multiplication
                    res = op1_i * op2_i
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] * {}[{}]' -> [{}] <- {}".format(opcode, self.pc, op1_i, op1.getIndex(self.relative_base), op2_i, op2.getIndex(self.relative_base), op3.getIndex(self.relative_base), self.getOpValue(op3)))
                elif opcode == 7:  # Less than
                    if op1_i < op2_i:
                        res = 1
                    else:
                        res = 0
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] < {}[{}]' -> [{}] <- {}".format(opcode, self.pc, op1_i, op1.getIndex(self.relative_base), op2_i, op2.getIndex(self.relative_base), op3.getIndex(self.relative_base), self.getOpValue(op3)))
                elif opcode == 8:  # Equals
                    if self.getOpValue(op1) == self.getOpValue(op2):
                        res = 1
                    else:
                        res = 0
                    self.setOpValue(op3, res)
                    if self.debug >= 2:
                        print("{}@{}: '{}[{}] == {}[{}]' -> [{}] <- {}".format(opcode, self.pc, op1_i, op1.getIndex(self.relative_base), op2_i, op2.getIndex(self.relative_base), op3.getIndex(self.relative_base), self.getOpValue(op3)))
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
                        print("{}@{}: non-zero:'{}' @ [{}], pc {} -> {}".format(opcode, pc, res, op1.getIndex(self.relative_base), pc, self.pc))
                elif opcode == 6:  # Jump-if-false if op1 is zero set pc to op2 value
                    res = self.getOpValue(op1)
                    if not res:
                        self.pc = self.getOpValue(op2)
                    else:
                        self.pc += 3
                    if self.debug >= 2:
                        print("{}@{}: zero:'{}' @ [{}], pc {} -> {}".format(opcode, pc, res, op1.getIndex(self.relative_base), pc, self.pc))
            elif opcode in [3, 4, 9]:  # 1 operand instructions
                if opcode == 3:  # Input
                    op1 = self.getOperand(0)  # , override_mode=parameterMode.POSITION_MODE)
                    if not self.phase_set:
                        self.setOpValue(op1, self.phase)
                        self.phase_set = True
                    else:
                        if self.input_queue:
                            inp = int(self.input_queue.get(block=True))
                            if self.debug >= 1:
                                print("Got '{}' from intput queue".format(inp))
                        else:
                            inp = int(input("Input $> "))
                        self.setOpValue(op1, inp)
                        if self.debug >= 2:
                            print("{}@{}: Input '{}' -> [{}]".format(opcode, self.pc, inp, op1.getIndex(self.relative_base)))
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
                        print("{}@{}: Output from [{}]-> '{}'".format(opcode, self.pc, op1.getIndex(self.relative_base), outp))
                elif opcode == 9:
                    op1 = self.getOperand(0)
                    prev = self.relative_base
                    inc = self.getOpValue(op1)
                    self.relative_base += inc
                    if self.debug >= 2:
                        print("{}@{}: {} + {}@[{}] -> {}".format(opcode, self.pc, prev, inc, op1.getIndex(self.relative_base), self.relative_base))

                self.pc += 2
            elif opcode == 99:
                self.endProgram()
                break


class direction(Enum):

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __str__(self):
        return str(self.name)


class colour(Enum):

    BLACK = 0
    WHITE = 1

    def __str__(self):
        return str(self.name)


class coord:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def increamentX(self):
        self.x += 1

    def decrementX(self):
        self.x -= 1

    def increamentY(self):
        self.y += 1

    def decrementY(self):
        self.y -= 1


class shipPanel:

    def __init__(self, coords):
        self.coords = coords
        self.times_painted = 0
        self.colour = colour.BLACK

    def paint(self, colour):
        self.colour = colour
        self.times_painted += 1


class shipHull:

    def __init__(self):

        self.panels = dict()

    def _getKey(self, x, y):
        return hashlib.sha1(str([x, y]).encode()).hexdigest()

    def _getPanel(self, x, y):
        key = self._getKey(x, y)
        if key not in self.panels:
            self.panels[key] = shipPanel(coord(x, y))
        return self.panels[key]

    def getPanelColour(self, x, y):
        panel = self._getPanel(x, y)
        return panel.colour

    def paintPanel(self, x, y, colour):
        panel = self._getPanel(x, y)
        panel.paint(colour)

    def getPaintedPanelCount(self):
        ret = 0
        for key, panel in self.panels.items():
            if panel.times_painted:
                ret += 1
        return ret

    def drawHull(self):
        for key, value in self.panels.items():
            if value.colour == colour.WHITE:
                plt.scatter(value.coords.x, value.coords.y, s=50)

        plt.title("SpaceshipMcSpaceface")
        plt.show()


class robot:

    def __init__(self, program, debug=0):

        self.running = threading.Semaphore()
        self.input_q = Queue()
        self.output_q = Queue()
        self.intComp = intCodeComputer(1, program=program, input_queue=self.input_q, output_queue=self.output_q, exit_semaphore=self.running, debug=debug)
        self.intComp.start()
        self.position = coord(0, 0)
        self.ship_hull = shipHull()
        self.direction = direction.UP  # Assume robot faces up at begining
        self.debug = debug
        self.start_panel = True

    def _paintPanel(self, colour):
        self.ship_hull.paintPanel(self.position.x, self.position.y, colour)

    def _changeDirection(self, direction):

        if self.direction == direction.LEFT:
            if direction.value:  # right
                self.direction = direction.UP
            else:  # left
                self.direction = direction.DOWN

        elif self.direction == direction.RIGHT:
            if direction.value:
                self.direction = direction.DOWN
            else:
                self.direction = direction.UP

        elif self.direction == direction.UP:
            if direction.value:
                self.direction = direction.RIGHT
            else:
                self.direction = direction.LEFT

        elif self.direction == direction.DOWN:
            if direction.value:
                self.direction = direction.LEFT
            else:
                self.direction = direction.RIGHT

    def _move(self, direction):

        self._changeDirection(direction)

        if self.direction == direction.LEFT:
            self.position.decrementX()

        elif self.direction == direction.RIGHT:
            self.position.increamentX()

        elif self.direction == direction.UP:
            self.position.increamentY()

        elif self.direction == direction.DOWN:
            self.position.decrementY()

    def _getCurrentPanelColour(self):
        return self.ship_hull.getPanelColour(self.position.x, self.position.y)

    def _paintCurrentPanel(self, colour):
        self.ship_hull.paintPanel(self.position.x, self.position.y, colour)

    def showHull(self):
        self.ship_hull.drawHull()

    def getPaintedPanelCount(self):
        return self.ship_hull.getPaintedPanelCount()

    def paint(self):
        while True:
            if self.running.acquire(blocking=False):
                return

            current_panel_colour = self._getCurrentPanelColour()
            if self.start_panel:
                self._paintCurrentPanel(colour.WHITE)
                current_panel_colour = colour.WHITE

            # Put into input queue for intCode comp and wait for output
            self.input_q.put(int(current_panel_colour.value))

            colour_to_paint_panel = colour(self.output_q.get(block=True))
            direction_to_move = direction(self.output_q.get(block=True))

            # Paint panel
            prev_pos = copy.copy(self.position)
            prev_facing = self.direction
            self._paintCurrentPanel(colour_to_paint_panel)
            self._move(direction_to_move)
            if self.intComp.debug >= 1:
                print("{} -> {}, moved {} from ({},{}) -> ({},{}), facing {} -> {}".format(str(current_panel_colour), str(colour_to_paint_panel), str(direction_to_move), prev_pos.x, prev_pos.y, self.position.x, self.position.y, prev_facing, self.direction))


program = get_program()
hull_robot = robot(program)
hull_robot.paint()
print("Panels painted = {}".format(hull_robot.getPaintedPanelCount()))
hull_robot.showHull()
exit(0)
