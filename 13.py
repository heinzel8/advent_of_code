from pathlib import Path

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data(id=1):
    with open(Path(__file__).stem + f"_reference{id}.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def cmp_int(v1, v2):
    if v1 == v2: return 0
    if v1 < v2: return -1
    if v1 > v2: return 1

type_list = type([])

def cmp(v1, v2):
    if type(v1) == int and type(v2) == int:
        return cmp_int(v1, v2)
    if type(v1) == type_list and type(v2) == type_list:
        m = min(len(v1), len(v2))
        for i in range(m):
            res = cmp(v1[i], v2[i])
            if res != 0:
                return res
        if len(v1) < len(v2): return -1
        elif len(v1) > len(v2): return 1
        else: return 0
    elif type(v1) == int and type(v2) == type_list:
        return cmp([v1], v2)
    elif type(v2) == int and type(v1) == type_list:
        return cmp(v1, [v2])
    else:
        raise Exception("unhandled case")

def get_val(v1):
    if type(v1) == int:
        return v1
    if type(v1) == type_list:
        m = min(len(v1), len(v2))
        for i in range(m):
            res = cmp(v1[i], v2[i])
            if res != 0:
                return res
        if len(v1) < len(v2): return -1
        elif len(v1) > len(v2): return 1
        else: return 0
    elif type(v1) == int and type(v2) == type_list:
        return cmp([v1], v2)
    elif type(v2) == int and type(v1) == type_list:
        return cmp(v1, [v2])
    else:
        raise Exception("unhandled case")
            

def solve_puzzle(puzzle):
    part1 = 0
    for l in range((len(puzzle)+1)//3):
        v1 = eval(puzzle[l*3])
        v2 = eval(puzzle[l*3+1])
        res = cmp(v1, v2)
        if res == -1:
            part1 += (l+1)
        print(l, res)

    packets = []
    for line in puzzle:
        if line == "": continue
        packets.append(eval(line))
        packets = sorted(packets, key = lambda i: )

    return part1, ""

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