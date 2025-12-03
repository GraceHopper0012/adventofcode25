
def split_ranges(ranges: str):
    id_ranges = ranges.split(",")
    ids_ranges = []
    for id_range in id_ranges:
        ids.append(id_range.split("-"))
    int_ids = []
    for str_range in ids:
        int_range = []
        for str_id in str_range:
            int_range.append(int(str_id))
        int_ids.append(int_range)

