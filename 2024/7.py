from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re
from itertools import combinations, product

def preprocess(puzzle):
    values = []
    for line in puzzle:
        values.append(list(map(int, re.split("[: ]+", line))))
    return values

def has_solution(line, operators):
    combinations = list(product(operators, repeat=len(line)-2))
    for operator in combinations:
        res = line[1]
        for i, val in enumerate(line[2:]):
            if operator[i] == "+":
                res += int(val)
            elif operator[i] == "*":
                res *= int(val)
            elif operator[i] == "||":
               res = int(f"{res}{val}")
            if res > line[0]:
                break
        if res == line[0]:
            return True
    return False

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    puzzle = preprocess(puzzle)
    r1, r2 = None, None

    if solve_part1:
        r1 = 0
        for line in puzzle:
            if has_solution(line, operators=["+", "*"]):
                r1 += line[0]

    if solve_part2:
        r2 = 0
        for i, line in enumerate(puzzle, 1):
            expected = line[0]
            if has_solution(line, operators=["+", "*", "||"]):
                r2 += expected
            progress = round(i/len(puzzle)*100, 1)
            print(f"  Progress: {progress}%   ", end="\r")

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
    print_statistics("Solution", solution, expected=(303876485655, 146111650210682))
