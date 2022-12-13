from pathlib import Path

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data(id=1):
    with open(Path(__file__).stem + f"_reference{id}.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def test(puzzle, expected1, expected2, prefix = ""):
    s1, s2 = solve_puzzle(puzzle)
    if prefix != "": print(prefix) 
    for i in [1, 2]:
        s = str(eval(f"str(s{i})"))
        exp = str(eval(f"expected{i}"))
        app = "  PASS" if s == exp else "  FAIL - should be " + exp
        print(f"solution {i}: " + s + " " + app)
        
    if (__name__ != "__main__"):
        assert s1 == expected1
        assert s2 == expected2

def test_reference():
    puzzle = preprocess(get_reference_data())
    test(puzzle, expected1="", expected2="", prefix="reference")

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1="", expected2="")

def preprocess(puzzle):
    return [eval(line) for line in puzzle if line != ""]

def solve_puzzle(puzzle):
    return "", ""

if (__name__ == "__main__"):
    test_reference()
    print("="*28)
    test_solution()