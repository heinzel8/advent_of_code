from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass, field
import sys
import re

@dataclass
class RangeData:
    dest_range_start: int
    source_range_start: int
    range_length: int
    def get_source_range(self):
        return range(self.source_range_start, self.source_range_start + self.range_length + 1)
    def get_dest_range(self):
        return range(self.dest_range_start, self.dest_range_start + self.range_length + 1)
    def in_source_range(self, value):
        return value >= self.source_range_start and value < self.source_range_start + self.range_length
    def in_target_range(self, value):
        return value >= self.dest_range_start and value < self.dest_range_start + self.range_length

@dataclass
class MapData:
    name : str
    ranges: list = field(default_factory=list)
    def transform(self, source_value):
        for r in self.ranges:
            # sr = r.get_source_range()
            # dr = r.get_dest_range()
            if r.in_source_range(source_value):
                diff = source_value - r.source_range_start
                return r.dest_range_start + diff

                # index = sr.index(source_value)
                # res = dr[index]
                return res
        return source_value

def preprocess(puzzle):
    maps = []
    current_map = None
    for line in puzzle:
        if "seeds:" in line:
            seeds_1 = list(map(int, line.replace("seeds:", "").split()))
            ranges = list(map(lambda x: x.split(), [r for r in re.findall("\d+ \d+", line)]))
            seeds_2 = [RangeData(0, int(r[0]), int(r[1])) for r in ranges]
        elif "map:" in line:
            current_map = MapData(line.replace(" map:", ""), [])
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

    c = 0
    for seed_range in seeds_2:
        c += seed_range.range_length

    c1 = 0
    min_location = sys.maxsize
    for seed_range in seeds_2:
        for seed in seed_range.get_source_range():
            c1 += 1
            if c1 % 100_000 == 0:
                print(f"\r{c1/c*100:0.3} {c1}/{c}         ", end="")
            for m in maps:
                seed = m.transform(seed)
            min_location = min(min_location, seed)

    part2 = min_location

    return part1, part2


def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    # ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    # print_statistics("Reference", (ref1, ref2), expected=(35, 46))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(510109797, None))
