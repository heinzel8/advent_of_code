from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import itertools as it

def preprocess(puzzle):
    values1 = []
    values2 = []
    for line in puzzle:
        val1,val2 = line.split()
        values1.append(int(val1))
        values2.append(int(val2))
    return values1, values2

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    puzzle = preprocess(puzzle)
    result1 = 0
    result2 = 0

    values1 = sorted(puzzle[0])
    values2 = sorted(puzzle[1])
    
    for v1,v2 in zip(values1, values2):
        result1 += abs(v2-v1)
    
    for v1 in puzzle[0]:
        result2 += puzzle[1].count(v1) * v1
    
    return result1, result2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(11, 31))

    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(2367773, 21271939))
