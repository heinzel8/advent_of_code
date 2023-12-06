from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass, field
import sys
import re

@dataclass
class RangeData:
    dest_range_start: int
    source_range_start: int
    range_length: int
    def in_source_range(self, value):
        return value >= self.source_range_start and value < self.source_range_start + self.range_length
    def in_target_range(self, value):
        return value >= self.dest_range_start and value < self.dest_range_start + self.range_length

@dataclass
class MapData:
    name : str
    ranges: list = field(default_factory=list)
    def transform(self, value):
        for r in self.ranges:
            if r.in_source_range(value):
                diff = value - r.source_range_start
                return r.dest_range_start + diff
        return value

    def calculate_jump(self, value):
        for r in self.ranges:
            if r.in_source_range(value):
                return r.source_range_start + r.range_length - value
        return 1e100


def preprocess(puzzle):
    maps = []
    current_map = None
    for line in puzzle:
        if (pattern:="seeds:") in line:
            seeds_1 = list(map(int, line.replace(pattern, "").split()))
            ranges = list(map(lambda x: x.split(), [r for r in re.findall("\d+ \d+", line)]))
            seeds_2 = [RangeData(0, int(r[0]), int(r[1])) for r in ranges]
        elif (pattern:=" map:") in line:
            current_map = MapData(line.replace(pattern, ""), [])
        elif len(line) == 0:
            if current_map is not None:
                maps.append(current_map)
        else:
            r = RangeData(*map(int, line.split()))
            current_map.ranges.append(r)
    maps.append(current_map)
    return seeds_1, seeds_2, maps

def solve_puzzle(puzzle):
    part1 = part2 = None
    seeds_1, seeds_2, maps = preprocess(puzzle)
    
    min_location = sys.maxsize
    for seed in seeds_1:
        for m in maps:
            seed = m.transform(seed)
        min_location = min(min_location, seed)

    part1 = min_location

    min_location = sys.maxsize
    for seed_range in seeds_2:
        seed = seed_range.source_range_start
        while seed < seed_range.source_range_start + seed_range.range_length:
            jump = sys.maxsize
            s = seed
            for m in maps:
                jump = min(m.calculate_jump(s), jump)
                s = m.transform(s)
            min_location = min(min_location, s)
            # skip a range of numbers that are converted to consecutive numbers
            seed += 1 if jump == sys.maxsize or jump < 1 else jump

    part2 = min_location

    return part1, part2


def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(35, 46))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(510109797, 9622622))
