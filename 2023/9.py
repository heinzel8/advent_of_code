from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re
from itertools import pairwise


def preprocess(puzzle):
    histories = []
    for line in puzzle:
        histories.append(list(map(int, re.findall("-*\d+", line))))
    return histories

def extrapolate(history, forward):
    diffs = [history]
    while not all(v == 0 for v in diffs[-1]):
        diffs.append([v2-v1 for v1,v2 in pairwise(diffs[-1])])

    result = 0
    if forward:
        for diff in diffs[::-1]:
            result += diff[-1]
    else:
        for diff in diffs[::-1]:
            result = diff[0] - result
    return result

def solve_puzzle(puzzle):
    part1 = part2 = 0
    histories = preprocess(puzzle)

    for history in histories:
        part1 += extrapolate(history, forward=True)
        pass

    for history in histories:
        part2 += extrapolate(history, forward=False)

    return part1, part2

def run_tests():
    pass


if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(114, 2))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(1479011877, 973))