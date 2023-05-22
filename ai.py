# import model
# import pickle
# from time import perf_counter_ns
#
# NANO_TO_SEC = 1000000000
# INF = 100000
# groups = []
# patternDbDict = []
#
#
# def init(boardSize):
#     global groups
#     global patternDbDict
#     print("Initializing pattern DB...")
#     with open("patternDb_"+str(boardSize)+".dat", "rb") as patternDbFile:
#         groups = pickle.load(patternDbFile)
#         patternDbDict = pickle.load(patternDbFile)
#         for i in range(len(patternDbDict)):
#             print("Group {}: {}, {:,} entries.".format(
#                 i, groups[i], len(patternDbDict[i])))
#
#
# def idaStar(puzzle):
#     if puzzle.checkWin():
#         return []
#     if not patternDbDict:
#         init(puzzle.boardSize)
#
#     t1 = perf_counter_ns()
#     bound = hScore(puzzle)
#     path = [puzzle]
#     dirs = []
#     while True:
#         rem = search(path, 0, bound, dirs)
#         if rem == True:
#             tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
#             print("Took {} seconds to find a solution of {} moves".format(
#                 tDelta, len(dirs)))
#             return dirs
#         elif rem == INF:
#             return None
#         bound = rem
#
#
# def search(path, g, bound, dirs):
#     cur = path[-1]
#     f = g + hScore(cur)
#
#     if f > bound:
#         return f
#
#     if cur.checkWin():
#         return True
#     min = INF
#
#     for dir in cur.DIRECTIONS:
#         if dirs and (-dir[0], -dir[1]) == dirs[-1]:
#             continue
#         validMove, simPuzzle = cur.simulateMove(dir)
#
#         if not validMove or simPuzzle in path:
#             continue
#
#         path.append(simPuzzle)
#         dirs.append(dir)
#
#         t = search(path, g + 1, bound, dirs)
#         if t == True:
#             return True
#         if t < min:
#             min = t
#
#         path.pop()
#         dirs.pop()
#
#     return min
#
#
# def hScore(puzzle):
#     h = 0
#     for g in range(len(groups)):
#         group = groups[g]
#         hashString = puzzle.hash(group)
#         if hashString in patternDbDict[g]:
#             h += patternDbDict[g][hashString]
#         else:
#             print("No pattern found in DB, using manhattan dist")
#             for i in range(puzzle.boardSize):
#                 for j in range(puzzle.boardSize):
#                     if puzzle[i][j] != 0 and puzzle[i][j] in group:
#                         destPos = ((puzzle[i][j] - 1) // puzzle.boardSize,
#                                    (puzzle[i][j] - 1) % puzzle.boardSize)
#                         h += abs(destPos[0] - i)
#                         h += abs(destPos[1] - j)
#
#     return h

import pickle
from time import perf_counter_ns


class PuzzleSolver:
    def __init__(self, board_size):
        self.NANO_TO_SEC = 1000000000
        self.INF = 100000
        self.groups = []
        self.patternDbDict = []
        self.init(board_size)

    def init(self, board_size):
        print("Initializing pattern DB...")
        with open("patternDb_" + str(board_size) + ".dat", "rb") as patternDbFile:
            self.groups = pickle.load(patternDbFile)
            self.patternDbDict = pickle.load(patternDbFile)
            for i in range(len(self.patternDbDict)):
                print("Group {}: {}, {:,} entries.".format(
                    i, self.groups[i], len(self.patternDbDict[i])))

    def ida_star(self, puzzle):
        if puzzle.check_win():
            return []
        if not self.patternDbDict:
            self.init(puzzle.boardSize)

        t1 = perf_counter_ns()
        bound = self.h_score(puzzle)
        path = [puzzle]
        dirs = []
        while True:
            rem = self.search(path, 0, bound, dirs)
            if rem is True:
                t_delta = (perf_counter_ns() - t1) / self.NANO_TO_SEC
                print("Took {} seconds to find a solution of {} moves".format(
                    t_delta, len(dirs)))
                return dirs
            elif rem == self.INF:
                return None
            bound = rem

    def search(self, path, g, bound, dirs):
        cur = path[-1]
        f = g + self.h_score(cur)

        if f > bound:
            return f

        if cur.check_win():
            return True
        min_val = self.INF

        for direction in cur.DIRECTIONS:
            if dirs and (-direction[0], -direction[1]) == dirs[-1]:
                continue
            valid_move, sim_puzzle = cur.simulate_move(direction)

            if not valid_move or sim_puzzle in path:
                continue

            path.append(sim_puzzle)
            dirs.append(direction)

            t = self.search(path, g + 1, bound, dirs)
            if t is True:
                return True
            if t < min_val:
                min_val = t

            path.pop()
            dirs.pop()

        return min_val

    def h_score(self, puzzle):
        h = 0
        for g in range(len(self.groups)):
            group = self.groups[g]
            hash_string = puzzle.hash(group)
            if hash_string in self.patternDbDict[g]:
                h += self.patternDbDict[g][hash_string]
            else:
                print("No pattern found in DB, using Manhattan distance")
                for i in range(puzzle.boardSize):
                    for j in range(puzzle.boardSize):
                        if puzzle[i][j] != 0 and puzzle[i][j] in group:
                            dest_pos = ((puzzle[i][j] - 1) // puzzle.boardSize,
                                        (puzzle[i][j] - 1) % puzzle.boardSize)
                            h += abs(dest_pos[0] - i)
                            h += abs(dest_pos[1] - j)

        return h
