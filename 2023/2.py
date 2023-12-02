from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import operator
from functools import reduce

def preprocess(puzzle):
    '''returns a list of games, where a game is a list of tuples representing the number of cubes in each color'''
    result = []
    for line in puzzle:
        game = []
        moves = line.split(':')[1].split(';')
        for move in moves:
            move_stat = []
            for color in ["red", "green", "blue"]:
                color_info = [ci for ci in move.split(',') if color in ci]
                count = 0
                if len(color_info) > 0:
                    count = int(color_info[0].replace(color, ""))
                move_stat.append(count)
            game.append(tuple(move_stat))
        result.append(game)
    return result

def solve_puzzle(puzzle):
    puzzle = preprocess(puzzle)
    sum1, sum2 = 0, 0
    for game_index, game in enumerate(puzzle, 1):
        max_rgb = [max([move[index] for move in game]) for index in range(3)]

        if all(map(operator.le, max_rgb, [12, 13, 14])):
            sum1 += game_index

        sum2 += reduce(operator.mul, max_rgb)

    return sum1, sum2

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1, ref2 = None, None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(8, 2286))

    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(2076, 70950))
