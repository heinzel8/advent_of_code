from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass, field
import math
import functools as ft
import operator as op

# HAND_TYPES = [
#     {"FIVE_OF_A_KIND ": "5"},
#     {"FOUR_OF_A_KIND": "41"},
#     {"FULL_HOUSE": "32"},
#     {"THREE_OF_A_KIND": "311"},
#     {"TWO_PAIR": "221"},
#     {"ONE_PAIR": "2111"},
#     {"HIGH_CARD": "11111"},
# ]

HAND_TYPES = ["5","41","32","311","221","2111","11111"][::-1]
CARDS_DEFAULT = "A K Q J T 9 8 7 6 5 4 3 2".split()[::-1]
CARDS_JOKER = "A K Q T 9 8 7 6 5 4 3 2 J".split()[::-1]

global use_joker
use_joker = False

def calculate_hand_type(cards, use_joker):
    CARDS = CARDS_JOKER[1:] if use_joker else CARDS_DEFAULT
    joker_count = cards.count("J") if use_joker else 0

    cards_count = sorted([cards.count(c) for c in CARDS])[::-1]
    cards_count[0] += joker_count
    cards_count = "".join(map(str, cards_count)).replace("0", "")
    
    return HAND_TYPES.index(cards_count)

@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: int = field(init=False)
    def __post_init__(self):
        global use_joker
        self.hand_type = calculate_hand_type(self.cards, use_joker)
        self.bid = int(self.bid)
    

def preprocess(puzzle):
    hands = []
    for line in puzzle:
        hands.append(Hand(*line.split()))
    return hands

def cmp(v1, v2):
    if (diff := v1 - v2) == 0:
        return 0
    return math.copysign(1, diff)

def compare_hands(hand1:Hand, hand2:Hand):
    if (diff := cmp(hand1.hand_type, hand2.hand_type)) != 0:
        return diff
    
    CARDS = CARDS_JOKER if use_joker else CARDS_DEFAULT
    for c1, c2 in zip(hand1.cards, hand2.cards):
        if (diff:=cmp(CARDS.index(c1), CARDS.index(c2))) != 0:
            return diff
    return 0

def solve_puzzle(puzzle):
    global use_joker
    results = []
    for use_joker in [False, True]:
        hands = preprocess(puzzle)
        hands = sorted(hands, key=ft.cmp_to_key(compare_hands))
        values = []
        for index, hand in enumerate(hands, 1):
            values.append(hand.bid * index)
        results.append(ft.reduce(op.add, values))
    return results

def run_tests():
    h1 = h2 = Hand("32T3K", 1)
    assert(0 == compare_hands(h1, h2))
    
    h1, h2 = Hand("KK677", 1), Hand("KTJJT", 1)
    assert(1 == compare_hands(h1, h2))

    assert(5 == calculate_hand_type("T55J5", use_joker=True))

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(6440, 5905))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(251136060, 249400220))
