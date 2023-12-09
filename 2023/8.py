from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re

def preprocess(puzzle):
    directions = list(map(int, puzzle[0].replace("L", "0").replace("R", "1")))
    cmds = {}
    for line in puzzle[2:]:
        for c in ["(", ")", ","]: line = line.replace(c, "")
        m = re.match("(.*) = (.*) (.*)", line)
        cmds.update({m.group(1): (m.group(2), m.group(3))})
    return directions, cmds

def calculate(pos, directions, cmds):
    counter = 0
    dir_index = 0
    while True:
        direction = directions[dir_index % len(directions)]
        counter += 1
        for pos_index in range(len(pos)):
            a = cmds[pos[pos_index]][direction]
            pos[pos_index] = a
        
        if all([p.endswith("Z") for p in pos]):
            break
        dir_index += 1
    return counter

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    directions, cmds = preprocess(puzzle)
    
    part1 = part2 = None
    if solve_part1:
        pos = ["AAA"]
        part1 = calculate(pos, directions, cmds)
    if solve_part2: 
        pos = [p for p in cmds.keys() if p.endswith("A")]
        pos = [pos[0]]
        part2 = calculate(pos, directions, cmds)
    return part1, part2

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    # ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    # print_statistics("Reference", (ref1, ref2), expected=(6, 6))

    sol = solve_puzzle(get_puzzle_data(__file__), solve_part1=False)
    print_statistics("Solution", sol, expected=(12361, None))
