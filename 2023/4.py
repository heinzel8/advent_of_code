from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from functools import reduce
import operator

def preprocess(puzzle):
    return puzzle

def solve_puzzle(puzzle):
    part1 = 0

    cards_count = {}
    for card_id in range(len(puzzle)):
        cards_count.update({card_id+1: 1})

    for card_id, line in enumerate(puzzle, 1):
        score_part1 = score_part2 = 0
        numbers = line.split(":")[1].split("|")
        win_numbers = list(map(int, numbers[0].split()))
        my_numbers = list(map(int, numbers[1].split()))
        for my_number in my_numbers:
            if my_number in win_numbers:
                score_part1 = score_part1 * 2 if score_part1 > 0 else 1
                score_part2 += 1
        part1 += score_part1
        
        for next in range(score_part2):
            next_card_id = card_id+next+1
            inc = cards_count[card_id]
            if next_card_id > len(puzzle):
                break
            cards_count.update({next_card_id: cards_count[next_card_id]+inc})
    
    part2 = reduce(operator.add, cards_count.values())

    return part1, part2

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(13, 30))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(27454, 6857330))
