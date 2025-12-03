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
    correct_dial_pos = check_position(dial_pos)
    return correct_dial_pos

def check_position(pos: int):
    #if pos > 99:
    #    pos -= 100
    #elif pos < 0:
    #    pos += 100
    pos %= 100
    return pos

def check_zero(pos: int):
    return 1 if pos == 0 else 0

def __main__():
    zeros = 0
    input_codes = parse_input("input.txt")
    dial_position = starting_position
    parsed_codes = []
    for code in input_codes:
        parsed_codes.append(translate_code(code))
    for code in parsed_codes:
        dial_position = turn_dial(code, dial_position)
        if dial_position == 0:
            zeros += 1
        # zeros += check_zero(dial_position)
    print(dial_position)
    print(zeros)

__main__()
