import re
from pathlib import Path

def get_input_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return ["2-4,6-8",
            "2-3,4-5",
            "5-7,7-9",
            "2-8,3-7",
            "6-6,4-6",
            "2-6,4-8"]

def solve_puzzle(lines):
    ranges = [list(map(int, re.findall(r"\d+", line))) for line in lines]
    result1 = sum([f1 <= f2 and t1 >= t2 or f2 <= f1 and t2 >= t1 for f1,t1,f2,t2 in ranges])
    result2 = sum([max(f1,f2) <= min(t1,t2) for f1,t1,f2,t2 in ranges])
    return result1, result2

def test_reference1():
    assert solve_puzzle(get_test_data())[0] == 2

def test_reference2():
    assert solve_puzzle(get_test_data())[1] == 4

def test_solution():
    assert solve_puzzle(get_input_data())[0] == 471
    assert solve_puzzle(get_input_data())[1] == 888

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_input_data())
    print("solution1", s1)
    print("solution2", s2)