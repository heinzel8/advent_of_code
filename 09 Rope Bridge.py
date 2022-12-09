from pathlib import Path

x = 0
y = 1

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data(id):
    with open(Path(__file__).stem + f"_test{id}.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def move(item, dir):
    if dir == "R":
        item[x] += 1
    if dir == "L":
        item[x] -= 1
    if dir == "U":
        item[y] += 1
    if dir == "D":
        item[y] -= 1
    return item

def solve_puzzle(puzzle, knot_count):
    rope = []
    for i in range(knot_count):
        rope.append([0,0])
    tail = knot_count-1
    tail_trace = set()

    for instruction in puzzle:
        for _count in range(int(instruction[2:])):
            rope[0] = move(rope[0], dir = instruction[0])
            for knot in range(1, knot_count):
                dx = rope[knot-1][x] - rope[knot][x]
                dy = rope[knot-1][y] - rope[knot][y]
                if max(abs(dx), abs(dy)) > 1:
                    if abs(dx) > 0:
                        dx //= abs(dx)
                    if abs(dy) > 0:
                        dy //= abs(dy)
                    rope[knot][x] += dx
                    rope[knot][y] += dy
                tail_trace.add(str(rope[tail]))
        
    return len(tail_trace)

def test_reference():
    assert solve_puzzle(get_test_data(1), knot_count=2) == 13
    assert solve_puzzle(get_test_data(2), knot_count=10) == 36

def test_solution():
    assert solve_puzzle(get_puzzle_data(), knot_count=2) == 5981
    assert solve_puzzle(get_puzzle_data(), knot_count=10) == 2352

if (__name__ == "__main__"):
    s1 = solve_puzzle(get_puzzle_data(), knot_count=2)
    s2 = solve_puzzle(get_puzzle_data(), knot_count=10)
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")