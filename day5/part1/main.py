def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        split = lines.index('')
        valid = lines[:split]
        ids = lines[split+1:]
        return valid, ids

def get_ranges(valid):
    ranges = []
    for idrange in valid:
        newrange = idrange.split("-")
        ranges.append([int(newrange[0]),int(newrange[1])])
    return ranges

class single_id():
    ranges = []
    def __init__(self, thisid):
        self.no = int(thisid)

    def inrange(self):
        for idrange in single_id.ranges:
            if min(idrange) <= int(self.no) <= max(idrange):
                return True
        return False

def check_valid(ranges, ids):
    count_correct = 0
    for everyid in ids:
        if single_id(everyid).inrange():
            count_correct += 1
    return count_correct

def __main__():
    valid, ids = parse_input("input.txt")
    ranges = get_ranges(valid)
    single_id.ranges = ranges
    valid_count = check_valid(ranges,ids)
    print(valid_count)

if __name__ == "__main__":
    __main__()
