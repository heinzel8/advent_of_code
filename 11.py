from pathlib import Path
import re
import math

def get_puzzle_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data():
    with open(Path(__file__).stem + f"_reference.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

class Monkey:
    id = 0
    items = []
    operation = ""
    test_divide_by = 0
    target_true = 0
    target_false = 0
    inspected_count = 0


def preprocess(puzzle):
    s_items = "Starting items: "
    s_op = "Operation: new = "
    s_test = "Test: divisible by "
    s_true = "If true: throw to monkey "
    s_false = "If false: throw to monkey "

    monkeys = []
    for line in puzzle:
        if line.startswith("Monkey"):
            monkeys.append(Monkey())
            monkeys[-1].id = int(re.findall(r"\d", line)[0])
        elif line.startswith(s_items):
            monkeys[-1].items = [int(i) for i in line[len(s_items):].split(",")]
        elif line.startswith(s_op):
            monkeys[-1].operation = line[len(s_op):]
        elif line.startswith(s_test):
            monkeys[-1].test_divide_by = int(line[len(s_test):])
        elif line.startswith(s_true):
            monkeys[-1].target_true = int(line[len(s_true):])
        elif line.startswith(s_false):
            monkeys[-1].target_false = int(line[len(s_false):])
    return monkeys

def solve_puzzle(puzzle, rounds_count, relief):
    monkeys = preprocess(puzzle)
    hcf = math.prod([m.test_divide_by for m in monkeys]) # highest common factor 

    for round in range(rounds_count):
        for m in monkeys:
            for item in m.items:
                item = eval(m.operation.replace("old", "item"))
                item //= relief
                item = item % hcf
                target_monkey = m.target_true if item % m.test_divide_by == 0 else m.target_false
                monkeys[target_monkey].items.append(item)
                m.inspected_count += 1
            m.items = []

    inspections = [m.inspected_count for m in monkeys]
    inspections = sorted(inspections, reverse=True)
    res1 = inspections[0] * inspections[1]

    return res1

def test_reference():
    s1 = solve_puzzle(get_reference_data(), rounds_count=20, relief=3)
    s2 = solve_puzzle(get_reference_data(), rounds_count=10000, relief=1)
    assert s1 == 10605
    assert s2 == 2713310158

def test_solution():
    s1 = solve_puzzle(get_puzzle_data(), rounds_count=20, relief=3)
    s2 = solve_puzzle(get_puzzle_data(), rounds_count=10000, relief=1)
    assert s1 == 182293
    assert s2 == 54832778815

if (__name__ == "__main__"):
    s1 = solve_puzzle(get_puzzle_data(), rounds_count=20, relief=3)
    s2 = solve_puzzle(get_puzzle_data(), rounds_count=10000, relief=1)
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")