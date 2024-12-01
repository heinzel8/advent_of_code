from pathlib import Path

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
            print(f"ERROR: Reference data file part {part} is empty")
            quit()

        return puzzle

def print_statistics(description, value, expected):
    print("="*48)
    for n in range(2):
        result = ""
        if expected[n] is not None:
            result = f"(PASS)" if value[n] == expected[n] else f"(FAIL) expected {expected[n]}"
        print(f"{description} {n+1}: ", value[n], result)