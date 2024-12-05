from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import copy

def preprocess(puzzle):
    r = []
    for line in puzzle:
        s = line.split()
        s = list(map(int, s))
        r.append(s)
    return r

def is_safe(line):
    diff = line[1] - line[0]
    if diff == 0:
        sign = -2
    else:
        sign = diff / abs(diff)
    
    good = True
    for e1, e2 in zip(line, line[1:]):
        diff = e2 - e1
        if abs(diff) > 3: 
            good = False
        if abs(diff) < 1: 
            good = False
        if diff !=0 and diff/abs(diff) != sign:
            good = False

    return good

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    puzzle = preprocess(puzzle)

    r1 = 0
    for line in puzzle:
        if is_safe(line):
            r1 += 1

    r2 = 0
    for line in puzzle:
        if is_safe(line):
            r2 += 1
            continue
        for index in range(0,len(line)):
            line_copy = copy.deepcopy(line)
            del line_copy[index]
            if is_safe(line_copy):
                r2 += 1
                break

    return r1, r2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(2, 4))

    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(585, 626))
