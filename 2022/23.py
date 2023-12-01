from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def preprocess(puzzle):
    return puzzle

def solve_puzzle(puzzle):
    return None, None

if (__name__ == "__main__"):
    ref = solve_puzzle(get_reference_data(__file__))
    print_statistics("Reference", ref, expected=(None, None))
    
    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution",  sol, expected=(None, None))
