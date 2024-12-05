from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def preprocess(puzzle):
    return puzzle

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    puzzle = preprocess(puzzle)
    r1, r2 = None, None

    return r1, r2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(None, None))

    solution = None, None
    # solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(None, None))
