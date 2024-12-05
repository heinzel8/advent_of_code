from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def preprocess(puzzle):
    rules = []
    updates = []
    for line in puzzle:
        if "|" in line:
            rules.append(list(map(int, line.split("|"))))
        elif "," in line:
            updates.append(list(map(int, line.split(","))))

    return rules, updates

def rules_violated(v1, v2, rules):
    for rule in rules:
        if v2 == rule[0] and v1 == rule[1]:
            return True 
    return False

def sort_update(update, rules):
    good = True
    for i1, v1 in enumerate(update):
            for i2, v2 in enumerate(update[i1+1:], i1+1):
                if rules_violated(v1, v2, rules):
                    update[i1], update[i2] = update[i2], update[i1]
                    good = False
    return good

def update_is_correct(update, rules):
    for i1, v1 in enumerate(update):
            for v2 in update[i1+1:]:
                if rules_violated(v1, v2, rules):
                    return False
    return True

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    rules, updates = preprocess(puzzle)
    r1, r2 = 0, 0

    for update in updates:
        if update_is_correct(update, rules):
            r1 += update[int(len(update)/2)]
        else:
            good = False
            while(not good):
                good = sort_update(update, rules)
            r2 += update[int(len(update)/2)]

    return r1, r2

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(143, 123))

    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(5509, 4407))
