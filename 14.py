from pathlib import Path

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
    test(puzzle, expected1=24, expected2="", prefix="reference")
    
def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1=795, expected2="")

def preprocess(puzzle):
    lines = []
    for line in puzzle:
        splits = line.split(" -> ")
        points = []
        for s in splits:
            x, y = s.split(",")
            points.append((int(x), int(y)))
        for i,(f,t) in enumerate(zip(points[0::1], points[1::1])):
            lines.append((f, t))
    return lines

def is_pos_free(pos, rocks):
    return pos not in rocks

def drop(sand, rocks):
    x,y = sand
    while y < 200:
        y += 1
        if is_pos_free((x, y), rocks):
            return drop((x, y), rocks)
        elif is_pos_free((x-1, y), rocks):
            return drop((x-1, y), rocks)
        elif is_pos_free((x+1, y), rocks):
            return drop((x+1, y), rocks)
        else:
            rocks.append((x, y-1))
            return True
    return False

def solve_puzzle(puzzle):
    print(puzzle)
    rocks = []
    for f, t in puzzle:
        minx = min(f[0], t[0])
        maxx = max(f[0], t[0])
        miny = min(f[1], t[1])
        maxy = max(f[1], t[1])
        dx = max(f[0], t[0]) - min(f[0], t[0])
        for x in range(minx, maxx+1):
            for y in range(miny, maxy+1):
                rocks.append((x,y))

    s1 = 0
    while drop(sand=(500,0), rocks=rocks):
        s1 += 1

    #for r in rocks: print(r)
    return s1, ""

if (__name__ == "__main__"):
    test_reference()
    print("="*28)
    test_solution()