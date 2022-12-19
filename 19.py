from pathlib import Path
import re
from copy import deepcopy

def print_statistics(r1, r2, s1, s2, exp_r1, exp_r2, exp_s1, exp_s2):
    print("solution 1: ", r1, " PASS" if r1==exp_r1 else "")
    print("solution 2: ", r2, " PASS" if r2==exp_r2 else "")
    print("solution 1: ", s1, " PASS" if s1==exp_s1 else "")
    print("solution 2: ", s2, " PASS" if s2==exp_s2 else "")
    #test_reference()
    #print("="*28)
    #test_solution()

def get_puzzle_data():
    stem = Path(__file__).stem
    if stem == "template": return ""
    with open(stem + ".txt", encoding="utf8") as f:
        return preprocess([line.strip() for line in f.readlines()])

def get_reference_data():
    stem = Path(__file__).stem
    if stem == "template": return ""
    with open(stem + f"_reference.txt", encoding="utf8") as f:
        return preprocess([line.strip() for line in f.readlines()])

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
    test(puzzle, expected1="", expected2="", prefix="reference")

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1="", expected2="")

def preprocess(puzzle):
    blueprints = []
    pattern = "Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    for line in puzzle:
        res = re.search(pattern, line)
        g = res.groups()
        blueprint = []
        blueprint.append([int(g[0]),  0,            0,          0])
        blueprint.append([int(g[1]),  0,            0,          0])
        blueprint.append([int(g[2]),  int(g[3]),    0,          0])
        blueprint.append([int(g[4]),  0,            int(g[5]),  0])
        blueprints.append(blueprint)
    print(blueprints)
    return blueprints

    #blueprint.update()
    return puzzle

ore = 0
clay = 1
obsidian = 2
geode = 3

one_robot = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

def produce_robots(resources, blueprint):
    resources = deepcopy(resources)
    new_robots = []
    next = True
    while next:
        next = False
        for robot_type in reversed(range(4)):
            costs = blueprint[robot_type]
            check = [resources[i] >= costs[i] for i in range(4)]
            if all(check):
                new_robots.append([one_robot[robot_type], costs])
                resources = [resources[type] - costs[type] for type in range(4)]
                next = True
    return new_robots


def calculate(blueprint):
    resources = [0,0,0,0]
    robots = [1,0,0,0]
    min_left = 24
    
    stack = [(resources, robots, min_left)]
    stack_index = 0

    while True:
        resources, robots, min_left = stack[stack_index]
        if min_left == 0:
            continue

        new_robots = produce_robots(resources, blueprint)
        for r in new_robots:
            res = deepcopy(resources)
            new_robot, cost = r
            res = [res[type] - cost[type] for type in range(4)]
            res = [res[type] + robots[type] for type in range(4)]
            robots = [r1 + r2 for r1, r2 in zip(robots, new_robot)]
            stack.append((res, robots, min_left-1))

        resources = deepcopy(resources)
        resources = [resources[type] + robots[type] for type in range(4)]
        stack.append((resources, robots, min_left-1))
        del(stack[0])
        print("stack size:", len(stack), end="\r")
        if len(stack) == 0:
            break


def solve_puzzle(puzzle):
    for blueprint in puzzle:
        calculate(blueprint)
    return None, None

if (__name__ == "__main__"):

    l1 = [1,2,3]
    l2 = [2,3,4]
    l = [el1 + el2 for el1, el2 in zip(l1,l2)]

    exp_r1, exp_r2 = None, None
    exp_s1, exp_s2 = None, None

    r1, r2 = solve_puzzle(get_reference_data())
    s1, s2 = solve_puzzle(get_puzzle_data())
    
    print_statistics(r1, r2, s1, s2, exp_r1, exp_r2, exp_s1, exp_s2)
