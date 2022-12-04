def get_input_data():
    with open(r"04 Camp Cleanup.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return ["2-4,6-8",
            "2-3,4-5",
            "5-7,7-9",
            "2-8,3-7",
            "6-6,4-6",
            "2-6,4-8"]

def fully_overlap(r1, r2):
    r1 = [int(i) for i in r1]
    r2 = [int(i) for i in r2]
    if r1[0] >= r2[0] and r1[1] <= r2[1]:
        return True
    elif r1[0] <= r2[0] and r1[1] >= r2[1]:
        return True
    else:
        return False

def overlap(r1, r2):
    r1 = [int(i) for i in r1]
    r2 = [int(i) for i in r2]
    for val in r1:
        if r2[0] <= val <= r2[1]:
            return True
    for val in r2:
        if r1[0] <= val <= r1[1]:
            return True
    return False

def solve_puzzle(lines):
    counter1 = 0
    counter2 = 0
    for line in lines:
        ranges = [i for i in line.split(",")]
        if fully_overlap(ranges[0].split("-"), ranges[1].split("-")):
            counter1 += 1
        if overlap(ranges[0].split("-"), ranges[1].split("-")):
            counter2 += 1
    return counter1, counter2

def test_reference1():
    assert solve_puzzle(get_test_data())[0] == 2

def test_reference2():
    assert solve_puzzle(get_test_data())[1] == 4

def test_solution():
    assert solve_puzzle(get_input_data())[0] == 471
    assert solve_puzzle(get_input_data())[1] == 888

def test_ranges():
    assert fully_overlap(["1", "4"], ["2", "3"]) == True
    assert fully_overlap(["2", "3"], ["1", "4"]) == True
    assert fully_overlap(["2", "5"], ["1", "4"]) == False
    assert fully_overlap(["1", "4"], ["2", "5"]) == False

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_input_data())
    print("solution1", s1)
    print("solution2", s2)