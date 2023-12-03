from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re
import functools
import operator

def preprocess(puzzle):
    return puzzle

def get_surrounding_block(puzzle, row, col_from, col_to):
    result = []
    max_col = len(puzzle[0])
    col_from = max(col_from-1, 0)
    col_to = min(col_to+1, max_col)
    for r in range(max(0, row-1), min(row+2, len(puzzle))):
        result.append(puzzle[r][col_from:col_to+1])
    return result

def has_symbol(block):
    for c in ". 0 1 2 3 4 5 6 7 8 9 \n".split():
        block = block.replace(c, '')
    block.strip()
    return len(block) > 0

def get_chebyshev_dist(f, t):
    return max(abs(f[0]-t[0]), abs(f[1]-t[1]))

def solve_puzzle(puzzle):
    sum1 = sum2 = 0
    max_col = len(puzzle[0])
    for row, line in enumerate(puzzle):
        for match in re.finditer("\d+", line):
            number = match.group(0)
            block = get_surrounding_block(puzzle, row, match.span()[0], match.span()[1]-1)
            if has_symbol("".join(block)):
                sum1 += int(number)
    for row, line in enumerate(puzzle):
        for match in re.finditer("\*", line):
            gear_y, gear_x = row, match.span()[0]
            block = get_surrounding_block(puzzle, gear_y, 0, max_col)
            gear_y = 1
            close_numbers = []
            for y, line in enumerate(block):
                for match in re.finditer("\d+", line):
                    number = match.group(0)
                    num_start_x, num_end_x = match.span()[0], match.span()[1]-1
                    for x in range(num_start_x, num_end_x+1):
                        if get_chebyshev_dist((gear_x, gear_y), (x, y)) <= 1:
                            close_numbers.append(int(number))
                            break
            if len(close_numbers) == 2:
                sum2 += functools.reduce(operator.mul, close_numbers)
                    
    return sum1, sum2

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(4361, 467835))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(507214, 72553319))
