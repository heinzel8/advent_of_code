from pathlib import Path
from functools import cmp_to_key

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data():
    with open(Path(__file__).stem + f"_reference.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def preprocess(puzzle):
    return [eval(line) for line in puzzle if line != ""]

def cmp(left, right):
    if type(left) is int and type(right) is int:
        return left - right
    if type(left) is not list: left = [left]
    if type(right) is not list: right = [right]
    for l, r in zip(left, right):
        res = cmp(l, r)
        if res != 0:
            return res
    return len(left) - len(right)

def solve_puzzle(puzzle):
    part1 = 0
    for i, (l,r) in enumerate(zip(puzzle[0::2], puzzle[1::2]), 1):
        part1 += i if cmp(l,r) < 0 else 0
    
    puzzle += [[[2]], [[6]]]
    puzzle = sorted(puzzle, key=cmp_to_key(cmp))
    part2 = (puzzle.index([[2]])+1) * (puzzle.index([[6]])+1)

    return part1, part2

def test_reference():
    puzzle = preprocess(get_reference_data())
    s1, s2 = solve_puzzle(puzzle)
    assert s1 == 13
    assert s2 == 140

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    s1, s2 = solve_puzzle(puzzle)
    assert s1 == 5843
    assert s2 == 26289

if (__name__ == "__main__"):
    test_reference()
    test_solution()
    puzzle = preprocess(get_puzzle_data())
    s1, s2 = solve_puzzle(puzzle)
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")