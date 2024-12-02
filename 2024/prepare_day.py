"""script to prepare files for advent of code"""
import sys, os
import shutil as sh
import aocd
from pathlib import Path

if len(sys.argv) != 2:
    raise ValueError('Please provide day number')


YEAR = 2024
DAY = sys.argv[1]
SCRIPT_TEMPLATE_FILE = "template.py"
SCRIPT_FILE = f"{DAY}.py"
DATA_FILE = f"{DAY}_data.txt"
REFERENCE_DATA_FILES = [f"{DAY}_reference_data_part{part}.txt" for part in range(1,3)]

# os.chdir(str(YEAR))
print(os.getcwd())

if not os.path.exists(SCRIPT_TEMPLATE_FILE):
    raise FileNotFoundError(f"Template file {SCRIPT_TEMPLATE_FILE} not found")

if not os.path.exists(SCRIPT_FILE):
    sh.copy(SCRIPT_TEMPLATE_FILE, SCRIPT_FILE)
    print(f"created {SCRIPT_FILE}")
else:
    print(f"{SCRIPT_FILE} already exists")

with open(DATA_FILE, 'w', encoding="utf8") as f:
    try:
        f.write(aocd.get_data(day=int(DAY), year=YEAR))
    except:
        pass
print(f"created {DATA_FILE}")

for file in REFERENCE_DATA_FILES:
    if not os.path.exists(file):
        with open(file, 'w', encoding="utf8") as f: pass
        print(f"created {file}")
    else:
        print(f"{file} already exists")
