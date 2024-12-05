from aoc_utils import get_puzzle_data, get_reference_data, print_statistics

def preprocess(puzzle):
    return puzzle

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    puzzle = preprocess(puzzle)
    r1,r2 = 0, 0

    directions = [[1,0], [0,1], [-1,0], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]]
    word_range = range(0, 4)
    for row, line in enumerate(puzzle):
        for col, c in enumerate(line):
            if c == "X":
                words = get_words(puzzle, col, row, directions, word_range)
                r1 += words.count("XMAS")

    directions = [[1, 1], [-1, 1]]
    word_range = range(-1, 2)
    for row, line in enumerate(puzzle):
        for col, c in enumerate(line):
            if c == "A":
                words = get_words(puzzle, col, row, directions, word_range)
                if 2 == words.count("MAS") + words.count("SAM"):
                    r2 += 1

    return r1, r2

# directions in col, row


def get_words(puzzle, col, row, directions, word_range):
    max_col = len(puzzle[0])
    max_row = len(puzzle)
    words = []
    for dcol, drow in directions:
        word = ""
        for magnitude in word_range:
            new_col, new_row = col + dcol*magnitude, row + drow*magnitude
            if 0 <= new_col < max_col and 0 <= new_row < max_row:
                word += puzzle[new_row][new_col]
            else:
                break
        words.append(word)
    return words

def run_tests():
    assert(1 == 1)
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(18, 9))

    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(2530, 1921))
