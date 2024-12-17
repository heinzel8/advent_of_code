from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass
from typing import List, Optional

LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,-1)
DOWN = (0,1)

directions_symbols = "^>v<"
directions = [UP, RIGHT, DOWN, LEFT]

@dataclass
class Waypoint:
    x: int
    y: int
    dir: tuple
    cost: int = 0
    previous:Optional["Waypoint"] = None

    def pos(self):
        return (self.x, self.y)
    
    def __lt__(self, other):
        if isinstance(other, Waypoint):
            return self.cost < other.cost
        return False
    
    def __hash__(self):
        return hash((self.x, self.y, self.dir))
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Waypoint):
            return self.x == other.x and self.y == other.y and self.dir == other.dir
        return False

@dataclass
class Map:
    obstacles: list[tuple]
    start: Waypoint
    end: Waypoint
    width: int
    height: int
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.obstacles = []

    def is_on_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_neighbors(self, waypoint:Waypoint) -> List[Waypoint]:
        neighbors = []
        for dir in directions:
            nx, ny = waypoint.x + dir[0], waypoint.y + dir[1]
            if self.is_on_map(nx, ny) and (nx, ny) not in self.obstacles:
                neighbors.append(Waypoint(x=nx, y=ny, dir=dir))
        return neighbors
    
    def to_array(self):
        content = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(" ")
            content.append(row)

        for obs in self.obstacles:
            content[obs[1]][obs[0]] = "#"
        
        return content

    def to_string(self, waypoint:Waypoint):
        content = self.to_array()
        wp = waypoint
        previous_index = directions.index(RIGHT)
        while wp:
            index = directions.index(wp.dir)
            c = directions_symbols[index]
            # c = "x"
            if index != previous_index:
                c = "x"
                previous_index = index
            content[wp.y][wp.x] = c
            wp = wp.previous
        
        res = ""
        for row in content:
            res += "".join(row) + "\n"
        return res.strip()
    
    def write_map(self, waypoint:Waypoint):
        with open("map.txt", "w") as f:
            f.writelines(self.to_string(waypoint))

class AStarAlgorithm:
    def __init__(self, map: Map):
        self.map = map
        self.open: List[Waypoint] = []
        self.closed: List[Waypoint] = []

    def heuristic(self, waypoint: Waypoint):
        return abs(waypoint.x - self.map.end.x) + abs(waypoint.y - self.map.end.y)

    def get_waypoint_at(self, waypoint:Waypoint, list_to_search):
        return next((w for w in list_to_search if w == waypoint), None)

    def search(self):
        self.open.append(self.map.start)
        
        while self.open:
            current = min(self.open, key=lambda w: w.cost + self.heuristic(w))
            self.open.remove(current)
            self.closed.append(current)
        
            if current.x == self.map.end.x and current.y == self.map.end.y:
                return current
            
            neighbors: List[Waypoint] = self.map.get_neighbors(current)
            for neighbor in neighbors:
                if self.get_waypoint_at(neighbor, self.closed):
                    continue

                new_cost = current.cost + 1
                if neighbor.dir != current.dir:
                    new_cost += 1000

                open_waypoint = self.get_waypoint_at(neighbor, self.open)
                if open_waypoint is None:
                    neighbor.cost = new_cost
                    neighbor.previous = current
                    self.open.append(neighbor)
                elif new_cost < open_waypoint.cost:
                    open_waypoint.cost = new_cost
                    open_waypoint.dir = neighbor.dir
                    open_waypoint.previous = current

        return None

def preprocess(puzzle):
    map = Map(width = len(puzzle[0]), height = len(puzzle))
    for y,line in enumerate(puzzle):
        for x,c in enumerate(line):
            if c == '#':
                map.obstacles.append((x,y))
            elif c == 'S':
                map.start = Waypoint(x, y, RIGHT, 0)
            elif c == 'E':
                map.end = Waypoint(x, y, RIGHT, 0)
    return map

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    map:Map = preprocess(puzzle)
    r1, r2 = None, None

    a_star = AStarAlgorithm(map)
    wp:Waypoint = a_star.search()
    r1 = wp.cost
    map.write_map(wp)
   
    return r1, r2

def run_tests():
    puzzle = [
    "#########E#",
    "#        x#",
    "# #######x#",
    "# ###xxxxx#",
    "# ###x#####",
    "#    xS####",
    "###########"
    ]
    map:Map = preprocess(puzzle)
    a_star = AStarAlgorithm(map)
    wp:Waypoint = a_star.search()
    assert 4010 == wp.cost
    # map.write_map(wp)


if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(11048, None))

    solution = None, None
    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(85432, None))