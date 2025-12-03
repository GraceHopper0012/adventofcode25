starting_position = 50
def parse_input(filename: str):
    lines = []
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
    return lines

def translate_code(code: str):
    translation = 0
    if code[0].upper() == "R":
        translation = int(code[1:])
    else:
        translation = (-1) * int(code[1:])
    return translation

def turn_dial(translated_code: int, dial_pos: int):
    dial_pos += translated_code
    correct_dial_pos,turning_zeros = check_position(dial_pos)
    return correct_dial_pos,turning_zeros

started_on_zero = starting_position == 0
print(started_on_zero)
def check_position(pos: int):
    global started_on_zero
    turning_zeros_other = str(abs(pos))[:-2]
    if turning_zeros_other == '':
        turning_zeros_other = 0
    else:
        turning_zeros_other = int(turning_zeros_other)
    if (pos % 100) == 0:
        turning_zeros_other -= 1
    if pos < 0 and not started_on_zero:
        turning_zeros_other += 1
    pos %= 100
    started_on_zero = False
    if pos == 0:
        started_on_zero = True
    return pos,turning_zeros_other

def __main__():
    zeros = 0
    input_codes = parse_input("input.txt")
    dial_position = starting_position
    parsed_codes = []
    for code in input_codes:
        parsed_codes.append(translate_code(code))
    for code in parsed_codes:
        dial_position,turning_zeros = turn_dial(code, dial_position)
        zeros += turning_zeros
        if dial_position == 0:
            zeros += 1
    print(dial_position)
    print(int(zeros))

__main__()
