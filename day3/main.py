def get_largest_joltage(batteries):
    largest_num = 0
    idx_largest = 0
    for idx, battery in enumerate(batteries[:-1]):
        if int(battery) > largest_num:
            largest_num = int(battery)
            idx_largest = idx
            if largest_num == 9:
                break
    largest_second_num = 0
    for battery in batteries[idx_largest+1:]:
        if int(battery) > largest_second_num:
            largest_second_num = int(battery)
    return int(str(largest_num) + str(largest_second_num))

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