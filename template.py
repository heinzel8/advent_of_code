from pathlib import Path

def get_input_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return ["", ""]

def solve_puzzle(lines):
    return "", ""

def test_reference():
    res1, res2 = solve_puzzle(get_test_data())
    #assert res1 == 0
    #assert res2 == 0

def test_solution():
    res1, res2 = solve_puzzle(get_test_data())
    #assert res1 == 0
    #assert res2 == 0

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_input_data())
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")