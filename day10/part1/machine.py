class Machine:
    def __init__(self, ):
        self.light_diag = None

    def parse_input(self, line):
        lights, buttons, joltage = line.split("]")


regex = r'''\[(?P<light>[.#]+)\]\s(?P<buttons>\(.*\))+\s\{(?P<joltage>.[^}]+)\}'''
example = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
