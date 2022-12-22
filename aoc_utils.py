from pathlib import Path

def get_puzzle_data(file):
    stem = Path(file).stem
    if stem == "template": return ""
    with open(stem + ".txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def get_reference_data(file):
    stem = Path(file).stem
    if stem == "template": return ""
    with open(stem + f"_reference.txt", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]

def print_statistics(description, value, expected):
    print("="*48)
    for n in range(2):
        result = ""
        if expected[n] is not None:
            result = f"(PASS)" if value[n] == expected[n] else f"(FAIL) expected {expected[n]}"
        print(f"{description} {n+1}: ", value[n], result)