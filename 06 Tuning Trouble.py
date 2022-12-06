from pathlib import Path

def get_input_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()][0]

def get_test_data():
    return [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz" ]

def solve_puzzle(data):
    result = []
    for l in [4, 14]: #marker length
        for i in range(len(data) - l):
            if len(set(data[i:i + l])) == l:
                result.append(i + l)
                break
    return result

def test_reference():
    assert solve_puzzle(get_test_data()[0])[0] == 7
    assert solve_puzzle(get_test_data()[1])[0] == 5
    assert solve_puzzle(get_test_data()[0])[1] == 19
    assert solve_puzzle(get_test_data()[1])[1] == 23

def test_solution():
    res1, res2 = solve_puzzle(get_input_data())
    assert res1 == 1953
    assert res2 == 2301

if (__name__ == "__main__"):
    test_reference()
    s1, s2 = solve_puzzle(get_input_data())
    print("solution1", s1)
    print("solution2", s2)