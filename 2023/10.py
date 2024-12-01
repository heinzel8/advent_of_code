from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def get_connected_neighbors(symbol, pos):
    x, y = pos
    N = (x, y-1)
    S = (x, y+1)
    E = (x+1, y)
    W = (x-1, y)
    match symbol:
        case "|": return (N, S)
        case "-": return (E, W)
        case "L": return (N, E)
        case "J": return (N, W)
        case "7": return (S, W)
        case "F": return (S, E)
        case _  : return ((None, None), (None, None))

def get_connected_neighbors_from_map(pipe_map, pos):
    neighbors = []
    x, y = pos
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (x,y) in pipe_map[y+dy][x+dx]:
                neighbors.append((x+dx, y+dy))
    return neighbors

def preprocess(puzzle):
    pipe_map = []
    for y, line in enumerate(puzzle):
        pipe_map.append([])
        for x, symbol in enumerate(line):
            pipe_map[-1].append(get_connected_neighbors(symbol, (x, y)))
            if "S" == line[x]:
                start_pos = (x, y)
    return pipe_map, start_pos

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    pipe_map, start_pos = preprocess(puzzle)
    results = [None, None]

    current_pos = start_pos
    pipe = [current_pos]
    pipe.append(get_connected_neighbors_from_map(pipe_map, start_pos)[0])

    while pipe[-1] != start_pos:
        x, y = pipe[-1]
        candidates = [n for n in pipe_map[y][x] if (n[0], n[1]) not in pipe[-2:]]
        pipe.append(candidates[0])
    results[0] = int(len(pipe)/2)

    return results

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(8, None))

    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(6786, None))
