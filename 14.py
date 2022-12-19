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
    test(puzzle, expected1=24, expected2=93, prefix="reference")
    
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

def drop(sand, max_y, rocks):
    x,y = sand
    max_y_copy = max_y if max_y is not None else 200
    while y <= max_y_copy:
        if not is_pos_free((x, y), rocks):
            return False
        y += 1
        if is_pos_free((x, y), rocks):
            if max_y is not None and y == max_y:
                rocks.append((x, y-1))
                #print("y", y-1, " "*10, end="\r")
                return True
            else:
                return drop((x, y), max_y, rocks)
        elif is_pos_free((x-1, y), rocks):
            return drop((x-1, y), max_y, rocks)
        elif is_pos_free((x+1, y), rocks):
            return drop((x+1, y), max_y, rocks)
        else:
            rocks.append((x, y-1))
            #print("y", y-1, " "*10, end="\r")
            return True, (x, y-1)
    return False, ""

def fill_rocks(puzzle):
    rocks = []
    highest_y = 0
    highest_x = 0
    lowest_x = 1_000_000
    for f, t in puzzle:
        minx = min(f[0], t[0])
        maxx = max(f[0], t[0])
        miny = min(f[1], t[1])
        maxy = max(f[1], t[1])
        highest_y = max(highest_y, maxy)
        highest_x = max(highest_x, maxx)
        lowest_x = min(lowest_x, minx)
        dx = max(f[0], t[0]) - min(f[0], t[0])
        for x in range(minx, maxx+1):
            for y in range(miny, maxy+1):
                rocks.append((x,y))
    return rocks, highest_y, highest_x, lowest_x

def solve_puzzle(puzzle):
    rocks, highest_y, highest_x, lowest_x = fill_rocks(puzzle)

    s1 = 0
    ret = False
    while ret:
        ret, pos = drop(sand=(500,0), max_y=None, rocks=rocks)
        s1 += 1
        if s1 % 10 == 0:
            pass
            # print_picture(rocks, highest_y)
            # print(len(rocks))
        # print("s1", s1, end="\r")

    #puzzle.append([(lowest_x-50, highest_y+2), (highest_x+50, highest_y+2)])
    rocks,_,_,_ = fill_rocks(puzzle)
    print_picture(rocks, highest_y)

    s2 = 0
    
    ret = True
    while ret:
        ret, pos = drop(sand=(500,0), max_y=highest_y+2, rocks=rocks)
        s2 += 1
        #if s2 % 10 == 0:
        update_picture(highest_y, pos)
        # print("s2", s2, end="\r")

    return s1, s2

def print_picture(rocks, highest_y):
    highest_x = 500 + highest_y//2
    lowest_x = 500 - highest_y//2
    with open("out.txt", mode="w") as f:
        for y in range(highest_y+1):
            for x in range(lowest_x, highest_x+1):
                if is_pos_free((x,y), rocks):
                    f.write(" ")
                else:
                    f.write("#")
            f.write("\n")

def update_picture(highest_y, pos):
    highest_x = 500 + highest_y//2
    lowest_x = 500 - highest_y//2
    x, y = pos
    line_length = (highest_x - lowest_x) + 3
    with open("out.txt", mode="r+") as f:
        f.seek(y * line_length + x - lowest_x)
        #f.seek(2)
        f.write("o")
        f.flush()

if (__name__ == "__main__"):
    #test_reference()
    #print("="*28)
    test_solution()