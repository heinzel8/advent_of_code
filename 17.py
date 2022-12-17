from pathlib import Path
from copy import deepcopy

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
    test(puzzle, expected1=3068, expected2=1514285714288, prefix="reference")

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1=3202, expected2="")

def preprocess(puzzle):
    res = []
    for c in puzzle[0]:
        res.append(-1 if c=="<" else 1)
    return res
    
class Block:
    def __init__(self, shape, x_offs_max) -> None:
        self.shape = shape
        self.x_offs_max = x_offs_max
    shape = []
    x_offs_max = 0
    x = 0
    y = 0

def solve_puzzle(puzzle):
    b1 = Block([[1,1,1,1]], 0)
    b2 = Block([[0,1,0,0],[1,1,1,0],[0,1,0,0]], 1)
    b3 = Block([[1,1,1,0],[0,0,1,0],[0,0,1,0]], 1)
    b4 = Block([[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], 3)
    b5 = Block([[1,1,0,0],[1,1,0,0]], 2)

    blocks = [b1, b2, b3, b4, b5]
    stack = []
    stream = puzzle
    stream_index = 0

    for block_id in range(2022):
        block = deepcopy(blocks[block_id%len(blocks)])
        block.x = 2
        block.y = len(stack) + 3
        if (stream_index) % len(stream) == 0:
            pass
        while True:
            push(block, stream[stream_index], stack)
            stream_index = (stream_index + 1) % len(stream)
            if (stream_index == 0):
                pass
            if not fall(block, stack):
                print_stack(stack)
                break
        # if block_id % 10_000 == 0:
        #     print(block_id, end="\r")
        # if block_id == 2022:
        #     res1 = len(stack)
    
    return len(stack), len(stack)

def put_on_stack(stack_block, block_y, stack):
    stack_top_y = len(stack)-1
    for i, y in enumerate(range(block_y, block_y + len(stack_block))):
        if y <= stack_top_y:
            for col in range(len(stack[y])):
                stack[y][col] = 1 if stack_block[i][col] or stack[y][col] else 0
        else:
            stack.append(stack_block[i])

def push(block:Block, dir, stack):
    max_x = 7 - 4 + block.x_offs_max
    if 0 <= block.x + dir <= max_x:
        stack_block = generate_stack_block(block, dir)
        if not collides(block.y, stack_block, stack):
            block.x += dir

def fall(block:Block, stack) -> bool:
    stack_top_y = len(stack)-1
    if block.y - 1 > stack_top_y:
        block.y -= 1
        return True
    
    stack_block = generate_stack_block(block)
    if collides(block.y-1, stack_block, stack):
        put_on_stack(stack_block, block.y, stack)
        return False
    else:
        block.y -= 1
        return True

def generate_stack_block(block, x_offset=0):
    new_block = []
    for block_line in block.shape:
        new_line = [0,0,0,0,0,0,0]
        f = block.x + x_offset
        t = min(block.x + 4 + x_offset, 7)
        for i, j in enumerate(range(f, t)):
            new_line[j] = block_line[i]
        new_block.append(new_line)
    return new_block

def print_stack(stack):
    with open("out.txt", mode="w") as f:
        for line in stack[::-1]:
            f.write("|")
            f.write("".join(map(str,line)).replace("0", ".").replace("1", "#"))
            f.write("|\n")
        f.flush()

def collides(y_block, block:list, stack) -> bool:
    y_stack = len(stack) - 1
    if y_stack < y_block:
        return False
    if y_stack < 0:
        return True
    for i, y in enumerate(range(y_block, min(y_block + len(block), y_stack+1))):
        stack_line = stack[y]
        block_line = block[i]
        for col in range(7):
            if stack_line[col] and block_line[col]:
                return True
    return False

if (__name__ == "__main__"):
    test_reference()
    print("="*28)
    test_solution()