from pathlib import Path
from pygame import Vector2 as vec

DIRS = [(1,0), (0,1), (-1,0), (0,-1)]

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return {(x,y): ord(v) if v.islower() else v 
            for y,line in enumerate(f.readlines())
            for x,v in enumerate(line.strip())}

def get_reference_data(id=1):
    with open(Path(__file__).stem + f"_reference{id}.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def valid_pos(pos, puzzle):
    x = int(pos.x)
    y = int(pos.y)
    if y < 0 or y >= len(puzzle) or x < 0 or x >= len(puzzle[0]):
        return False
    return True

def get_value(pos, puzzle):
    if not valid_pos(pos, puzzle):
        raise Exception()
    x = int(pos.x)
    y = int(pos.y)
    return puzzle[y][x]

def get_elevation(pos, puzzle):
    norm = ord("a") - 1
    val = get_value(pos, puzzle)
    if val == "S":
        return 1
    if val == "E":
        return ord("z") + 1 - norm
    return ord(val) - norm

def step_allowed(curr_pos, next_pos, trace, puzzle):
    if not valid_pos(next_pos, puzzle):
        return False
    if curr_pos == next_pos:
        return False
    #val = get_value(next_pos, puzzle)
    next_elevation = get_elevation(next_pos, puzzle)
    curr_elevation = get_elevation(curr_pos, puzzle)
    diff = next_elevation - curr_elevation
    if diff not in [0,1]:
        return False
    if str(next_pos) in trace:
        return False
    return True

def step_forward(pos, end, trace, solutions, puzzle):
    trace.append(pos)
    if puzzle[pos] == end:
        solutions.append(trace.copy())
        return
    # next_positions = get_next_positions(pos, trace, puzzle)
    # if len(next_positions) == 0:
    #     return
    for next_pos in get_next_positions(pos, trace, puzzle):
        step_forward(next_pos, trace, solutions, puzzle)

def get_next_positions(x, y, trace, puzzle):
    for neighbor in [(x+dx, y+dy) for dx, dy in DIRS]:
        if step_allowed((x,y), neighbor, trace, puzzle):
            yield neighbor
    #possible = []
    # for dir in DIRS:
    #     next_pos = pos + dir.x
    #     if step_allowed(pos, next_pos, trace, puzzle):
    #         possible.append(next_pos)
    # return possible

def find_start(puzzle):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            p = vec(x, y)
            if get_value(p, puzzle) == "S":
                return p
            # if get_value(p, puzzle) == "E":
            #     FINAL = vec(p.x, p.y, p.z)

def solve_puzzle(puzzle):
    for pos, elevation in puzzle.items():
        if elevation == "S":
            start = pos
            puzzle[pos] = 1
        if elevation == "E":
            end = pos
            puzzle[pos] = 26
    steps = 0
    trace = []
    solutions = []
    step_forward(start, end, trace, solutions, puzzle)
    solutions = sorted(solutions, key=lambda x: len(x), reverse=False)
    return len(solutions[0])-1, ""

def test_reference():
    res1, res2 = solve_puzzle(get_reference_data())
    #assert res1 == 0
    #assert res2 == 0

def test_solution():
    res1, res2 = solve_puzzle(get_puzzle_data())
    #assert res1 == 0
    #assert res2 == 0

if (__name__ == "__main__"):
    puzzle = get_puzzle_data()
    s1, s2 = solve_puzzle(puzzle)
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")