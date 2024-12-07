from pathlib import Path
from termcolor import colored, cprint

def get_puzzle_data(file):
    stem = Path(file).stem
    path = Path(file).parent
    if stem == "template": return ""
    filename = f"{stem.split('_')[0]}_data.txt"
    with open(path / filename, encoding="utf8") as f:
        return [line.strip("\r\n") for line in f.readlines()]

def get_reference_data(file, part):
    stem = Path(file).stem
    path = Path(file).parent
    if stem == "template": return ""
    filename = f"{stem.split('_')[0]}_reference_data_part{part}.txt"
    with open(path / filename, encoding="utf8") as f:
        puzzle = [line.strip("\r\n") for line in f.readlines()]
        if (0 == len(puzzle)):
            cprint(f"ERROR: Reference data file part {part} is empty", color="red")
            quit()

        return puzzle

def print_statistics(description, value, expected):
    print("="*48)
    for n in range(2):
        result = ""
        if expected[n] is not None:
            if value[n] == expected[n]:
                result = colored("(PASS)", "green")
            else:
                result = result = colored("(FAIL)", "red") + f" expected {expected[n]}"
        print(f"{description} {n+1}: ", value[n], result)