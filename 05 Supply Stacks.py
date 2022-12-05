from pathlib import Path
import re

def read_stacks():
    with open("05 Stacks.txt", encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]
    stacks = []
    for i in range(9):
        stacks.append([])
    for line in lines:
        for n in range(9):
            i = n*4+1
            if i > len(line):
                continue
            if (line[i]) == " ":
                continue
            stacks[n].append(line[i])
    return stacks

def read_moves():
    with open("05 Moves.txt", encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]
    moves = []
    for line in lines:
        moves.append([int(n) for n in re.findall(r"\d+", line)])

def get_input_data():
    s = read_stacks()
    m = read_moves()
    return s, m

def get_test_data():
    return ["", ""]

def solve_puzzle(stacks, moves):
    print(moves)
    return "", ""

def test_reference():
    res1, res2 = solve_puzzle(get_test_data())
    #assert res1 == 0
    #assert res1 == 0

def test_solution():
    res1, res2 = solve_puzzle(get_test_data())
    #assert res1 == 0
    #assert res2 == 0

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(*get_input_data())
    print("solution1", s1)
    print("solution2", s2)