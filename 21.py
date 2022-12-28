from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re
from sympy import S, Eq, solve, expand
from copy import deepcopy

class Monkey:
    def __init__(self, name:str, value:str) -> None:
        self.name = name
        if value.isnumeric():
            self.number = int(value)
        else:
            self.set_expression(value)

    def set_expression(self, value):
        self.sources = [s.strip() for s in re.split(r'[*\-\+/]', value) if not s.strip().isnumeric()]
        match = re.match(".*([*\-\+/]+).*", value)
        self.operation = match.groups()[0]
        self.expression = value

    name = ""
    number = None
    sources:list[str] = []
    operation = None
    expression = ""

def preprocess(puzzle):
    pattern = "(.*): (.*)"
    return [Monkey(*re.match(pattern, line).groups()) for line in puzzle]

def get_monkey(name, monkeys):
    r = [m for m in monkeys if m.name == name]
    if not r:
        raise ValueError(f"monkey with name {name} not found.")
    return r[0]

    
def solve_puzzle_part1(monkeys:list[Monkey]):
    has_unresolved = True
    while has_unresolved:
        has_unresolved = False
        for monkey in monkeys:
            if monkey.number is not None:
                continue
            else:
                sm1:Monkey = [m for m in monkeys if m.name == monkey.sources[0]][0]
                sm2:Monkey = [m for m in monkeys if m.name == monkey.sources[1]][0]
                if sm1.number is not None and sm2.number is not None:
                    s = f"{sm1.number} {monkey.operation} {sm2.number}"
                    monkey.number = int(eval(s))
                else:
                    has_unresolved = True
    s1 = [m for m in monkeys if m.name == "root"][0].number
    return s1

def solve_puzzle_part2(monkeys:list[Monkey]):
    symbols = []
    equations = []
    human:Monkey = get_monkey("humn", monkeys)
    human.number = None

    resolved = False
    while True:
        resolved = False
        for monkey in [m for m in monkeys if m.number is None and m.name != "humn"]:
            for source_name in monkey.sources:
                source_monkey:Monkey = get_monkey(source_name, monkeys)
                if source_name not in monkey.expression:
                    continue
                if source_monkey.number is not None:
                    monkey.set_expression(monkey.expression.replace(source_name, str(source_monkey.number)))
                    resolved = True
            try:
                s = eval(monkey.expression)
                monkey.number = int(s)
                resolved = True
            except:
                pass
        
        if not resolved: break
    
    for i,monkey in enumerate([m for m in monkeys if m.name != "humn"]):
        if monkey.name == "root":
            l,r = monkey.expression.split(f" {monkey.operation} ")
        elif monkey.number is not None:
            continue
            l = monkey.name
            r = monkey.number
        else:
            l = monkey.name
            r = monkey.expression
        equations.append(Eq(S(l), S(r)))
        #print(f"{i:4} {l} = {r}")

    result = solve(equations)
    return int(result.get(S("humn")))

def solve_puzzle(_monkeys:list[Monkey]):
    s1, s2 = None, None
    s1 = solve_puzzle_part1(deepcopy(_monkeys))
    s2 = solve_puzzle_part2(deepcopy(_monkeys))
    return s1, s2

if (__name__ == "__main__"):
    ref = solve_puzzle(preprocess(get_reference_data(__file__)))
    print_statistics("Reference", ref, expected=(152, 301))
    
    sol = solve_puzzle(preprocess(get_puzzle_data(__file__)))
    print_statistics("Solution",  sol, expected=(81075092088442, 3349136384441))
