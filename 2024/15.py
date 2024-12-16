from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from dataclasses import dataclass
from vector import Vector

@dataclass
class Globals:
    stretched_map:bool = False

globals = Globals()

LEFT = Vector(x=-1, y=0)
RIGHT = Vector(x=1, y=0)
UP = Vector(x=0, y=-1)
DOWN = Vector(x=0, y=1)

directions = {"<": LEFT, ">": RIGHT, "^": UP, "v": DOWN}
directions2 = {}
for k,v in directions.items():
    directions2.update({(v.x,v.y):k})

@dataclass
class Box:
    positions: list[Vector]

    def __init__(self, positions):
        if type(positions) is list: 
            self.positions = positions
        else:
            self.positions = [positions]

    def hit(self, pos:Vector):
        return(pos in self.positions)

@dataclass
class Map:
    width: int
    height: int
    obstacles: list[Vector]
    boxes: list[Box]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.boxes = []

    def add_obstacle(self, x, y):
        self.obstacles.append(Vector(x=x, y=y))
        if globals.stretched_map:
            self.obstacles.append(Vector(x=x+1, y=y))

    def add_box(self, x, y):
        if globals.stretched_map:
            self.boxes.append(Box([Vector(x=x,y=y), Vector(x=x+1,y=y)]))
        else:
            self.boxes.append(Box(Vector(x=x,y=y)))

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def has_box_at(self, pos):
        return self.get_box_at(pos) != None
    
    def get_box_at_xy(self, x, y):
        return self.get_box_at(Vector(x=x, y=y))

    def get_box_at(self, pos):
        for box in self.boxes:
            if box.hit(pos):
                return box
        return None
    
    def can_move_box(self, box: Box, dir: Vector):
        # if not self.is_box(pos):
        #     assert False, f"No commodity at pos {pos.x},{pos.y}"
        
        for pos in box.positions:
            target_pos = pos + dir
            if self.is_obstacle(target_pos):
                return False

            target_box = self.get_box_at(target_pos)
            if target_box is None or target_box == box:
                continue

            if not self.can_move_box(target_box, dir):
                return False
        
        return True
    
    def move_box(self, box: Box, dir: Vector):
        if not (self.can_move_box(box, dir)):
            return False
        
        target_boxes = []
        for pos in box.positions:
            target_pos = pos + dir
            target_box = self.get_box_at(target_pos)
            if target_box is None or target_box == box:
                continue
            target_boxes.append(target_box)
        if len(target_boxes)==2:
            if target_boxes[0] == target_boxes[1]:
                del target_boxes[1]
        for b in target_boxes:
            self.move_box(b, dir)
        
        for index in range(len(box.positions)):
            box.positions[index] += dir
        return True
    
    def to_str(self, robot=None, prev_pos:Vector=None) -> str:
        res = ""
        for y in range(self.height):
            skip_next = False
            for x in range(self.width):
                if skip_next:
                    skip_next = False
                    continue
                pos = Vector(x=x, y=y)
                if robot is not None and x == robot.x and y == robot.y:
                    res += "@"
                elif prev_pos is not None and x == prev_pos.x and y == prev_pos.y:
                    res += "x"
                elif self.has_box_at(pos):
                    if globals.stretched_map:
                        res += "[]"
                        skip_next = True
                    else:
                        res += "O"
                elif pos in self.obstacles:
                    res += "#"
                else:
                    res += "."
            res += "\n"
        return res.strip()
        

def preprocess(puzzle):
    map = Map(0,0)
    for y,line in enumerate(puzzle):
        if line == "":
            break
        for x,c in enumerate(line):
            if globals.stretched_map:
                x *= 2
            if c == "#":
                map.add_obstacle(x,y)
            elif c == "O":
                map.add_box(x,y)
            elif c == "@":
                robot = Vector(x=x, y=y)
    map.height = y
    map.width = len(puzzle[0])

    if globals.stretched_map:
        map.width *= 2

    movements = []
    for line in puzzle[y+1:]:
        for c in line:
            movements.append(directions[c])
    return map, movements, robot

def move(robot:Vector, dir:Vector, map:Map):
    new_pos = robot + dir
    if map.is_obstacle(new_pos):
        return robot

    box = map.get_box_at(new_pos)
    if box is not None:
        if not map.move_box(box, dir):
            return robot
    
    robot = new_pos
    return robot

def write_map(map:Map, robot:Vector=None, move:Vector=None, previous_pos:Vector=None):
    with open("map.txt", "w") as f:
        f.writelines(map.to_str(robot, previous_pos))
        if move is not None:
            f.write(directions2[(move.x, move.y)])
        

def solve_puzzle(puzzle, solve_part1=True, solve_part2=True):
    global globals
    r1, r2 = None, None
    dbg = False

    for part in range(1,3):
        if part == 1:
            globals = Globals(stretched_map=False)
            if not solve_part1:
                continue
        else:
            globals = Globals(stretched_map=True)
            if not solve_part2:
                continue
            
        print(f"Part {part}:")
        print()

        map, movements, robot = preprocess(puzzle)
        for i,m in enumerate(movements, 1):
            if i == 22:
                pass
            previous_pos = Vector(x=robot.x, y=robot.y)
            robot = move(robot, m, map)
            if dbg: write_map(map, robot, m, previous_pos)
            progress = round(i/len(movements)*100,1)
            if i%10 == 0:
                print(f"  Progress: {progress}%   ", end="\r")
        print()
        write_map(map, robot, m)

        r = 0
        for b in map.boxes:
            r += b.positions[0].y * 100 + b.positions[0].x
        if part == 1:
            r1 = r
        else:
            r2 = r

    return r1, r2

def run_tests():
    global globals
    globals = Globals(stretched_map=False)

    map,_,_ = preprocess(["# O@#", "", "<"])
    box = map.get_box_at_xy(2,0)
    assert map.move_box(box, LEFT)
    assert len(map.boxes)==1 and Box(Vector(x=1,y=0)) in map.boxes
    assert False == map.move_box(box, LEFT)
    assert len(map.boxes)==1 and Box(Vector(x=1,y=0)) in map.boxes

    map, moves, robot = preprocess(["# @OO #", "", ">"])
    box = map.get_box_at_xy(3,0)
    assert map.move_box(box, RIGHT)
    assert len(map.boxes) == 2
    assert Box(Vector(x=4,y=0)) in map.boxes
    assert Box(Vector(x=5,y=0)) in map.boxes
    assert False == map.move_box(box, RIGHT)
    assert len(map.boxes) == 2
    assert Box(Vector(x=4,y=0)) in map.boxes
    assert Box(Vector(x=5,y=0)) in map.boxes

    map, moves, robot = preprocess(["# @O O #", "", ">"])
    box = map.get_box_at_xy(3,0)
    assert map.move_box(box, RIGHT)
    assert len(map.boxes) == 2
    assert Box(Vector(x=4,y=0)) in map.boxes
    assert Box(Vector(x=5,y=0)) in map.boxes
    assert map.move_box(box, RIGHT)
    assert Box(Vector(x=5,y=0)) in map.boxes
    assert Box(Vector(x=6,y=0)) in map.boxes

    globals = Globals(stretched_map=True)
    dbg = True

    map, moves, robot = preprocess(["#@O O #", "", ">"])
    box = map.get_box_at_xy(4,0)
    if dbg: write_map(map)
    assert map.move_box(box, RIGHT)
    if dbg: write_map(map)
    assert len(map.boxes) == 2
    assert map.get_box_at(Vector(x=5,y=0)) is not None
    assert map.get_box_at(Vector(x=8,y=0)) is not None
    assert map.move_box(box, RIGHT)
    if dbg: write_map(map)
    assert len(map.boxes) == 2
    assert map.get_box_at(Vector(x=6,y=0)) is not None
    assert map.get_box_at(Vector(x=8,y=0)) is not None
    assert map.move_box(box, RIGHT)
    if dbg: write_map(map)
    assert len(map.boxes) == 2
    assert map.get_box_at(Vector(x=7,y=0)) is not None
    assert map.get_box_at(Vector(x=9,y=0)) is not None

    m = [
        "#######",
        "#...#.#",
        "#.....#",
        "#..OO@#",
        "#..O..#",
        "#.....#",
        "#######",
        "",
        "^"
    ]
    map, moves, robot = preprocess(m)
    if dbg: write_map(map)
    assert map.move_box(map.get_box_at(Vector(x=9, y=3)), LEFT)
    if dbg: write_map(map)
    assert len(map.boxes) == 3 
    assert map.get_box_at(Vector(x=5,y=3)) is not None
    assert map.get_box_at(Vector(x=7,y=3)) is not None
    assert map.get_box_at(Vector(x=6,y=4)) is not None

    assert map.move_box(map.get_box_at(Vector(x=6, y=4)), UP)
    if dbg: write_map(map)

    assert map.move_box(map.get_box_at(Vector(x=5, y=2)), UP)
    if dbg: write_map(map)

    m = [
        "#######",
        "#.....#",
        "#..O..#",
        "#..OO@#",
        "#.OOO.#",
        "#.....#",
        "#.#...#",
        "#######",
        "",
        "^"
    ]
    map, moves, robot = preprocess(m)
    if dbg: write_map(map)
    assert map.move_box(map.get_box_at(Vector(x=9, y=3)), LEFT)
    if dbg: write_map(map)
    assert map.move_box(map.get_box_at(Vector(x=6, y=2)), DOWN)
    if dbg: write_map(map)
    assert False == map.move_box(map.get_box_at(Vector(x=6, y=3)), DOWN)

    m = [
        "#######",
        "#.....#",
        "#..O..#",
        "#..O..#",
        "#..@..#",
        "#######",
        "",
        "^"
    ]
    map, moves, robot = preprocess(m)
    if dbg: write_map(map)
    assert map.move_box(map.get_box_at(Vector(x=6, y=3)), UP)
    if dbg: write_map(map)

if (__name__ == "__main__"):
    run_tests()

    globals = Globals(stretched_map=False)

    ref1 = ref2 = None
    ref1 = solve_puzzle(get_reference_data(__file__, part=1), solve_part2=False)[0]
    ref2 = solve_puzzle(get_reference_data(__file__, part=2), solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(10092, 9021))

    sol1, sol2 = None, None
    sol1 = solve_puzzle(get_puzzle_data(__file__), solve_part2=False)[0]
    sol2 = solve_puzzle(get_puzzle_data(__file__), solve_part1=False)[1]
    print_statistics("Solution", (sol1, sol2), expected=(1465152, 1511259))
