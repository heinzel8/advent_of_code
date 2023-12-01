from pathlib import Path
from copy import deepcopy

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
    return [((id, int(val))) for id, val in enumerate(puzzle)]

def mix(numbers):
    for i in range(len(numbers)):
        item = [e for e in numbers if e[0] == i][0]
        _,v = item
        ci = numbers.index(item)
        target_index = ci+v

        if target_index < 0 or target_index > (len(numbers)-1):
            target_index = target_index % (len(numbers)-1)

        if ci > target_index:
            numbers.remove(item)
            numbers.insert(target_index, item)
        if ci < target_index:
            numbers.remove(item)
            numbers.insert(target_index, item)

def calculate_results(numbers):
    oi, v = [e for e in numbers if e[1] == 0][0]
    index_0 = numbers.index((oi,v))
    return sum([numbers[(index_0+n)%len(numbers)][1] for n in [1000, 2000, 3000]])

def solve_puzzle(puzzle):
    numbers1 = deepcopy(puzzle)
    mix(numbers1)
    s1 = calculate_results(numbers1)
    
    key = 811589153
    numbers2 = [(i,v*key) for i,v in deepcopy(puzzle)]
    for n in range(10):
        mix(numbers2)
    s2 = calculate_results(numbers2)
    return s1, s2, numbers1, numbers2

def print_statistics(description, value, expected):
    print("="*48)
    for n in range(2):
        result = ""
        if expected[n] is not None:
            result = f"(PASS)" if value[n] == expected[n] else f"(FAIL) expected {expected[n]}"
        print(f"{description} {n+1}: ", value[n], result)

if (__name__ == "__main__"):
    ref = solve_puzzle(get_reference_data())
    print_statistics("Reference", ref, expected=(3, 1623178306))
    
    sol = solve_puzzle(get_puzzle_data())
    print_statistics("Solution",  sol, expected=(7004, 17200008919529))

    print()
    number_sequence = ",".join([str(e[1]) for e in ref[2]])
    print(f"number_sequence={number_sequence}")
    assert(number_sequence == "-2,1,2,-3,4,0,3")

    number_sequence = ",".join([str(e[1]) for e in ref[3]])
    print(f"number_sequence={number_sequence}")
    assert(number_sequence == "-2434767459,1623178306,3246356612,-1623178306,2434767459,811589153,0")
