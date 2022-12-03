"""Advent of Code day 3"""
#from enum import Enum

filename = r"03 Rucksack Reorganization.txt"

def get_input_data():
    with open(filename, encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return ["vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw"]

def solve_puzzle(lines):
    """solve puzzle"""
    priority = 0
    for line in lines:
        index_half = int(len(line)/2)
        part1 = line[0:index_half]
        part2 = line[index_half:]
        for char in part1:
            if char in part2:
                priority += to_priority(char)
                break
    return priority

def solve_puzzle_part2(lines):
    """solve puzzle"""
    priority = 0
    total = len(lines)
    groups_count = int(total / 3)
    for group_id in range(groups_count):
        group_rucksacks = lines[3*group_id:3*group_id+3]
        for char in group_rucksacks[0]:
            if char in group_rucksacks[1] and char in group_rucksacks[2]:
                priority += to_priority(char)
                break
    return priority

def test_reference_solution_one():
    """test reference solution"""
    data = get_test_data()
    s1 = solve_puzzle(data)
    assert s1 == 157

def test_reference_solution_two():
    """test reference solution"""
    data = get_test_data()
    s2 = solve_puzzle_part2(data)
    assert s2 == 70

def test_solution():
    """test solution"""
    s1 = solve_puzzle(get_input_data())
    s2 = solve_puzzle_part2(get_input_data())
    assert s1 == 8088
    assert s2 == 2522

def to_priority(char):
    if ord(char) >= 97 and ord(char) <= 122:
        return ord(char) - 96
    elif ord(char) >= 65 and ord(char) <= 90:
        return ord(char) - 38

def test_to_prio():
    assert to_priority("a") == 1
    assert to_priority("z") == 26
    assert to_priority("A") == 27
    assert to_priority("Z") == 52
    for char in "abczABCZ":
        print(char, to_priority(char))

if (__name__ == "__main__"):
    s1 = solve_puzzle(get_input_data())
    print("solution1", s1)

    s2 = solve_puzzle_part2(get_input_data())
    print("solution2", s2)
