from pathlib import Path

SCREEN_HEIGHT = 6

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_puzzle_data():
    file_name = Path(__file__).stem + f"_reference.txt"
    with open(file_name, encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_solution():
    file_name = Path(__file__).stem + f"_reference_solution.txt"
    with open(file_name, encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_solution2():
    file_name = Path(__file__).stem + f"_solution2.txt"
    with open(file_name, encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def solve_puzzle(puzzle):
    register_x = 1
    cycles = []
    for instruction in puzzle:
        cycles.append(register_x)
        if instruction.startswith("addx"):
            cycles.append(register_x)
            register_x += int(instruction.split()[1])

    res1 = sum([cycles[i-1]*i for i in [20, 60, 100, 140, 180, 220]])
    screen_width = len(cycles) // SCREEN_HEIGHT

    pixels = ""
    for pixel_id in range(len(cycles)):
        sprite_pos = cycles[pixel_id]
        row = pixel_id % screen_width
        if row >= (sprite_pos-1) and row <= (sprite_pos+1):
            pixels += "#"
        else:
            pixels += "."
        if (len(pixels)-6) % screen_width == 0:
            pixels += "\n"
    
    screen = []
    for line in range(SCREEN_HEIGHT):
        f = line * screen_width
        t = f + screen_width
        screen.append("".join(pixels[f:t]))
    return res1, pixels

def test_reference():
    res1, res2 = solve_puzzle(get_reference_puzzle_data())
    assert res1 == 13140
    assert res2 == get_reference_solution()

def test_solution():
    res1, res2 = solve_puzzle(get_puzzle_data())
    assert res1 == 14760
    assert res2 == get_solution2()

if (__name__ == "__main__"):
    res1, res2 = solve_puzzle(get_puzzle_data())
    print(f"solution1: {res1}")
    print(f"solution2:")
    print(res2)