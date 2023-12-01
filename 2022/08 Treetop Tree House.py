from pathlib import Path

def test_reference():
    res1, res2 = solve_puzzle(get_test_data())
    #assert res1 == 0
    #assert res2 == 0

def test_solution():
    res1, res2 = solve_puzzle(get_input_data())
    assert res1 == 1816
    assert res2 == 383520

def get_input_data():
    with open(Path(__file__).stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return ["", ""]

def solve_puzzle(input):
    visible_from_left = True
    visible_from_right = True
    visibles = []
    scores = []

    
    i = 0
    for row in input:
        visibles.append([0])
        scores.append([])
        for col in input:
            visibles[i].append(True)
            #scores[i].append(0)
        i += 1

    #visible from
    max_col = len(input[0])
    max_row = len(input)

    for col in range(0, max_col):
        for row in range(0, max_row):
            vl = vr = vu = vd = True #visible
            dl = dr = du = dd = 0 #distance
            tree = int(input[row][col])
            for left in range(col-1, -1, -1):
                cmp = int(input[row][left])
                dl = col
                if tree <= cmp:
                    vl = False
                    dl = col-left
                    break
            for right in range(col+1, max_col):
                cmp = int(input[row][right])
                dr = max_col - col - 1
                if tree <= cmp:
                    vr = False
                    dr = right-col
                    break
            for up in range(row-1, -1, -1):
                cmp = int(input[up][col])
                du = row
                if tree <= cmp:
                    vu = False
                    du = row-up
                    break
            for down in range(row+1, max_row):
                cmp = int(input[down][col])
                dd = max_row - row - 1
                if tree <= cmp:
                    vd = False
                    dd = down-row
                    break
            if not vl and not vr and not vu and not vd:
                visibles[row][col] = False
            scores[row][col] = du * dd * dr * dl

    sum = 0
    for row in visibles:
        for item in row:
            sum += item

    max_score = 0
    for row in scores:
        for item in row:
            max_score = max(item, max_score)

    for row in scores:
        print(row)

    return sum, max_score

if (__name__ == "__main__"):
    s1, s2 = solve_puzzle(get_input_data())
    print(f"solution1: {s1}")
    print(f"solution2: {s2}")