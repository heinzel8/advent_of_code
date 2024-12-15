from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass
from vector import Vector

LEFT = Vector(x=-1, y=0)
RIGHT = Vector(x=1, y=0)
UP = Vector(x=0, y=-1)
DOWN = Vector(x=0, y=1)

directions = {"<": LEFT, ">": RIGHT, "^": UP, "v": DOWN}
directions2 = {}
for k,v in directions.items():
    directions2.update({(v.x,v.y):k})

@dataclass
class Map:
    width: int
    height: int
    obstacles: list[Vector]
    goods: list[Vector]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.goods = []

    def add_obstacle(self, x, y):
        self.obstacles.append(Vector(x=x, y=y))

    def add_good(self, x, y):
        self.goods.append(Vector(x=x, y=y))

    def is_obstacle2(self, x, y):
        return self.is_obstacle(Vector(x=x,y=y))

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def is_good2(self, x, y):
        return self.is_good(Vector(x=x,y=y))

    def is_good(self, pos):
        return pos in self.goods
    
    def move_good2(self, f_x:int, f_y:int, dir:Vector):
        return self.move_good(Vector(x=f_x, y=f_y), dir)
    
    def move_good(self, pos: Vector, dir: Vector):
        if not self.is_good(pos):
            assert False, f"No commodity at pos {pos.x},{pos.y}"
        
        to = pos + dir
        if self.is_obstacle(to):
            return False
        elif self.is_good(to):
            if not self.move_good(to, dir):
                return False
        
        self.goods.remove(pos)
        self.goods.append(to)
        return True
    
    def to_str(self, robot) -> str:
        res = ""
        for y in range(self.height):
            for x in range(self.width):
                pos = Vector(x=x, y=y)
                if pos == robot:
                    res += "@"
                elif pos in self.goods:
                    res += "O"
                elif pos in self.obstacles:
                    res += "#"
                else:
                    res += " "
            res += "\n"
        return res.strip()
        

def preprocess(puzzle):
    map = Map(0,0)
    for y,line in enumerate(puzzle):
        if line == "":
            break
        for x,c in enumerate(line):
            if c == "#":
                map.add_obstacle(x,y)
            elif c == "O":
                map.add_good(x,y)
            elif c == "@":
                robot = Vector(x=x, y=y)
    map.width = x + 1
    map.height = y + 1

    movements = []
    for line in puzzle[y+1:]:
        for c in line:
            movements.append(directions[c])
    return map, movements, robot

def move(robot:Vector, dir:Vector, map:Map):
    new_pos = robot + dir
    if map.is_obstacle(new_pos):
        return robot

    if map.is_good(new_pos):
        if not map.move_good(new_pos, dir):
            return robot
    
    robot = new_pos
    return robot

def write_map(map:Map, robot:Vector, move:Vector):
    with open("map.txt", "w") as f:
        f.writelines(map.to_str(robot))
        f.write(directions2[(move.x, move.y)])
        

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    map, movements, robot = preprocess(puzzle)
    r1, r2 = None, None

    for i,m in enumerate(movements):
        robot = move(robot, m, map)
        progress = round(i/len(movements)*100,1)
        if i%10 == 0:
            print(f"  Progress: {progress}%   ", end="\r")
    write_map(map, robot, m)

    r1 = 0
    for g in map.goods:
        r1 += g.y * 100 + g.x

    return r1, r2

def run_tests():
    map, moves, robot  = preprocess(["# O@#", "", "<"])
    assert map.move_good(Vector(x=2,y=0), moves[0])
    assert map.goods == [Vector(x=1, y=0)]
    assert False == map.move_good(Vector(x=1,y=0), moves[0])
    assert map.goods == [Vector(x=1, y=0)]

    map, moves, robot  = preprocess(["# @OO #", "", ">"])
    assert map.move_good2(3, 0, RIGHT)
    assert len(map.goods) == 2 and map.is_good2(4,0) and map.is_good2(5,0)
    assert False == map.move_good2(4, 0, RIGHT)
    assert len(map.goods) == 2 and map.is_good2(4,0) and map.is_good2(5,0)

    map, moves, robot  = preprocess(["# @O O #", "", ">"])
    assert map.move_good(Vector(x=3,y=0), RIGHT)
    assert len(map.goods) == 2 and map.is_good2(4,0) and map.is_good2(5,0)
    assert map.move_good(Vector(x=4,y=0), RIGHT)
    assert len(map.goods) == 2 and map.is_good2(5,0) and map.is_good2(6,0)


if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(10092, None))

    solution = None, None
    solution = solve_puzzle(get_puzzle_data(__file__))
    print_statistics("Solution", solution, expected=(1465152, None))
