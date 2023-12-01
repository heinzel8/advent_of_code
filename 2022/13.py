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

def test(puzzle, expected1, expected2, prefix = ""):
    s1, s2 = solve_puzzle(puzzle)
    for i in [1, 2]:
        s = str(eval(f"str(s{i})"))
        exp = str(eval(f"expected{i}"))
        app = "  PASS" if s == exp else "  FAIL - should be " + exp
        print(prefix + f"solution {i}: " + s + " " + app)
        
    if (__name__ != "__main__"):
        assert s1 == expected1
        assert s2 == expected2

def test_reference():
    puzzle = preprocess(get_reference_data())
    test(puzzle, expected1=13, expected2=1401)

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1=5843, expected2=26289)

if (__name__ == "__main__"):
    test_reference()
    print("="*28)
    test_solution()