import re
regex = r"^(.*)\1+$"

def parse_input(filename: str):
    with open(filename, 'r') as file:
        return file.readline().strip()

def split_ranges(ranges: str):
    id_ranges = ranges.split(",")
    ids_ranges = []
    for id_range in id_ranges:
        newrange = id_range.split("-")
        if len(newrange[0]) > 0 and len(newrange[1]) > 0:
            ids_ranges.append(newrange)
    int_ids = []
    for str_range in ids_ranges:
        int_range = []
        for str_id in str_range:
            try:
                int_range.append(int(str_id))
            except Exception as e:
                print("'#" + str_id + "#'")
        int_ids.append(int_range)
    return int_ids

def get_all_numbers(int_ranges: list):
    all_ids = []
    for int_range in int_ranges:
        all_ids.extend(range(int(int_range[0]), int(int_range[1]+1)))
    return all_ids

def __main__():
    input_line = parse_input("input.txt")
    int_ids = split_ranges(input_line)
    all_ids = get_all_numbers(int_ids)
    result = 0
    for id_number in all_ids:
        if is_invalid(id_number):
            result += id_number
    print(result)

def is_invalid(id_number):
    matches = re.findall(regex, str(id_number))
    if len(matches) > 0:
        return True
    return False

__main__()