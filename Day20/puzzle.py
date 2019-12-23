#!/bin/python

from enum import Enum
import copy
import curses.ascii as na
import time

class Coord:
    def __init__(self, x, y):

        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x, self.y)


class PortalMapping:
    def __init__(self, label, p1=None, p2=None):

        self.label = label
        self.p1 = p1
        self.p2 = p2


def isPortalChar(char):

    return na.isupper(char)


class Map:
    def __init__(self):

        self.start_loc = None
        self.end_loc = None
        self.cols = 0
        self.rows = 0
        self.portals = dict()
        self.grid = self._getInput()
        self.portal_count = len(self.portals.keys()) - 2

    def _getMapping(self, label):

        if label not in self.portals:
            self.portals[label] = PortalMapping(label=label)

        return self.portals[label]

    def _completeMapping(self, label, loc):

        portal = self._getMapping(label)

        if not portal.p1:
            portal.p1 = loc
        else:
            portal.p2 = loc

    def _getInput(self):
        ret = []
        for line in iter(input, ""):
            ret.append(list(line))

        self.cols = len(ret[0])
        self.rows = len(ret)

        self._parsePortals(ret)
        self._placePortalMappings(ret)
        return ret

    def _isOuterPortal(self, x, y):
        if x <= 2 or x >= (self.cols - 3) or y <= 2 or y >= (self.rows - 3):
            return True
        return False

    def _parsePortals(self, grid):
        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                if isPortalChar(char):
                    # Vertical portals
                    try:
                        if isPortalChar(grid[y + 1][x]):
                            label = grid[y][x] + grid[y + 1][x]
                            try:  # top/bottom middle
                                if grid[y + 2][x] in ['.', '#']:
                                    self._completeMapping(label=label,
                                                          loc=Coord(x, y + 2))
                                    if label == 'AA':
                                        self.start_loc = Coord(x, y + 2)
                                    elif label == 'ZZ':
                                        self.end_loc = Coord(x, y + 2)
                                    grid[y][x] = " "
                                    grid[y + 1][x] = " "
                            except Exception:
                                pass
                            try:
                                if grid[y - 1][x] in ['.', '#']:
                                    self._completeMapping(label=label,
                                                          loc=Coord(x, y - 1))
                                    if label == 'AA':
                                        self.start_loc = Coord(x, y - 1)
                                    elif label == 'ZZ':
                                        self.end_loc = Coord(x, y - 1)
                                    grid[y][x] = " "
                                    grid[y + 1][x] = " "
                            except Exception:
                                pass
                    except Exception as e:
                        pass
                    # Horizontal portals
                    try:
                        if isPortalChar(grid[y][x + 1]):
                            label = grid[y][x] + grid[y][x + 1]
                            try:  # Left sides
                                if grid[y][x + 2] in ['.', '#']:
                                    self._completeMapping(label=label,
                                                          loc=Coord(x + 2, y))
                                    if label == 'AA':
                                        self.start_loc = Coord(x + 2, y)
                                    elif label == 'ZZ':
                                        self.end_loc = Coord(x + 2, y)
                                    grid[y][x] = " "
                                    grid[y][x + 1] = " "
                            except Exception:
                                pass
                            try:
                                if grid[y][x - 1] in ['.', '#']:
                                    self._completeMapping(label=label,
                                                          loc=Coord(x - 1, y))
                                    if label == 'AA':
                                        self.start_loc = Coord(x - 1, y)
                                    elif label == 'ZZ':
                                        self.end_loc = Coord(x - 1, y)
                                    grid[y][x] = " "
                                    grid[y][x + 1] = " "
                            except Exception:
                                pass
                    except Exception as e:
                        print(e)
                        pass


    def _placePortalMappings(self, grid):

        grid[self.start_loc.y][self.start_loc.x] = 's'
        grid[self.end_loc.y][self.end_loc.x] = 'f'
        for label, mapping in self.portals.items():
            if not label in ['AA', 'ZZ']:
                grid[mapping.p1.y][mapping.p1.x] = "{},{},{}".format(label, mapping.p2.x, mapping.p2.y)
                grid[mapping.p2.y][mapping.p2.x] = "{},{},{}".format(label, mapping.p1.x, mapping.p1.y)

    def printGrid(self):

        print("\n".join([
            str(line) for line in list("".join(line2) for line2 in self.grid)
        ]))


class MOVE_DIR(Enum):

    UP = 1
    DOWN = 4
    LEFT = 2
    RIGHT = 3
    WARP = 6


class Moves:
    def __init__(self, initial_loc):

        self.pos = initial_loc
        self.moves = []
        self.warps = []
        self.level = 0


debug_no = 0


class MapCompleter:
    def __init__(self):

        self.map = Map()

        self.q = []

    def solve(self):
        global debug_no
        moves = Moves(self.map.start_loc)
        start_time = time.time()
        self.q = [moves]

        while not self._isAtFinish(moves):
            debug_no += 1

            try:
                moves = self.q.pop(0)
            except Exception as e:
                print(e)

            if debug_no == 116:
                print("wait here")

            for i in [
                    MOVE_DIR.UP, MOVE_DIR.DOWN, MOVE_DIR.LEFT, MOVE_DIR.RIGHT
            ]:
                put = copy.deepcopy(moves)
                if put.moves:
                    if self._isOpposite(put.moves[-1], i):
                        continue
                put.moves.append(i)
                if self._validMoves(put):
                    self.q.append(put)

        print("FINISHED in {}".format(time.time() - start_time))
        prev_portal = 'AA'
        prev_level = 0
        for move in moves.warps:
            print("{}->{} @ {}, Level: {}->{}, debug#: {}".format(prev_portal, move[0], move[2] - 1, prev_level, move[1], move[3]))
            prev_portal = move[0]
            prev_level = move[1]
        return len(moves.moves)

    def _isAtFinish(self, moves):

        if self.map.grid[moves.pos.y][moves.pos.x] == 'f' and moves.level == 0:
            return len(moves.moves)

        return 0

    def _getPortalLevelDelta(self, x, y, level):

        if self.map._isOuterPortal(x, y):
            if level == 0:
                return 0
            return -1
        return 1

    def _isPortal(self, loc):

        if 'A' <= loc[0] <= 'Z':
            return True
        return False

    def _validMoves(self, moves):
        global debug_no

        move = moves.moves[-1]

        if move == MOVE_DIR.UP:
            moves.pos.y -= 1
        elif move == MOVE_DIR.DOWN:
           moves.pos.y += 1
        elif move == MOVE_DIR.LEFT:
            moves.pos.x -= 1
        elif move == MOVE_DIR.RIGHT:
            moves.pos.x += 1

        loc = self.map.grid[moves.pos.y][moves.pos.x]

        if loc == ' ':
            return False

        if loc == '.' or loc == 'f' and moves.level == 0:
            return True

        if self._isPortal(loc):
            # Check portal can be used given current level
            outer = self._getPortalLevelDelta(moves.pos.x, moves.pos.y, moves.level)
            if outer:
                # Extra step needed
                moves.moves.append(MOVE_DIR.WARP)

                # Change position
                op = self.map.grid[moves.pos.y][moves.pos.x].split(",")
                moves.pos.x = int(op[1])
                moves.pos.y = int(op[2])

                # Increase or decrease level
                moves.level += outer

                if moves.level > self.map.portal_count:
                    return False

                # Bookkeeping
                moves.warps.append([op[0], moves.level, len(moves.moves), debug_no])
                return True


        return False

    def _isOpposite(self, one, two):

        return True if one.value + two.value == 5 else False


my_map = MapCompleter()
my_map.map.printGrid()
print("Req moves = {}".format(my_map.solve()))
