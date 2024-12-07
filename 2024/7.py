from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re
from itertools import combinations, product

def preprocess(puzzle):
    values = []
    for line in puzzle:
        values.append(list(map(int, re.split("[: ]+", line))))
    return values

def get_combinations(line, operators):
    expressions = []
    operators_count = len(line)-2
    combinations = list(product(operators, repeat=operators_count))
    for operator in combinations:
        ex = f"{line[1]}"
        for i, val in enumerate(line[2:]):
            if operator[i] == "||":
               ex = f"{eval(ex)}{val}"
            else:
                ex = f"({ex}) {operator[i]} {val}"
        expressions.append(ex)
    return expressions

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    puzzle = preprocess(puzzle)
    r1, r2 = None, None

    if solve_part1:
        r1 = 0
        for line in puzzle:
            expected = line[0]
            expressions = get_combinations(line, operators=["+", "*"])
            for expression in expressions:
                if eval(expression) == expected:
                    r1 += expected
                    break
    if solve_part2:
        r2 = 0
        for i, line in enumerate(puzzle, 1):
            expected = line[0]
            expressions = get_combinations(line, operators=["+", "*", "||"])
            if expected == 7290:
                pass
            for expression in expressions:
                if eval(expression) == expected:
                    print(f"{expected} = {expression}")
                    r2 += expected
                    break
            print(f"{round(i/len(puzzle)*100, 1)}%")

    return r1, r2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(3749, 11387))

    solution = None, None
    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(None, None))
