from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from itertools import combinations

def preprocess(puzzle):
    antennas = {}
    for y, line in enumerate(puzzle):
        line = line.strip()
        for x, char in enumerate(list(line)):
            if char == ".":
                continue
            antennas.update({char: antennas.get(char, []) + [(x,y)]})
    return antennas

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    antennas = preprocess(puzzle)
    max_x = len(puzzle[0])-1
    max_y = len(puzzle)-1

    antipodes1, antipodes2 = set(), set()
    for positions in antennas.values():
        for p1, p2 in combinations(positions, 2):
            x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
            dx, dy = x2-x1, y2-y1
            factor = max(int(max_x/dx+1), int(max_y/dy+1))
            for f in range(-factor, factor):
                for a in [(x1-dx*f, y1-dy*f), (x2+dx*f, y2+dy*f)]:
                    if 0 <= a[0] <= max_x and 0 <= a[1] <= max_y:
                        if f == 1:
                            antipodes1.add(a)
                        antipodes2.add(a)
    r1 = len(antipodes1)
    r2 = len(antipodes2)
    return r1, r2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(14, 34))

    solution = None, None
    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(291, 1015))
