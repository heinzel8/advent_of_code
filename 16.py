# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=C0303
# pylint: disable=C0301
# pylint: disable=C0116
# pylint: disable=C0115

from pathlib import Path
import re
from copy import deepcopy

ALL_VALUES = ""

def get_puzzle_data():
    """function"""
    with open(Path(__file__).stem + ".txt", encoding="utf8") as file:
        return [line.strip() for line in file.readlines()]

def get_reference_data():
    """function"""
    with open(Path(__file__).stem + "_reference.txt", encoding="utf8") as file:
        return [line.strip() for line in file.readlines()]

def test(puzzle, expected1, expected2, prefix = ""):
    """function"""
    s_1, s_2 = solve_puzzle(puzzle)
    if prefix != "":
        print(prefix)
    for i in [1, 2]:
        _s = str(eval(f"str(s{i})")) # pylint: disable=W0123
        exp = str(eval(f"expected{i}")) # pylint: disable=W0123
        app = "  PASS" if _s == exp else "  FAIL - should be " + exp
        print(f"solution {i}: " + _s + " " + app)
        
    if __name__ != "__main__":
        assert s_1 == expected1
        assert s_2 == expected2

def test_reference():
    puzzle = preprocess(get_reference_data())
    test(puzzle, expected1="", expected2="", prefix="reference")

def test_solution():
    puzzle = preprocess(get_puzzle_data())
    test(puzzle, expected1="", expected2="")

def preprocess(puzzle):
    pattern = r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    puzzle = [re.search(pattern, line).groups() for line in puzzle]
    return [[id, int(flow_rate), targets.split(", ")] for [id, flow_rate, targets] in puzzle]

class Valve:
    my_id:str = ""
    flow_rate:int = 0
    targets:list = []

    def __init__(self, my_id:str, flow_rate:int, targets:list):
        self.my_id = my_id
        self.flow_rate = flow_rate
        self.targets = targets

class Status:
    def __init__(self, curr_valve:str, opened_valves:set, time_left:int, trace:str):
        self.curr_valve_id = curr_valve
        self.opened_valves = opened_valves
        self.time_left = time_left
        self.trace = trace

    curr_valve_id:str = ""
    opened_valves:set = set()
    time_left:int = 0
    total_released:int = 0
    trace:str = ""

def calc_flow(opened_valves):
    return sum([ALL_VALUES[id].flow_rate for id in opened_valves])

def solve_puzzle(puzzle):
    global ALL_VALUES # pylint: disable=W0603
    ALL_VALUES = dict()
    for _id, flow_rate, targets in puzzle:
        ALL_VALUES.update({_id: Valve(_id, flow_rate, targets)})

    paths:list(Status) = [Status("AA", set(["AA"]), 30, "AA")]

    i = 0
    while i < len(paths):
        if paths[i].time_left == 0 or len(paths[i].opened_valves) == 10:
            i += 1
            continue
        stat = deepcopy(paths[i])
        if stat.curr_valve_id not in stat.opened_valves and ALL_VALUES[stat.curr_valve_id].flow_rate > 0:
            stat.time_left -= 1
            stat.total_released += calc_flow(stat.opened_valves)
            stat.trace += "+"
        else:
            stat.trace += "_"

        stat.opened_valves.add(stat.curr_valve_id)
        if stat.time_left == 0 or len(paths[i].opened_valves) == 10:
            i += 1
            continue

        # go to next valve
        next_targets = ALL_VALUES[paths[i].curr_valve_id].targets[:]
        next_targets = [t for t in next_targets if t not in stat.opened_valves]
        if len(next_targets) == 0:
            next_targets = ALL_VALUES[paths[i].curr_valve_id].targets[:]
        for next_valve_id in next_targets:
            new_stat = deepcopy(stat)
            new_stat.curr_valve_id = next_valve_id
            new_stat.time_left -= 1
            new_stat.total_released += calc_flow(new_stat.opened_valves)
            new_stat.trace += next_valve_id
            paths.append(new_stat)
        i += 1

    max_released = 0
    for stat in paths:
        max_released = max(max_released, stat.total_released + stat.time_left * calc_flow(stat.opened_valves))

    return "", ""

if __name__ == "__main__":
    test_reference()
    # print("="*28)
    # test_solution()
