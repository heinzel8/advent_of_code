from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from itertools import pairwise
from pygame import vector2 as vec

def preprocess(puzzle):
    walls = []
    open_tiles = []
    for row, line in enumerate(puzzle):
        if line == "":
            break
        for col, c in enumerate(line):
            if c == "#":
                walls.append((col, row))
            elif c == ".":
                open_tiles.append((col, row))

    ll = puzzle[-1]
    path = []
    i_last = 0
    for i,c in enumerate(ll):
        if c.isalpha():
            path.append(int(ll[i_last:i]))
            path.append(c)
            i_last = i + 1
    path.append(int(ll[i_last:len(ll)]))
    return [walls, open_tiles, path]

def move(pos, count, dir):
    for i in range(count):
        next_pos = vec(*pos) + vec(*dir)


def solve_puzzle(puzzle):
    global walls, open_tiles, path
    walls, open_tiles, path = puzzle

    all_tiles = [*walls, *open_tiles]
    min_x, min_y = 0, 0
    max_x = max(e[0] for e in all_tiles)
    max_y = max(e[1] for e in all_tiles)

    start = (0,0)
    for x in range(max_x + 1):
        if (x,0) in all_tiles:
            start = (x,0)
            break

    dir = (1,0)
    pos = start
    for m,d in pairwise(path):
        pos = move(pos, m, dir)

    return None, None

if (__name__ == "__main__"):
    ref = solve_puzzle(preprocess(get_reference_data(__file__)))
    print_statistics("Reference", ref, expected=(None, None))
    
    # sol = solve_puzzle(preprocess(get_puzzle_data(__file__)))
    # print_statistics("Solution",  sol, expected=(None, None))
