from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def preprocess(puzzle):
    mapp = []
    for line in puzzle:
        line = line.strip()
        mapp.append(list(map(int, line)))
    return mapp

def find_trailheads(mapp):
    trailheads = []
    for y in range(len(mapp)):
        for x in range(len(mapp[y])):
            if mapp[y][x] == 0:
                trailheads.append((x, y))
    return trailheads

def is_on_map(mapp, x, y):
    if 0 <= x < len(mapp[0]) and 0 <= y < len(mapp):
        return True
    return False

def print_map(mapp, point):
    with open("map.txt", "w") as f:
        for y in range(len(mapp)):
            for x in range(len(mapp[0])):
                if (x, y) == point:
                    f.write("x")
                else:
                    f.write(str(mapp[y][x]))
            f.write("\n")

def walk(mapp, start_point, peaks:set[(int, int)]):
    x, y = start_point
    if mapp[y][x] == 9:
        peaks.add((x,y))
        return 1
    neighbors = [[x+1,y], [x-1,y], [x,y+1], [x,y-1]]
    neighbors = [n for n in neighbors if is_on_map(mapp, *n)]
    sum = 0
    for nx, ny in neighbors:
        if mapp[ny][nx] == mapp[y][x] + 1:
            print_map(mapp, (nx, ny))
            sum += walk(mapp, (nx, ny), peaks)
    return sum


def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    mapp = preprocess(puzzle)
    r1, r2 = None, None

    r1, r2 = 0, 0
    heads = find_trailheads(mapp)
    for head in heads:
        peaks = set()
        val = walk(mapp, head, peaks)
        r1 += len(peaks)
        r2 += val

    return r1, r2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(36, 81))

    solution = None, None
    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(825, 1805))
