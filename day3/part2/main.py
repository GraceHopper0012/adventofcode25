def get_largest_joltage(batteries):
    last_idx = 0
    batteries_joltage = ""
    for i in range(12,0,-1):
        largest_num = -1
        idx_largest = 0
        end = -(i-1) if i != 1 else None
        for idx, battery in enumerate(batteries[last_idx:end]):
            if int(battery) > largest_num:
                largest_num = int(battery)
                idx_largest = last_idx + idx
        last_idx = idx_largest + 1
        batteries_joltage += str(largest_num)
    if len(batteries_joltage) != 12:
        raise
    return int(batteries_joltage)

def parse_input(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        return lines

def __main__():
    batterypacks = parse_input("input.txt")
    max_joltage = 0
    for batterypack in batterypacks:
        max_joltage += get_largest_joltage(batterypack)
    print(max_joltage)

__main__()