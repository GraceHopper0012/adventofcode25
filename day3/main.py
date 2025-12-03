largest_num = 0
idx_largest = 0
for idx, battery in enum(batteries[:-1]):
    if int(battery) > largest_num:
        largest_num = battery
        idx_largest = idx
        if largest_num == 9:
            break
largest_second_num = 0
for battery in batteries[idx_largest:]:
    if int(battery > largest_second_num):
        largest_second_num = battery