"""script to prepare files for advent of code"""
import sys
import shutil as sh
import os

if len(sys.argv) != 2:
    raise ValueError('Please provide day number')

DAY = sys.argv[1]
SCRIPT_TEMPLATE_FILE = "template.py"
SCRIPT_FILE = DAY + ".py"
DATA_FILE = DAY + ".txt"
REFERENCE_DATA_FILE = DAY + "_reference.txt"

if not os.path.exists(SCRIPT_TEMPLATE_FILE):
    raise FileNotFoundError(SCRIPT_TEMPLATE_FILE + " not found")

if not os.path.exists(SCRIPT_FILE):
    sh.copy(SCRIPT_TEMPLATE_FILE, SCRIPT_FILE)
    print(f"created {SCRIPT_FILE}")
else:
    print(f"{SCRIPT_FILE} already exists")

for file_name in [DATA_FILE, REFERENCE_DATA_FILE]:
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding="utf8") as f:
            pass
        print(f"created {file_name}")
    else:
        print(f"{file_name} already exists")
