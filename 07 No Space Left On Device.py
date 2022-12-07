from pathlib import Path
import re

def get_input_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    with open(Path(__file__).stem + " reference.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def solve_puzzle(lines):
    dirs = {}
    curr_dir = "."
    i = 0
    for line in lines:
        i += 1
        if line.startswith("$"):
            if line == "$ cd /":
                curr_dir = "."
            elif line == "$ cd ..":
                curr_dir = "/".join(curr_dir.split("/")[0:-1])
            elif line.startswith("$ cd"):
                curr_dir += "/" + line[5:]
            elif line == "$ ls":
                continue
            else:
                raise Exception(f"unknown command in line {i}")
        s = re.findall("\\d+", line)
        if len(s) > 0:
            splits = curr_dir.split("/")
            for i in range(len(splits)):
                size = int(s[0])
                dir = "/".join(splits[0:i+1])
                if dir in dirs.keys():
                    size += dirs[dir]
                dirs.update({dir: size})

    sum = 0
    for d, s in dirs.items():
        if s < 100000:
            sum += s
    
    size_of_root = int(dirs["."])
    
    needed_space = abs(70000000 - 30000000 - size_of_root)
    sizes = sorted([s for _,s in dirs.items()])
    for s in sizes:
        print(s)
    for size in sizes:
        if size >= needed_space:
            file_to_delete = size
            break

    return sum, file_to_delete

def test_reference():
    res1, res2 = solve_puzzle(get_test_data())
    assert res1 == 95437
    assert res2 == 24933642

def test_solution():
    res1, res2 = solve_puzzle(get_input_data())
    assert res1 == 1513699
    assert res2 == 7991939

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_input_data())
    print("solution1", s1)
    print("solution2", s2)