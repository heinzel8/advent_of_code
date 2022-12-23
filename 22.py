from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from itertools import pairwise, islice
from pygame import Vector2 as vec

def preprocess(puzzle):
    walls = set()
    open_tiles = set()
    for row, line in enumerate(puzzle):
        if line == "":
            break
        for col, c in enumerate(line):
            if c == "#":
                walls.add((col, row))
            elif c == ".":
                open_tiles.add((col, row))

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

def find_opposite_edge(cur_pos_vec, dir):
    search_dir = vec(-dir.x, -dir.y)
    while True:
        next_pos_vec = cur_pos_vec + search_dir
        next_pos = (next_pos_vec.x, next_pos_vec.y)
        if (next_pos not in all_tiles):
            break
        cur_pos_vec = next_pos_vec
    return (cur_pos_vec.x, cur_pos_vec.y)

def move(pos, count, dir):
    pos = vec(pos)
    for i in range(count):
        next_pos_vec = pos + dir
        next_pos = (next_pos_vec.x, next_pos_vec.y)
        if next_pos in walls:
            break
        elif next_pos not in open_tiles:
            next_pos = find_opposite_edge(pos, dir)
            next_pos_vec = vec(*next_pos)
            if next_pos in walls:
                break
        pos = next_pos_vec
        trace.add((pos[0], pos[1]))
        
    return (pos.x, pos.y)

def rotate(dir:vec, change):
    if change == "L":
        return all_dirs[(all_dirs.index(dir)-1)%4]
    elif change == "R":
        return all_dirs[(all_dirs.index(dir)+1)%4]
    else:
        raise SystemError("unknown rotation")

def init(puzzle_data):
    global walls, open_tiles, path, all_tiles, all_dirs, start_pos, trace, max_x, max_y

    walls, open_tiles, path = puzzle_data
    all_tiles = walls.union(open_tiles)
    all_dirs = [vec(1,0), vec(0,1), vec(-1,0), vec(0,-1)]
    max_x = int(max(e[0] for e in all_tiles))
    max_y = int(max(e[1] for e in all_tiles))
    trace = set()

    for x in range(max_x + 1):
        if (x,0) in all_tiles:
            start_pos = vec(x,0)
            break

def draw(curr_pos, dir):
    dir_symbols = ">v<^"
    lines = []
    with open("out.txt", mode="w") as f:
        for y in range(max_y):
            line = ""
            for x in range(max_x + 1):
                pos = (x,y)
                symbol = " "
                if pos in [curr_pos]:
                    symbol = dir_symbols[all_dirs.index(dir)]
                elif pos in trace:
                    symbol = "o"
                elif pos in walls:
                    symbol = "#"
                elif pos in open_tiles:
                    symbol = "."
                line += symbol
            lines.append(line + "\n")
        f.writelines(lines)
        f.flush()

def solve_puzzle(puzzle_data):
    init(puzzle_data)

    hist = ""
    dir = vec(1,0)
    pos = start_pos
    p1 = [x for x in islice(path,0,len(path),2)]
    p2 = [x for x in islice(path,1,len(path),2)]

    for m,d in zip(p1, p2):
        #print(m, d)
        pos = move(pos, m, dir)
        dir = rotate(dir, d)
        #draw(pos, dir)
        hist += str(m) + str(d)

    m = path[-1]
    pos = move(pos, m, dir)
    hist += str(m)
    #print("final pos:", pos[0], pos[1])

    s1 = int(sum([1000*(pos[1]+1), 4*(pos[0]+1), all_dirs.index(dir)]))
    #print(hist)

    return s1, None

if (__name__ == "__main__"):
    ref = solve_puzzle(preprocess(get_reference_data(__file__)))
    print_statistics("Reference", ref, expected=(6032, None))
    
    # quit()
    sol = solve_puzzle(preprocess(get_puzzle_data(__file__)))
    print_statistics("Solution", sol, expected=(106094, None))