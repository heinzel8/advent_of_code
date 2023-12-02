from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def preprocess(puzzle):
    return puzzle

def solve_puzzle(puzzle, part):
    return None, None

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = solve_puzzle(get_reference_data(__file__, part=1), part=1)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), part=2)[1]
    print_statistics("Reference", (ref1, ref2), expected=(None, None))

    sol1 = solve_puzzle(get_puzzle_data(__file__), part=1)
    sol2 = solve_puzzle(get_puzzle_data(__file__), part=2)
    print_statistics("Solution", (sol1, sol2), expected=(None, None))
