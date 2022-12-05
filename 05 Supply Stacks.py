import re
import copy

def read_stacks():
    with open("05 Stacks.txt", encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]
    stacks = []
    for index in range(9):
        stacks.append([])
    for line in lines:
        for n in range(9):
            index = n*4+1
            if index > len(line) or (line[index]) == " ":
                continue
            stacks[n].append(line[index])
    return [list(reversed(s)) for s in stacks]

def read_moves():
    with open("05 Moves.txt", encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]
    moves = []
    for line in lines:
        moves.append([int(n) for n in re.findall(r"\d+", line)])
    return moves

def get_input_data():
    s = read_stacks()
    m = read_moves()
    return s, m

def get_test_data():
    stacks = [["N", "Z"], ["D", "C", "M"], ["P"]]
    stacks = [list(reversed(s)) for s in stacks]
    moves = [[1, 2, 1],
             [3, 1, 3],
             [2, 2, 1],
             [1, 1, 2]]
    return stacks, moves

def solve_puzzle(stacks, moves):
    stacks1 = copy.deepcopy(stacks)
    for move in moves:
        c, f, t = move
        for i in range(c):
            stacks1[t-1].append(stacks1[f-1].pop())
    s1 = "".join([s[-1] for s in stacks1])

    stacks2 = copy.deepcopy(stacks)
    for move in moves:
        c, f, t = move
        to_move = stacks2[f-1][-c:]
        stacks2[t-1].extend(to_move)
        del(stacks2[f-1][-c:])
    s2 = "".join([s[-1] for s in stacks2])
    return s1, s2

def test_reference():
    res1, res2 = solve_puzzle(*get_test_data())
    assert res1 == "CMZ"
    assert res2 == "MCD"

def test_solution():
    res1, res2 = solve_puzzle(*get_input_data())
    assert res1 == "TDCHVHJTG"
    assert res2 == "NGCMPJLHV"

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(*get_input_data())
    print("solution1", s1)
    print("solution2", s2)