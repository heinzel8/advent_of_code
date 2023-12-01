filename = r"01 Calorie Counting.txt"

with open(filename) as f:
    lines = f.readlines()

sum_calories = 0
elves = []

for line in lines:
    line = line.strip()
    if not line:
        elves.append(sum_calories)
        sum_calories = 0
        continue
    else:
        sum_calories += int(line)

elves = sorted(elves)

solution1 = elves[-1]
print("solution1", solution1, "calories")

top_three_elves = elves[-3:]
solution2 = sum(top_three_elves)

print("solution2", solution2, "calories")