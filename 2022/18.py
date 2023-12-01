from pathlib import Path
from pygame import Vector3 as vec

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
    test(puzzle, expected1=64, expected2=58, prefix="reference")

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1=3364, expected2=2006)

def preprocess(puzzle):
    return set([Cube(vec(list(map(int, l.split(","))))) for l in puzzle])

class Cube:
    def __init__(self, pos:vec) -> None:
        self.pos = pos
    pos = vec(0,0,0)
    outer_surfaces_count = 0


def process(seed_pos, cubes):
    work_stack = [seed_pos]
    curr_stack_pos = 0
    while curr_stack_pos < len(work_stack):
        curr_pos = work_stack[curr_stack_pos]
        for neighbor_pos in [vec(curr_pos + d) for d in dirs]:
            if minx <= neighbor_pos.x <= maxx and miny <= neighbor_pos.y <= maxy and minz <= neighbor_pos.z <= maxz:
                neighbor_cube = next((c for c in cubes if c.pos == neighbor_pos), None)
                if neighbor_cube is not None:
                    neighbor_cube.outer_surfaces_count += 1
                elif neighbor_pos not in work_stack:
                    work_stack.append(neighbor_pos)
                    
        curr_stack_pos += 1
    pass

def solve_puzzle(cubes):
    global dirs
    dirs = [vec(1,0,0), vec(-1,0,0), vec(0,1,0), vec(0,-1,0), vec(0,0,1), vec(0,0,-1)]

    global cubes_positions
    cubes_positions = [c.pos for c in cubes]

    global minx
    global miny
    global minz
    global maxx
    global maxy
    global maxz

    minx = int(min([p.x for p in cubes_positions])) -1
    miny = int(min([p.y for p in cubes_positions])) -1
    minz = int(min([p.z for p in cubes_positions])) -1
    maxx = int(max([p.x for p in cubes_positions])) +1
    maxy = int(max([p.y for p in cubes_positions])) +1
    maxz = int(max([p.z for p in cubes_positions])) +1

    s1 = len(cubes)*6
    for cube in cubes:
        for dir in dirs:
            if cube.pos+dir in cubes_positions:
                s1 -= 1

    seed_cube = vec(minx, miny, minz)
    process(seed_cube, cubes)
    s2 = sum(c.outer_surfaces_count for c in cubes)

    return s1, s2

if (__name__ == "__main__"):
    test_reference()
    print("="*28)
    test_solution()