"""script to prepare files for advent of code"""
import sys, os
import shutil as sh
from aocd import get_data, examples
from pathlib import Path

if len(sys.argv) != 2:
    raise ValueError('Please provide day number')

YEAR = 2023
DAY = sys.argv[1]
SCRIPT_TEMPLATE_FILE = "template.py"
SCRIPT_FILE = f"{DAY}.py"
DATA_FILE = f"{DAY}_data.txt"
REFERENCE_DATA_FILE = f"{DAY}_reference_data.txt"

if not os.path.exists(SCRIPT_TEMPLATE_FILE):
    raise FileNotFoundError(f"{SCRIPT_TEMPLATE_FILE} not found")

if not os.path.exists(SCRIPT_FILE):
    sh.copy(SCRIPT_TEMPLATE_FILE, SCRIPT_FILE)
    print(f"created {SCRIPT_FILE}")
else:
    print(f"{SCRIPT_FILE} already exists")

with open(DATA_FILE, 'w', encoding="utf8") as f:
    f.write(get_data(day=int(DAY), year=YEAR))
print(f"created {DATA_FILE}")
with open(REFERENCE_DATA_FILE, 'w', encoding="utf8") as f:
    pass
print(f"created {REFERENCE_DATA_FILE}")
