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
    global target_y
    target_y = 10
    global min_x, min_y
    min_x = 0
    min_y = 0
    global max_x, max_y
    max_x = 20
    max_y = 20
    
    puzzle = preprocess(get_reference_data())
    test(puzzle, expected1=26, expected2="", prefix="reference")

def test_solution():
    global target_y
    target_y = 2_000_000
    global min_x, min_y
    min_x = 0
    min_y = 1_900_000
    global max_x, max_y
    max_x = 4_000_000
    max_y = 2_100_000
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1=5525990, expected2="")

def preprocess(puzzle):
    return [list(map(int, re.findall(r"\d+", line))) for line in puzzle]

def calc_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def combine(target_line):
    m = 0
    while m < len(target_line)-1:
        if len(target_line) < 2: break
        for n in range(m+1, len(target_line)):
            l1 = target_line[m]
            l2 = target_line[n]
            a = l2[0]-1 <= l1[0] <= l2[1]+1
            b = l2[0]-1 <= l1[1] <= l2[1]+1
            c = l1[0]-1 <= l2[0] <= l1[1]+1
            d = l1[0]-1 <= l2[1] <= l1[1]+1
            if a or b or c or d:
                x = min(l1[0], l2[0])
                y = max(l1[1], l2[1])
                del(target_line[n])
                del(target_line[m])
                target_line.append((x,y))
                m = -1
                break
        m += 1
    return sorted(target_line, key=lambda p: p[1])


def get_target_line(target_y, sensors, beacons, min_x, max_x):
    target_line = []
    for s in sensors.items():
        (sx, sy),d = s
        diff_y = abs(sy - target_y)
        if diff_y >= d: continue
        diff_y = d - diff_y
        target_line.append((sx - diff_y, sx + diff_y))
        # for i in range(sx - diff_y, sx + diff_y + 1):
        #     if min_x <= i <= max_x:
        #         e = (i, target_y)
        #         #if str(e) in beacons: continue
        #         target_line.add(i)
    return combine(target_line)

def print_picture(sensors, beacons):
    for y in range(min_y, max_y+1):
        target_line = get_target_line(y, sensors, beacons, min_x=min_x, max_x=max_x)
        for x in range(min_x, max_x+1):
            if str((x,y)) in beacons:
                print("B", end="")
            elif (x,y) in sensors:
                print("S", end="")
            elif x in target_line:
                print("#", end="")
            else:
                print(".", end="")
        print()
        #print(y, len(target_line), " "*10)

def solve_puzzle(puzzle):
    sensors = dict()
    beacons = set()
    for xs, ys, xb, yb in puzzle:
        sensors.update({(xs, ys): calc_distance(p1=(xs, ys), p2=(xb, yb))})
        beacons.add(str((xb, yb)))

    #target_line = get_target_line(target_y, sensors, beacons, min_x=-1e10, max_x=1e10)
    #s1 = len(target_line)

    coll = []
    #print_picture(sensors, beacons)
    for y in range(min_y, max_y+1):
        #not_in_line = []
        target_line = get_target_line(y, sensors, beacons, min_x=min_x, max_x=max_x)
        #print(y, len(target_line))
        if len(target_line) != 1:
            coll.append(target_line)
            #print(y, len(target_line))
    # for x in range(min_x, max_x):
    #     if x not in target_line:
    #         not_in_line.append(x)

    two = 0
    for i,l in enumerate(coll):
        print(l[1][0] - l[0][1])
    
    #print("not_in_line", not_in_line)
    #s2 = not_in_line[0] * 4000000 + target_y

    return "", ""

if (__name__ == "__main__"):
    # s1, s2 = solve_puzzle(preprocess(get_puzzle_data()))
    # print("s1: ", s1)
    # print("s2: ", s2)
    # assert s1 > 5117391
    #test_reference()
    #print("="*28)
    test_solution()

    target_line = [(10,20), (21,22), (24,26)]
    target_line = combine(target_line)
    pass