#!/bin/python

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

debug_no = 0

class MapCompleter:
    def __init__(self):

        self.map = Map()
        self.q = []

    def solve(self):
        global debug_no
        start_time = time.time()

        seen_moves = []
        start_pos = [self.map.start_loc.x , self.map.start_loc.y]
        start_level = 0
        start_move_count = 0
        # warps = []
        # self.q = [[start_pos, start_level, start_move_count, warps]]
        self.q = [[start_pos, start_level, start_move_count]]

        while len(self.q):

            # pos, level, move_cnt, warps = self.q.pop(0)
            pos, level, move_cnt = self.q.pop(0)

            if self._isAtFinish(pos[0], pos[1], level):
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                debug_no += 1

                new_pos = (pos[0] + dx, pos[1] + dy)
                new_level = level

                if self.map.grid[new_pos[1]][new_pos[0]] == '#':
                    continue

                if (new_pos, new_level) in seen_moves:
                    continue
                seen_moves.append((new_pos, new_level))

                # Standard move
                if self.map.grid[new_pos[1]][new_pos[0]] in ['.', 'f']:
                    # self.q.append((new_pos, new_level, move_cnt + 1, warps.copy()))
                    self.q.append((new_pos, new_level, move_cnt + 1))

                # Portal
                label = self._isPortal(new_pos)
                if label:
                    level_change = self._getPortalLevelDelta(new_pos[0], new_pos[1], new_level)
                    if level_change:
                        # Change position
                        op = self.map.grid[new_pos[1]][new_pos[0]].split(",")
                        new_pos = (int(op[1]), int(op[2]))
                        # Increase or decrease level
                        new_level += level_change
                        if new_level > self.map.portal_count:
                            continue
                        # if (new_pos, new_level) in seen_moves:
                        #     continue
                        # seen_moves.append((new_pos, new_level))

                        # Track warp
                        # warps.append((label, new_level, debug_no))
                        # self.q.append((new_pos, new_level, move_cnt + 2, warps.copy()))
                        self.q.append((new_pos, new_level, move_cnt + 2))

        print("FINISHED in {}".format(time.time() - start_time))
        # prev_portal = 'AA'
        # prev_level = 0
        # for move in warps:
        #     print("{}->{}, level {}->{} @ {}".format(prev_portal, move[0], prev_level, move[1], move[2]))
        #     prev_portal = move[0]
        #     prev_level = move[1]
        return move_cnt

    def _isAtFinish(self, x, y, level):

        if self.map.grid[y][x] == 'f' and level == 0:
            return True

        return False

    def _getPortalLevelDelta(self, x, y, level):

        if self.map._isOuterPortal(x, y):
            if level == 0:
                return 0
            return -1
        return 1

    def _isPortal(self, pos):

        if 'A' <= self.map.grid[pos[1]][pos[0]][0] <= 'Z':
            return self.map.grid[pos[1]][pos[0]][0:2]
        return None

my_map = MapCompleter()
my_map.map.printGrid()
print("Req moves = {}".format(my_map.solve()))
