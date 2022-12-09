from pathlib import Path
from pygame import Vector2 as vec

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip().split() for line in f.readlines()]

def get_test_data(id):
    with open(Path(__file__).stem + f"_test{id}.txt", encoding="utf8") as f:
        return [line.strip().split() for line in f.readlines()]

def solve_puzzle(puzzle, knot_count):
    rope = [vec(0,0)]*knot_count
    tail = knot_count-1
    tail_trace = set()
    DIRS = dict(L=vec(0,-1), R=vec(0,1), U=vec(1,0), D=vec(-1,0))

    for dir_str, count in puzzle:
        for _ in range(int(count)):
            rope[0] = rope[0] + DIRS[dir_str]
            for knot in range(1, knot_count):
                diff = rope[knot-1] - rope[knot]
                if max(abs(diff.x), abs(diff.y)) > 1:
                    if abs(diff.x) > 0: diff.x //= abs(diff.x)
                    if abs(diff.y) > 0: diff.y //= abs(diff.y)
                    rope[knot] = rope[knot] + diff
                tail_trace.add(str(rope[tail]))
        
    return len(tail_trace)

def test_reference():
    assert solve_puzzle(get_test_data(1), knot_count=2) == 13
    assert solve_puzzle(get_test_data(2), knot_count=10) == 36

def test_solution():
    assert solve_puzzle(get_puzzle_data(), knot_count=2) == 5981
    assert solve_puzzle(get_puzzle_data(), knot_count=10) == 2352

if (__name__ == "__main__"):
    s1 = solve_puzzle(get_test_data(1), knot_count=2) == 13
    s1 = solve_puzzle(get_puzzle_data(), knot_count=2)
    s2 = solve_puzzle(get_puzzle_data(), knot_count=10)
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")