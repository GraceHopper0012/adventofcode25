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
        ranges.append((int(newrange[0]), int(newrange[1])))
    return ranges

def remove_overlaps(ranges):
    ranges = sorted(ranges, key=lambda x: x[0])
    current_s, current_e = ranges[0]
    newranges = [ranges[0]]
    for s, e in ranges:
        if s <= newranges[-1][0]:
            newranges[-1] = (s,max(e,newranges[-1][1]))
        elif s <= newranges[-1][1]:
            if e > newranges[-1][1]:
                newranges[-1] = (newranges[-1][0], e)
            else:
                continue
        else:
            newranges.append((s,e))
    return newranges


def count_ids(ranges):
    return sum((end - start) + 1 for start, end in ranges)

def __main__():
    valid, ids = parse_input("input.txt")
    ranges = get_ranges(valid)
    newranges = remove_overlaps(ranges)
    idcount = count_ids(newranges)
    print(idcount)

if __name__ == "__main__":
    __main__()
