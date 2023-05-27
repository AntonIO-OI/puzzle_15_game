import model
import pickle
from collections import deque
import math
from time import perf_counter_ns

from config import NANO_TO_SEC


class PatternDBBuilder:
    def __init__(self, board_size, groups):
        self.board_size = board_size
        self.groups = groups

    def fact(self, n):
        if n <= 1:
            return 1
        return n * self.fact(n - 1)

    def n_pr(self, n, r):
        return math.floor(self.fact(n) / self.fact(n - r))

    def build_pattern_db(self, group, group_num):
        puzzle = model.Puzzle(self.board_size, shuffle=False)
        puzzle.count = 0

        group_with_blank = group.copy()
        group_with_blank.add(0)

        visited = set()  # Permutations of group tile + blank tile locations visited
        closed_list = (
            {}
        )  # Permutation of group tile locations with min move count so far
        open_list = deque()  # Next permutations to visit
        iterations = 0
        to_iterate = self.n_pr(self.board_size ** 2, len(group_with_blank))
        t1 = perf_counter_ns()

        open_list.append((puzzle, (0, 0)))

        while open_list:
            cur, prev_move = open_list.popleft()

            if not self.visit_node(cur, visited, closed_list, group_with_blank, group):
                continue
            for direction in puzzle.DIRECTIONS:
                if direction == prev_move:
                    continue

                valid_move, sim_puzzle = cur.simulateMove(direction)

                if not valid_move:
                    continue

                if sim_puzzle[cur.blankPos[0]][cur.blankPos[1]] in group:
                    sim_puzzle.count += 1

                open_list.append((sim_puzzle, (-direction[0], -direction[1])))
            iterations += 1

            if iterations % 100000 == 0:
                t2 = perf_counter_ns()
                t_delta = (t2 - t1) / NANO_TO_SEC
                print(
                    "Group {}, Iteration {:,} of {:,}, time elapsed: {}".format(
                        group_num, iterations, to_iterate, t_delta
                    )
                )
                print("Size of closed list: {:,}".format(len(closed_list)))
                print("Size of open list: {:,}".format(len(open_list)))
                t1 = t2

        return closed_list

    @staticmethod
    def visit_node(puzzle, visited, closed_list, group_with_blank, group):
        puzzle_hash_with_blank = puzzle.hash(group_with_blank)
        if puzzle_hash_with_blank in visited:
            return False

        visited.add(puzzle_hash_with_blank)

        group_hash = puzzle.hash(group)
        if group_hash not in closed_list:
            closed_list[group_hash] = puzzle.count
        elif closed_list[group_hash] > puzzle.count:
            closed_list[group_hash] = puzzle.count

        return True

    def run(self):
        closed_list = []

        group_number = 0
        for group in self.groups:
            group_number += 1
            closed_list.append(self.build_pattern_db(group, group_number))

        with open(
            "patternDb_663_" + str(self.board_size) + ".dat", "wb"
        ) as patternDbFile:
            pickle.dump(self.groups, patternDbFile)
            pickle.dump(closed_list, patternDbFile)

        for i in range(len(closed_list)):
            group = closed_list[i]
            print("Group:", self.groups[i], len(group), "permutations")


def main():
    board_size = 4

    # 663
    # groups = [{1, 5, 6, 9, 10, 13}, {7, 8, 11, 12, 14, 15}, {2, 3, 4}]

    # 555
    groups = [{1, 2, 3, 4, 7}, {5, 6, 9, 10, 13}, {8, 11, 12, 14, 15}]

    # 78
    # groups = [{1,2,3,4,5,6,7,8},{9,10,11,12,13,14,15}]

    builder = PatternDBBuilder(board_size, groups)
    builder.run()


if __name__ == "__main__":
    main()
