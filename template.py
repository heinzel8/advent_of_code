from pathlib import Path

def get_puzzle_data():
    stem = Path(__file__).stem
    if stem == "template": return ""
    with open(stem + ".txt", encoding="utf8") as f:
        return preprocess([line.strip() for line in f.readlines()])

def get_reference_data():
    stem = Path(__file__).stem
    if stem == "template": return ""
    with open(stem + f"_reference.txt", encoding="utf8") as f:
        return preprocess([line.strip() for line in f.readlines()])

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
    return puzzle

def solve_puzzle(puzzle):
    return None, None

def print_statistics(r1, r2, s1, s2, exp_r1, exp_r2, exp_s1, exp_s2):
    
    test_reference()
    print("="*28)
    test_solution()

if (__name__ == "__main__"):
    exp_r1, exp_r2 = None, None
    exp_s1, exp_s2 = None, None

    r1, r2 = solve_puzzle(get_reference_data)
    s1, s2 = solve_puzzle(get_puzzle_data)
    
    print_statistics(r1, r2, s1, s2, exp_r1, exp_r2, exp_s1, exp_s2)
    
    