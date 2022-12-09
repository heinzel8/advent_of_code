from pathlib import Path

def get_input_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return ["", ""]

def move(Hx, Hy, dir):
    if dir == "R":
        Hx += 1
    if dir == "L":
        Hx -= 1
    if dir == "U":
        Hy += 1
    if dir == "D":
        Hy -= 1
    return Hx, Hy

def solve_puzzle(lines):
    Hx = Tx = 0
    Hy = Ty = 0
    traceT = []

    for line in lines:
        for _ in range(int(line[2:])):
            Hx, Hy = move(Hx, Hy, line[0])
            dx = Hx - Tx
            dy = Hy - Ty
            if max(abs(dx), abs(dy)) > 1:
                # if min(dx, dy) == 0:
                #     Tx += dx
                #     Ty += dy
                # else:
                if abs(dx) > 0:
                    dx //= abs(dx)
                if abs(dy) > 0:
                    dy //= abs(dy)
                Tx += dx
                Ty += dy
                T = [Tx, Ty]
            if T not in traceT:
                traceT.append(T)

            print(Hx, Hy, Tx, Ty, "  ", line)
        
    return len(traceT), ""

def test_reference():
    res1, res2 = solve_puzzle(get_test_data())
    #assert res1 == 0
    #assert res2 == 0

def test_solution():
    res1, res2 = solve_puzzle(get_input_data())
    #assert res1 == 0
    #assert res2 == 0

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_input_data())
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")