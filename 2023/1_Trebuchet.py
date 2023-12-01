from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from pathlib import Path
import re

DIGIT_NAMES = "one two three four five six seven eight nine".split(" ")

def get_digit(s, detect_words, search_from_right):
    if len(s) == 1 and s.isdigit():
        return int(s)

    if not detect_words:
        return None
    
    while len(s) >= 3:
        for d in DIGIT_NAMES:
            if len(s) < len(d): continue
            sub = s[len(s)-len(d):] if search_from_right else s[:len(d)]
            if d == sub: return DIGIT_NAMES.index(d)+1
        s = s[0:-1] if search_from_right else s[1:]
    return None

def get_first_digit(line, detect_words=False):
    splits = re.split("(\d)", line)
    for candidate in splits:
        if (d:=get_digit(candidate, detect_words, search_from_right=False)) is not None:
            return d
    return None

def get_last_digit(line, detect_words=False):
    splits = re.split("(\d)", line)
    for candidate in splits[::-1]:
        if (d:=get_digit(candidate, detect_words, search_from_right=True)) is not None:
            return d
    return None

def solve_puzzle(puzzle, part):
    detect_words = False if part == 1 else True
    sum = 0
    for line in puzzle:
        first = get_first_digit(line, detect_words)
        last = get_last_digit(line, detect_words)
        sum += int(f"{first}{last}")
    return sum

def run_tests():

    cases = [
        ("a2oneasd", 2, 2, 2, 1),
        ("aoneb2345bdf2cthrees", 2, 1, 2, 3),
        ("eightwothree", None, 8, None, 3),
        ]

    for test,fwo,fw,lwo,lw in cases:
        assert(get_first_digit(test, detect_words=False) == fwo)
        assert(get_first_digit(test, detect_words=True) == fw)
        assert(get_last_digit(test, detect_words=False) == lwo)
        assert(get_last_digit(test, detect_words=True) == lw)

if (__name__ == "__main__"):
    run_tests()

    ref1 = solve_puzzle(get_reference_data(__file__, part=1), part=1)
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), part=2)
    print_statistics("Reference", (ref1, ref2), expected=(142, 281))

    sol1 = solve_puzzle(get_puzzle_data(__file__), part=1)
    sol2 = solve_puzzle(get_puzzle_data(__file__), part=2)
    print_statistics("Solution", (sol1, sol2), expected=(54634, 53855))

    if not sol2 > 53845:
        print("FAIL: solution is not greater 53845")

    if not sol2 < 53887:
        print("FAIL: solution is not less than 53887")
