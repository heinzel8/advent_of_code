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

class Edge:
    def __init__(self, name, from_pt, line_length, line_dir, invert_line, move_dir, companion) -> None:
        self.from_point = from_pt
        self.move_dir = move_dir
        self.name = name
        self.companion = companion
        self.calculate_points(from_pt, line_dir, line_length, invert_line)
    
    def calculate_points(self, from_pt, line_dir, line_length, invert_line):
        if invert_line:
            from_pt = from_pt + (line_length-1) * line_dir
            line_dir = line_dir * -1
        self.points = [((vec(from_pt) + n*line_dir)) for n in range(line_length)]
        pass

    from_point = (None,None)
    move_dir = (0,0)
    points = []
    name = ""
    companion = ""

def move_to_associated_edge_part2(cur_pos_vec, dir):
    current_edge = None
    other_edge = None
    for edge in edges:
        if (cur_pos_vec.x, cur_pos_vec.y) in edge.points and edge.move_dir == dir:
            current_edge = edge
            other_edge = [e for e in edges if e.name == edge.companion][0]
            break
    if other_edge is None:
        raise ValueError(f"other edge not found for {cur_pos_vec}")
    p = other_edge.points[current_edge.points.index((cur_pos_vec.x, cur_pos_vec.y))]
    return (p.x, p.y), -1 * other_edge.move_dir

def move_to_opposite_edge_part1(cur_pos_vec, dir):
    search_dir = vec(-dir.x, -dir.y)
    while True:
        next_pos_vec = cur_pos_vec + search_dir
        next_pos = (next_pos_vec.x, next_pos_vec.y)
        if (next_pos not in all_tiles):
            break
        cur_pos_vec = next_pos_vec
    return (cur_pos_vec.x, cur_pos_vec.y)

def move_to_associated_edge(cur_pos_vec, dir):
    if PUZZLE_PART_2:
        return move_to_associated_edge_part2(cur_pos_vec, dir)
    else:
        return move_to_opposite_edge_part1(cur_pos_vec, dir), dir

def move(pos, count, dir):
    pos = vec(pos)
    for i in range(count):
        next_dir = dir
        next_pos_vec = pos + dir
        next_pos = (next_pos_vec.x, next_pos_vec.y)
        if next_pos in walls:
            break
        elif next_pos not in open_tiles:
            next_pos, next_dir = move_to_associated_edge(pos, dir)
            next_pos_vec = vec(*next_pos)
            if next_pos in walls:
                break
        pos = next_pos_vec
        dir = next_dir
        trace.add((pos[0], pos[1]))
        
    return (pos.x, pos.y), dir

def rotate(dir:vec, change):
    if change == "L":
        return all_dirs[(all_dirs.index(dir)-1)%4]
    elif change == "R":
        return all_dirs[(all_dirs.index(dir)+1)%4]
    else:
        raise SystemError("unknown rotation")

def init(puzzle_data):
    global walls, open_tiles, path, all_tiles, all_dirs, start_pos, trace, max_x, max_y
    global edges

    walls, open_tiles, path = puzzle_data
    all_tiles = walls.union(open_tiles)
    all_dirs = [vec(1,0), vec(0,1), vec(-1,0), vec(0,-1)]
    max_x = int(max(e[0] for e in all_tiles))
    max_y = int(max(e[1] for e in all_tiles))
    trace = set()

    RIGHT, DOWN, LEFT, UP = all_dirs
    normal, invert = False, True

    if PUZZLE_REFERENCE_DATA:
        x = (max_x+1)//4
        y = (max_y+1)//3
        line_len = x
        A,B = (2*x, 0*y), (3*x-1, 0*y)
        C,D,F = (0*x, 1*y), (1*x, 1*y), (3*x-1, 1*y)
        G,H,I,J,K = (0*x, 2*y-1), (1*x, 2*y-1), (2*x, 2*y), (3*x, 2*y), (4*x-1, 2*y)
        L,M = (2*x, 3*y-1), (3*x, 3*y-1)
        edges = [
            Edge("DC", C, line_len, RIGHT, invert, UP,    "AB"),
            Edge("AB", A, line_len, RIGHT, normal, UP,    "DC"),
            Edge("AE", A, line_len, DOWN,  normal, LEFT,  "DE"),
            Edge("DE", D, line_len, RIGHT, normal, UP,    "AE"),
            Edge("BF", B, line_len, DOWN,  normal, RIGHT, "NK"),
            Edge("NK", K, line_len, DOWN,  invert, RIGHT, "BF"),
            Edge("FJ", F, line_len, DOWN,  normal, RIGHT, "JK"),
            Edge("JK", J, line_len, RIGHT, invert, UP,    "FJ"),
            Edge("CG", C, line_len, DOWN,  normal, LEFT,  "NM"),
            Edge("NM", M, line_len, RIGHT, invert, DOWN,  "CG"),
            Edge("GH", G, line_len, RIGHT, normal, DOWN,  "ML"),
            Edge("ML", L, line_len, RIGHT, invert, DOWN,  "GH"),
            Edge("HI", H, line_len, RIGHT, normal, DOWN,  "IL"),
            Edge("IL", I, line_len, DOWN,  normal, LEFT,  "HI"),
        ]
    else:
        x = (max_x+1)//3
        y = (max_y+1)//4
        line_len = x
        A,B,C = (x,0), (2*x,0), (3*x-1,0)
        D,E1,E2,F = (x,y), (2*x,y-1), (2*x-1,y), (3*x-1,y-1)
        G,I = (0,2*y), (2*x-1,2*y)
        J,K1,K2 = (0,3*y), (x,3*y-1), (x-1,3*y)
        M = (0,4*y-1)
        edges = [
        Edge("AB", A, line_len, RIGHT,  normal, UP,     "JM"),
        Edge("JM", J, line_len, DOWN,   normal, LEFT,   "AB"),
        Edge("BC", B, line_len, RIGHT,  normal, UP,     "MN"),
        Edge("MN", M, line_len, RIGHT,  normal, DOWN,   "BC"),
        Edge("AD", A, line_len, DOWN,   invert, LEFT,   "GJ"),
        Edge("GJ", G, line_len, DOWN,   normal, LEFT,   "AD"),
        Edge("DH", D, line_len, DOWN,   normal, LEFT,   "GH"),
        Edge("GH", G, line_len, RIGHT,  normal, UP,     "DH"),
        Edge("EF", E1, line_len, RIGHT,  normal, DOWN,   "EI"),
        Edge("EI", E2, line_len, DOWN,   normal, RIGHT,  "EF"),
        Edge("CF", C, line_len, DOWN,   invert, RIGHT,  "IL"),
        Edge("IL", I, line_len, DOWN,   normal, RIGHT,  "CF"),
        Edge("KL", K1, line_len, RIGHT,  normal, DOWN,   "KN"),
        Edge("KN", K2, line_len, DOWN,   normal, RIGHT,  "KL"),
        ]


    for x in range(max_x + 1):
        if (x,0) in all_tiles:
            start_pos = vec(x,0)
            break

def draw(curr_pos, dir):
    dir_symbols = ">v<^"
    lines = []
    with open("out.txt", mode="w") as f:
        for y in range(max_y + 1):
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

def solve(puzzle_data):
    init(puzzle_data)
    # hist = ""
    dir = vec(1,0)
    pos = start_pos
    for m,d in zip(islice(path,0,len(path),2), islice(path,1,len(path),2)):
        # print(m, d)
        pos, dir = move(pos, m, dir)
        dir = rotate(dir, d)
        # draw(pos, dir)
        # hist += str(m) + str(d)

    m = path[-1]
    pos, dir = move(pos, m, dir)
    # hist += str(m)
    #print("final pos:", pos[0], pos[1])
    #print(hist)

    return int(sum([1000*(pos[1]+1), 4*(pos[0]+1), all_dirs.index(dir)]))

def solve_puzzle(puzzle_data):
    global PUZZLE_PART_2
    PUZZLE_PART_2 = False
    s1 = solve(puzzle_data)
    PUZZLE_PART_2 = True
    s2 = solve(puzzle_data)
    return s1, s2

if (__name__ == "__main__"):
    # PUZZLE_PART_2 = True
    # init(preprocess(get_reference_data(__file__)))
    # assert (14,8),(0,1) == move_to_associated_edge_part2(vec(11,5), vec(1,0))
    #PUZZLE_PART_2 = False

    global PUZZLE_REFERENCE_DATA
    PUZZLE_REFERENCE_DATA = True

    ref = solve_puzzle(preprocess(get_reference_data(__file__)))
    print_statistics("Reference", ref, expected=(6032, 5031))
    
    PUZZLE_REFERENCE_DATA = False
    # quit()
    sol = solve_puzzle(preprocess(get_puzzle_data(__file__)))
    print_statistics("Solution", sol, expected=(106094, 162038))
