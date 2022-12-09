from pathlib import Path

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data(id=1):
    with open(Path(__file__).stem + f"_reference{id}.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def solve_puzzle(puzzle):
    return "", ""

def test_reference():
    res1, res2 = solve_puzzle(get_reference_data())
    #assert res1 == 0
    #assert res2 == 0

def test_solution():
    res1, res2 = solve_puzzle(get_puzzle_data())
    #assert res1 == 0
    #assert res2 == 0

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_puzzle_data())
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")