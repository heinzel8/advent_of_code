from pathlib import Path
import re

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data():
    with open(Path(__file__).stem + f"_reference.txt", encoding="utf8") as f:
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
    pattern = "Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    puzzle = [[re.search(pattern, line).groups()] for line in puzzle]
    puzzle = [[id, int(flow_rate), [targets.split(", ")]] for id, flow_rate, targets in puzzle]
    print()


def solve_puzzle(puzzle):
    return "", ""

if (__name__ == "__main__"):
    # text1 = "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
    # text2 = "Valve HH has flow rate=22; tunnel leads to valve GG"
    # pattern = "Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    # print([re.search(pattern, text2).groups()])
    # print()

    test_reference()
    # print("="*28)
    # test_solution()