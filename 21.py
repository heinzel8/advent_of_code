from aoc_utils import get_puzzle_data, get_reference_data, print_statistics
import re
from sympy import S, Eq, solve, expand
from copy import deepcopy

class Monkey:
    def __init__(self, name:str, value:str) -> None:
        if name == "dcjm":
            pass
        name = "monkey_" + name
        self.name = name
        if value.isnumeric():
            self.number = int(value)
        else:
            pattern_instruction = "([a-z]+) ([*\-+/]+) (.*)"
            match = re.match(pattern_instruction, value).groups()
            assert len(match) == 3
            self.source1, self.operation, self.source2 = match
            self.expression = value.replace(self.source1, "monkey_" + self.source1).replace(self.source2, "monkey_" + self.source2)
            self.source1 = "monkey_" + self.source1
            self.source2 = "monkey_" + self.source2
    name = ""
    number = None
    source1 = ""
    source2 = ""
    operation = None
    expression = ""

def preprocess(puzzle):
    pattern = "(.*): (.*)"
    return [Monkey(*re.match(pattern, line).groups()) for line in puzzle]

def solve_puzzle(_monkeys:list[Monkey]):
    monkeys = deepcopy(_monkeys)
    has_unresolved = True
    while has_unresolved:
        has_unresolved = False
        for monkey in monkeys:
            if monkey.number is not None:
                continue
            else:
                sm1:Monkey = [m for m in monkeys if m.name == monkey.source1][0]
                sm2:Monkey = [m for m in monkeys if m.name == monkey.source2][0]
                if sm1.number is not None and sm2.number is not None:
                    monkey.number = int(eval(f"{sm1.number} {monkey.operation} {sm2.number}"))
                else:
                    has_unresolved = True
    s1 = [m for m in monkeys if m.name == "monkey_root"][0].number

    s2 = None

    return s1, s2

if (__name__ == "__main__"):
    x, y = S(["x", "y"])
    #equations = [Eq(x,y), Eq(y, 5**2)]
    equations = []
    # x = S("x")
    # a = S("pppw")
    # b = S("sjmn")
    # s = S("root")
    equations.append(Eq(S("myroot"), S("pppw + sjmn")))
    equations.append(Eq(S("pppw"), 1))
    equations.append(Eq(S("sjmn"), 1))
    
    #dbpl: 5
    #cczh: sllz + lgvd

    print(solve(equations))

    ref = solve_puzzle(preprocess(get_reference_data(__file__)))
    print_statistics("Reference", ref, expected=(152, None))
    
    #sol = solve_puzzle(preprocess(get_puzzle_data(__file__)))
    #print_statistics("Solution",  sol, expected=(81075092088442, None))
