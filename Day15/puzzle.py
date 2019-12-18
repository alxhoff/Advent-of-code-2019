#!/bin/python

import queue
from intCodeComp import intCodeComputer
import numpy as np
from enum import Enum
import hashlib
from functools import reduce
import pygame

pygame.init()

program = "3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1001,1034,0,1039,102,1,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,102,1,1038,1043,1001,1037,0,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1001,1035,0,1040,102,1,1038,1043,1001,1037,0,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,9,1032,1006,1032,165,1008,1040,5,1032,1006,1032,165,1101,0,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,40,1044,1106,0,224,1101,0,0,1044,1106,0,224,1006,1044,247,102,1,1039,1034,101,0,1040,1035,101,0,1041,1036,1001,1043,0,1038,1001,1042,0,1037,4,1044,1106,0,0,26,29,83,66,1,36,14,44,33,12,3,15,20,56,9,35,51,55,6,20,13,71,15,23,94,38,45,15,47,30,89,39,11,55,5,9,47,29,41,36,78,12,4,65,48,66,36,94,76,30,63,41,32,1,73,1,35,65,87,46,18,90,11,44,30,73,87,8,38,46,17,78,51,34,19,53,37,26,20,24,46,64,17,6,26,41,10,62,14,88,23,94,13,55,5,45,10,39,83,99,32,34,72,30,58,33,71,47,21,38,97,38,46,41,18,39,37,8,86,55,35,4,92,19,21,53,61,6,55,69,16,85,62,26,63,17,80,33,10,53,91,2,37,94,37,93,7,97,18,55,54,36,17,62,89,12,92,32,69,4,46,47,19,89,25,12,51,91,9,1,71,35,56,39,98,48,7,49,24,95,15,45,2,1,93,82,19,7,11,70,30,64,28,27,58,4,39,30,94,72,33,43,90,98,26,32,70,1,81,25,35,47,17,31,92,15,73,13,27,72,65,30,67,2,22,89,77,30,47,12,58,26,79,22,37,74,41,3,42,30,39,67,24,18,62,98,19,59,95,25,6,67,42,35,85,51,48,7,63,17,67,53,45,13,25,43,1,54,4,65,55,20,73,32,70,1,33,39,93,88,19,35,56,21,13,53,73,31,21,44,73,31,13,69,30,42,26,51,25,90,16,49,9,93,50,28,60,24,18,61,23,11,98,19,45,77,12,61,31,3,66,56,4,77,24,59,87,31,38,65,67,7,9,23,71,9,59,35,55,83,22,12,94,17,67,87,96,63,8,29,32,34,15,55,39,60,41,74,39,81,47,51,25,26,57,28,18,60,84,20,16,66,42,14,25,16,94,2,22,74,85,19,63,32,9,19,11,91,44,34,21,1,56,12,87,8,52,18,56,7,90,5,86,81,24,98,21,9,80,59,68,10,80,53,18,75,50,9,14,43,26,29,57,86,39,41,93,3,69,55,16,84,15,22,84,30,72,19,13,15,19,80,97,79,32,68,77,82,30,19,4,71,45,67,14,95,17,54,80,88,25,13,80,41,37,96,15,28,26,33,73,32,45,79,21,52,23,98,82,21,16,13,64,32,39,93,17,33,95,61,36,12,21,3,84,4,88,22,26,59,80,27,82,2,85,79,29,33,52,17,23,95,8,64,16,56,23,42,43,18,41,11,9,84,42,62,4,67,17,98,76,99,1,16,72,72,10,79,19,76,4,54,9,99,34,33,7,97,85,19,76,93,38,6,90,37,90,2,83,61,19,43,39,2,91,17,60,21,79,2,32,94,38,32,7,64,8,14,7,68,23,28,75,24,73,50,29,63,22,89,4,51,66,2,7,33,82,13,23,84,81,23,55,68,15,27,9,97,27,79,42,86,75,56,13,95,74,5,88,25,44,99,33,14,24,29,21,78,4,15,75,32,92,74,11,56,24,57,10,28,73,8,10,90,77,30,96,8,60,3,71,20,41,9,33,89,38,74,95,4,95,35,13,18,55,10,81,9,60,17,67,7,34,48,48,15,54,79,37,66,43,22,64,28,28,4,91,5,9,92,30,64,37,98,66,15,92,2,3,25,70,25,33,61,56,25,70,58,30,41,97,18,54,10,49,45,3,1,30,57,30,46,8,55,79,39,58,46,35,19,38,80,86,4,36,75,29,62,39,71,2,41,6,66,36,99,21,61,39,72,3,48,29,43,31,59,84,71,12,52,61,82,11,56,23,51,30,60,88,65,35,48,24,58,76,49,93,51,33,72,0,0,21,21,1,10,1,0,0,0,0,0,0"


class DROID_RESPONSE(Enum):

    HIT_WALL = 0
    MOVED = 1
    AT_OXY = 2


class DIRECTION(Enum):

    NONE = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def __str__(self):
        return str(self.name)


class BLOCKS(Enum):

    WALL = 1
    NOT_WALL = 2
    OXYGEN_SYS = 3
    START = 4


class TURN(Enum):

    LEFT = 1
    RIGHT = 2


class Block:
    def __init__(self, x, y, btype):

        self.position = coord(x, y)
        self.btype = btype


class coord:
    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y

    def incrementX(self):

        self.x += 1

    def decrementX(self):

        self.x -= 1

    def incrementY(self):

        self.y += 1

    def decrementY(self):

        self.y -= 1


class MazeSolver:
    def __init__(self, maze, start_pos=[0, 0]):

        self.maze = maze
        self.q = queue.Queue()
        self.start_pos = start_pos
        self.max_moves = 0

    def solve(self):

        self._solve()

    def findLongest(self):

        return self._solveLen()

    def _isValid(self, x, y):

        loc = self.maze[x][y]
        if loc == '.' or loc == 'S' or loc == 'O':
            return True

        return False

    def _validMove(self, x, y, direction):

        if direction == DIRECTION.NORTH:
            return self._isValid(x, y - 1)
        elif direction == DIRECTION.SOUTH:
            return self._isValid(x, y + 1)
        elif direction == DIRECTION.WEST:
            return self._isValid(x - 1, y)
        elif direction == DIRECTION.EAST:
            return self._isValid(x + 1, y)

        return False

    def _validMoves(self, moves):

        pos = self.start_pos.copy()

        for move in moves:
            if self._validMove(pos[0], pos[1], move):
                if move == DIRECTION.NORTH:
                    pos[1] -= 1
                elif move == DIRECTION.SOUTH:
                    pos[1] += 1
                elif move == DIRECTION.EAST:
                    pos[0] += 1
                elif move == DIRECTION.WEST:
                    pos[0] -= 1
            else:
                return False

        return True

    def _movesToEnd(self, moves, finish):

        pos = self.start_pos.copy()
        for move in moves:
            if move == DIRECTION.NORTH:
                pos[1] -= 1
            elif move == DIRECTION.SOUTH:
                pos[1] += 1
            elif move == DIRECTION.EAST:
                pos[0] += 1
            elif move == DIRECTION.WEST:
                pos[0] -= 1

        if any(finish):
            if pos[0] == finish[0] and pos[1] == finish[1]:
                print("Path found to {},{} in {} moves".format(
                    finish[0], finish[1], len(moves)))
                return len(moves)
        else:
            if self.maze[pos[0]][pos[1]] == 'O':
                print("Path found in {} moves: {}".format(len(moves), moves))
                return len(moves)

        return 0

    def _isOpposite(self, move, next_move):

        if next_move == DIRECTION.NORTH:
            if move == DIRECTION.SOUTH:
                return True
        elif next_move == DIRECTION.SOUTH:
            if move == DIRECTION.NORTH:
                return True
        elif next_move == DIRECTION.EAST:
            if move == DIRECTION.WEST:
                return True
        elif next_move == DIRECTION.WEST:
            if move == DIRECTION.EAST:
                return True

    def _solve(self, finish=[]):
        # reset
        moves = []

        while not self.q.empty():
            self.q.get()
        self.q.put(moves)

        while not self._movesToEnd(moves, finish):
            moves = self.q.get()

            for i in [
                    DIRECTION.NORTH, DIRECTION.SOUTH, DIRECTION.EAST,
                    DIRECTION.WEST
            ]:
                put = moves.copy()
                if put:
                    if self._isOpposite(put[-1], i):
                        continue
                put.append(i)
                if self._validMoves(put):
                    self.q.put(put)
        return len(moves)

    def _solveLen(self, finish=[]):
        # reset
        moves = []

        while not self.q.empty():
            self.q.get()
        self.q.put(moves)

        while not self.q.empty():
            moves = self.q.get()

            for i in [
                    DIRECTION.NORTH, DIRECTION.SOUTH, DIRECTION.EAST,
                    DIRECTION.WEST
            ]:
                put = moves.copy()
                if put:
                    if self._isOpposite(put[-1], i):
                        continue
                put.append(i)
                if self._validMoves(put):
                    self.q.put(put)
        return len(moves)


class RepairDroid:
    def __init__(self):

        self.iq = queue.Queue()
        self.oq = queue.Queue()
        self.ic = intCodeComputer(input_queue=self.iq,
                                  output_queue=self.oq,
                                  program_str=program)
        self.ic.start()
        self.map = dict()
        self.position = coord()
        self.direction_traveling = DIRECTION.NORTH
        self._setMap(self.position.x, self.position.y, BLOCKS.START)
        self.oxygen_loc = [0, 0]
        self.win = pygame.display.set_mode((900, 900))
        self.block_size = 22

    def _generateGrid(self):

        points = self._getPoints()

        x_size = self._getXSize(points)
        y_size = self._getYSize(points)

        ret = np.full((x_size, y_size), '#')

        for point in points:
            if point.btype == BLOCKS.NOT_WALL:
                ret[point.position.x][point.position.y] = '.'
            elif point.btype == BLOCKS.START:
                ret[point.position.x][point.position.y] = 'S'
            elif point.btype == BLOCKS.OXYGEN_SYS:
                ret[point.position.x][point.position.y] = 'O'

        return ret

    def _getXSize(self, points):

        return self._getMaxX(points) - self._getMinX(points) + 1

    def _getYSize(self, points):

        return self._getMaxY(points) - self._getMinY(points) + 1

    def _getMaxX(self, points):

        return max(points, key=lambda a: a.position.x).position.x

    def _getMinX(self, points):

        return min(points, key=lambda a: a.position.x).position.x

    def _getMaxY(self, points):

        return max(points, key=lambda a: a.position.y).position.y

    def _getMinY(self, points):

        return min(points, key=lambda a: a.position.y).position.y

    def _getPoints(self):

        points = []

        for key, value in self.map.items():
            points.append(value)

        return points

    def _printMap(self):

        points = self._getPoints()

        if points:

            min_x = self._getMinX(points)
            min_y = self._getMinY(points)

            self.win.fill((0, 0, 0))

            pygame.draw.rect(self.win, (0, 0, 255),
                             ((self.position.x - min_x) * self.block_size,
                              (self.position.y - min_y) * self.block_size,
                              self.block_size, self.block_size))

            for point in points:
                if point.btype == BLOCKS.NOT_WALL:
                    pygame.draw.rect(
                        self.win, (255, 0, 0),
                        ((point.position.x - min_x) * self.block_size,
                         (point.position.y - min_y) * self.block_size,
                         self.block_size, self.block_size))
                elif point.btype == BLOCKS.WALL:
                    pygame.draw.rect(
                        self.win, (0, 255, 0),
                        ((point.position.x - min_x) * self.block_size,
                         (point.position.y - min_y) * self.block_size,
                         self.block_size, self.block_size))
                elif point.btype == BLOCKS.OXYGEN_SYS:
                    pygame.draw.rect(
                        self.win, (0, 255, 255),
                        ((point.position.x - min_x) * self.block_size,
                         (point.position.y - min_y) * self.block_size,
                         self.block_size, self.block_size))
                elif point.btype == BLOCKS.START:
                    pygame.draw.rect(
                        self.win, (255, 255, 0),
                        ((point.position.x - min_x) * self.block_size,
                         (point.position.y - min_y) * self.block_size,
                         self.block_size, self.block_size))

            pygame.display.update()

    def _setMap(self, x, y, block):

        self.map[self._getKey(x, y)] = Block(x, y, block)

    def _getMap(self, x, y):

        return self.map[self._getKey(x, y)]

    def _alreadyBeen(self, x, y):

        key = self._getKey(x, y)
        if key in self.map:
            if self.map[key].btype == BLOCKS.WALL:
                return True

        return False

    def _getKey(self, x, y):
        return hashlib.sha1(str([x, y]).encode()).hexdigest()

    def _turnRobot(self, direction):

        if self.direction_traveling == DIRECTION.NORTH:
            if direction == TURN.LEFT:
                self.direction_traveling = DIRECTION.WEST
            else:
                self.direction_traveling = DIRECTION.EAST
        elif self.direction_traveling == DIRECTION.SOUTH:
            if direction == TURN.LEFT:
                self.direction_traveling = DIRECTION.EAST
            else:
                self.direction_traveling = DIRECTION.WEST
        elif self.direction_traveling == DIRECTION.EAST:
            if direction == TURN.LEFT:
                self.direction_traveling = DIRECTION.NORTH
            else:
                self.direction_traveling = DIRECTION.SOUTH
        elif self.direction_traveling == DIRECTION.WEST:
            if direction == TURN.LEFT:
                self.direction_traveling = DIRECTION.SOUTH
            else:
                self.direction_traveling = DIRECTION.NORTH

    def _sendMovement(self, direction):

        #  print("Send direction: {}".format(direction.value))
        self.iq.put(direction.value)

    def _getResponse(self):

        ret = self.oq.get(block=True)
        #  print("Got response: {}".format(ret))
        return ret

    def _solve(self):
        grid = self._generateGrid()

        ms = MazeSolver(grid)
        ms.solve()

        longest = MazeSolver(grid, self.oxygen_loc)
        print("Longest: {}".format(longest.findLongest()))

    def _finish(self):
        self._printMap()
        self._solve()
        # TODO
        exit(0)

    def _normalizePoint(self, point):
        points = self._getPoints()
        return [
            point[0] - self._getMinX(points), point[1] - self._getMinX(points)
        ]

    # Moves in the direction the robot is facing, records block information depending on response and returns
    # True if the robot was able to move
    def _moveRobot(self):

        self._sendMovement(self.direction_traveling)

        response = DROID_RESPONSE(self._getResponse())

        if response == DROID_RESPONSE.MOVED or response == DROID_RESPONSE.AT_OXY:
            #  if self._alreadyBeen(self.position.x, self.position.y):
            #      print("wait here")

            if self.direction_traveling == DIRECTION.NORTH:
                self.position.incrementY()
            elif self.direction_traveling == DIRECTION.SOUTH:
                self.position.decrementY()
            elif self.direction_traveling == DIRECTION.EAST:
                self.position.incrementX()
            elif self.direction_traveling == DIRECTION.WEST:
                self.position.decrementX()

            self._setMap(self.position.x, self.position.y, BLOCKS.NOT_WALL)

            if response == DROID_RESPONSE.AT_OXY:
                self._setMap(self.position.x, self.position.y,
                             BLOCKS.OXYGEN_SYS)
                self.oxygen_loc = [self.position.x, self.position.y]
                print("Found oxygen @ {}, {}".format(self.oxygen_loc[0],
                                                     self.oxygen_loc[1]))
                # return DROID_RESPONSE.AT_OXY

            return DROID_RESPONSE.MOVED

        elif DROID_RESPONSE.HIT_WALL:
            if self.direction_traveling == DIRECTION.NORTH:
                self._setMap(self.position.x, self.position.y + 1, BLOCKS.WALL)
            elif self.direction_traveling == DIRECTION.SOUTH:
                self._setMap(self.position.x, self.position.y - 1, BLOCKS.WALL)
            elif self.direction_traveling == DIRECTION.EAST:
                self._setMap(self.position.x + 1, self.position.y, BLOCKS.WALL)
            elif self.direction_traveling == DIRECTION.WEST:
                self._setMap(self.position.x - 1, self.position.y, BLOCKS.WALL)

            return DROID_RESPONSE.HIT_WALL

    def _walkRobot(self):

        # Algorithm
        # If at the end:
        #   Finished
        # Else:
        #   There an empty space to the left:
        #       Rotate left and start algorithm again
        #   Else:
        #       There a wall in front:
        #           Rotate right and start algorithm again
        #       Else:
        #           Move forward and start algorithm again
        self._printMap()
        # print("Robot @ {}, {}, facing: {}".format(
        #     self.position.x, self.position.y, str(self.direction_traveling)))
        self._turnRobot(TURN.LEFT)
        mv = self._moveRobot()
        if mv == DROID_RESPONSE.HIT_WALL:  # Was not able to move to the left
            self._turnRobot(TURN.RIGHT)  # Turn back to straight
            mv = self._moveRobot()
            if mv == DROID_RESPONSE.HIT_WALL:  # Could not go straight
                self._turnRobot(TURN.RIGHT)
        # elif mv == DROID_RESPONSE.MOVED:
        #     print("Wait here")
        if mv == DROID_RESPONSE.MOVED and self.position.x == 0 and self.position.y == 0:
            print("Back to start")
            return True
        return False

    def run(self):

        while not self._walkRobot():
            pass

        self._finish()


robo = RepairDroid()
robo.run()
