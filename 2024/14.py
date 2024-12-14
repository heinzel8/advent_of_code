from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
from vector import Vector
from dataclasses import dataclass
import re
from PIL import Image
import numpy as np

@dataclass
class Robot:
    position: Vector
    velocity: Vector

@dataclass
class Map:
    width:int
    height: int

def preprocess(puzzle) -> list[Robot]:
    robots = []
    digit = r"(-?\d+)"
    pattern = f"p={digit},{digit} v={digit},{digit}"
    for line in puzzle:
        match = re.match(pattern, line)
        if match:
            position = Vector(x=int(match.group(1)), y=int(match.group(2)))
            velocity = Vector(x=int(match.group(3)), y=int(match.group(4)))
            robots.append(Robot(position, velocity))
    return robots

def walk(robot:Robot, mapp:Map):
    n:Vector = robot.position + robot.velocity

    if n.x < 0:
        n.x += mapp.width

    if n.y < 0:
        n.y += mapp.height

    if not 0 <= n.x <= mapp.width-1:
        n.x = n.x % (mapp.width)
    if not 0 <= n.y <= (mapp.height-1):
        n.y = n.y % (mapp.height)
    robot.position = n

def get_quadrant(pos:Vector, map:Map):
    m_x = ((map.width-1)//2)
    m_y = ((map.height-1)//2)
    if pos.x == m_x or pos.y == m_y:
        return 0
    
    if pos.x < m_x:
        if pos.y < m_y:
            return 1
        else:
            return 3
    if pos.x > m_x:
        if pos.y < m_y:
            return 2
        else:
            return 4

    assert(False)

def create_image(filename, map:Map, robots:list[Robot]):
    # Create a new image with white background
    img = Image.new('L', (map.width+10, map.height+10), color=0)
    
    # Convert the image to a numpy array for easier pixel manipulation
    pixels = np.array(img)

    for robot in robots:
        pixels[robot.position.x, robot.position.y] = 255
    
    # Convert back to an image
    img = Image.fromarray(pixels)
    
    # Save the image
    img.save(filename)
    print(f"Image saved as {filename}")

def solve_puzzle(puzzle, mapp:Map, solve_part1=True, solve_part2=True):
    robots: list[Robot] = preprocess(puzzle)
    r1, r2 = None, None

    if solve_part1:
        for loop in range(1, 101):
            for robot in robots:
                walk(robot, mapp)

        counts = {}
        for robot in robots:
            q = get_quadrant(robot.position, mapp)
            counts[q] = counts.get(q, 0) + 1
        del counts[0]

        r1 = 1
        for v in counts.values():
            r1 *= v

    # I found the number by writing 10.000 images and manually searching for the Christmas tree
    if solve_part2:
        r2 = 7132
        for loop in range(101, 10_000):
            print(loop)
            for robot in robots:
                walk(robot, mapp)
            if loop == r2:
                create_image(filename=f"{loop}.png", map=mapp, robots=robots)
                break

    return r1, r2

def run_tests():
    m = Map(width=11, height=7)
    r = Robot(Vector(x=2,y=4), Vector(x=2,y=-3))
    walk(r, m)
    assert(r.position == Vector(x=4,y=1))
    walk(r, m)
    assert(r.position == Vector(x=6,y=5))
    walk(r, m)
    assert(r.position == Vector(x=8,y=2))
    walk(r, m)
    assert(r.position == Vector(x=10,y=6))
    walk(r, m)
    assert(r.position == Vector(x=1,y=3))

    assert(0 == get_quadrant(Vector(x=5,y=0), m))
    assert(0 == get_quadrant(Vector(x=0,y=3), m))
    assert(1 == get_quadrant(Vector(x=0,y=0), m))
    assert(1 == get_quadrant(Vector(x=4,y=2), m))
    assert(2 == get_quadrant(Vector(x=6,y=2), m))
    assert(2 == get_quadrant(Vector(x=8,y=1), m))
    assert(3 == get_quadrant(Vector(x=1,y=4), m))
    assert(3 == get_quadrant(Vector(x=3,y=5), m))
    assert(4 == get_quadrant(Vector(x=6,y=6), m))
    assert(4 == get_quadrant(Vector(x=7,y=4), m))
    pass

if (__name__ == "__main__"):
    run_tests()

    ref1 = ref2 = None
    m = Map(width=11, height=7)

    ref1 = solve_puzzle(get_reference_data(__file__, part=1), m, solve_part2=False)[0]
    # ref2 = solve_puzzle(get_reference_data(__file__, part=2), m, solve_part1=False)[1]
    print_statistics("Reference", (ref1, ref2), expected=(12, None))

    m = Map(width=101, height=103)

    solution = None, None
    solution = solve_puzzle(get_puzzle_data(__file__), m)
    print_statistics("Solution", solution, expected=(229980828, 7132))
