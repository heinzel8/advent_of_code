from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass, field
import sys

@dataclass
class RangeData:
    dest_range_start: int
    source_range_start: int
    range_length: int
    def get_source_range(self):
        return range(self.source_range_start, self.source_range_start + self.range_length + 1)
    def get_dest_range(self):
        return range(self.dest_range_start, self.dest_range_start + self.range_length + 1)

@dataclass
class MapData:
    name : str
    ranges: list = field(default_factory=list)
    def transform(self, source_value):
        for r in self.ranges:
            sr = r.get_source_range()
            dr = r.get_dest_range()
            if source_value in sr:
                index = sr.index(source_value)
                res = dr[index]
                return res
        return source_value

def preprocess(puzzle):
    maps = []
    current_map = None
    for line in puzzle:
        if "seeds:" in line:
            seeds = list(map(int, line.replace("seeds:", "").split()))
        elif "map:" in line:
            current_map = MapData(line.replace(" map:", ""), [])
        elif len(line) == 0:
            if current_map is not None:
                maps.append(current_map)
        else:
            r = RangeData(*map(int, line.split()))
            current_map.ranges.append(r)
    maps.append(current_map)
    return seeds, maps

def solve_puzzle(puzzle):
    part1 = part2 = None
    seeds, maps = preprocess(puzzle)
    min_location = sys.maxsize
    for seed in seeds:
        for md in maps:
            seed = md.transform(seed)
            continue
        min_location = min(min_location, seed)

    return min_location, part2

def run_tests():
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1))[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2))[1]
    print_statistics("Reference", (ref1, ref2), expected=(35, None))

    sol = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", sol, expected=(None, None))
