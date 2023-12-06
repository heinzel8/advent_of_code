from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re

def preprocess(puzzle):
    time = list(map(int, re.findall('\d+', puzzle[0])))
    distance = list(map(int, re.findall('\d+', puzzle[1])))
    return time, distance

def calculate(times, distances):
    result = 1
    for race_time, best_distance in zip(times, distances):
        win_count = 0
        for push_time in range(1, race_time):
            speed = push_time
            distance = speed * (race_time-push_time)
            if distance > best_distance:
                win_count += 1
        result *= win_count
    return result

def solve_puzzle(puzzle):
    times, distances = preprocess(puzzle)
    part1 = calculate(times, distances)

    times = [int("".join(map(str, times)))]
    distances = [int("".join(map(str, distances)))]
    part2 = calculate(times, distances)
    return part1, part2

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(288, 71503))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(1624896, 32583852))
