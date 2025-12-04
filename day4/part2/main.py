class Position():
    chars = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def inBounds(self):
        if self.getY() < 0:
            return False
        if self.getX() < 0:
            return False
        if self.getY() > (len(Position.chars) - 1):
            return False
        if self.getX() > (len(Position.chars[self.getY()]) - 1):
            return False
        return True
    
    def getChar(self):
        return Position.chars[self.getY()][self.getX()]

    def removeRoll(self):
        Position.chars[self.getY()][self.getX()] = "."
    
    def isRoll(self):
        return self.getChar() == "@"

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def get_adjacent(self):
        adjacent = []
        for i in range(-1,2):
            for j in range(-1,2):
                if not (i == 0 and j == 0):
                    pos = Position(self.getX()+i, self.getY()+j)
                    if pos.inBounds():
                        adjacent.append(pos)

        return adjacent

    def canPickup(self):
        adjacent = self.get_adjacent()
        count = 0
        for pos in adjacent:
            if pos.isRoll():
                count += 1
        if count < 4:
            self.removeRoll()
            return True
        return False
    
    def set_chars(chars: list):
        Position.chars = chars

def parse_input(filename: str):
    with open(filename, "r") as f:
        data = f.read().splitlines()
    coordinate_system = []
    for line in data:
        coordinate_system.append(list(line))
    return coordinate_system

def __main__():
    coordinate_system = parse_input("input.txt")
    Position.set_chars(coordinate_system)
    possible_rolls = 0
    possible_rolls_before = -1
    runs = 0
    while possible_rolls_before != possible_rolls:
        possible_rolls_before = possible_rolls
        for y, line in enumerate(coordinate_system):
            for x, char in enumerate(line):
                if char == "@":
                    roll = Position(x,y)
                    if roll.canPickup():
                        possible_rolls += 1
    print("Possible rolls:")
    print(possible_rolls)

if __name__ == "__main__":
    __main__()
