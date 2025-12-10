import math
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist
import itertools
from itertools import combinations
from typing import List


def pairwise_sorted_by_distance(boxes: List["JunctionBox"]):
    pairs = []
    for a, b in combinations(boxes, 2):
        if a == b:
            continue
        dist = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))
        pairs.append((dist, a, b))
    pairs.sort(key=lambda t: t[0])
    return pairs


def parse_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
    return lines


class JunctionBox:
    last_id = 0

    def __init__(self, x: float, y: float, z: float):
        JunctionBox.last_id += 1
        self.id = JunctionBox.last_id
        self._x = x
        self._y = y
        self._z = z
        self._cc = Circuit([self])

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, JunctionBox):
            return False
        return self.id == other.id

    def calculateDistance(self, x, y, z):
        return math.sqrt((self._x - x) ** 2 + (self._y - y) ** 2 + (self._z - z) ** 2)

    def to_array(self):
        return np.array([self.x, self.y, self.z], dtype=float)

    def connect(self, box: "JunctionBox"):
        if self.circuit != box.circuit:
            self.circuit.merge(box.circuit)

    @property
    def circuit(self):
        return self._cc

    @circuit.setter
    def circuit(self, new):
        self._cc = new

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, new):
        self._x = new

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new):
        self._y = new

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, new):
        self._z = new


class Circuit:
    circuits: List["Circuit"] = []
    last_id: int = 0

    def __init__(self, boxes=None):
        if boxes is None:
            boxes = []
        Circuit.last_id += 1
        self.id = Circuit.last_id
        Circuit.circuits.append(self)
        self._boxes = list(boxes)

    def __eq__(self, other):
        if not isinstance(other, Circuit):
            return False
        return self.id == other.id

    @staticmethod
    def getcircuits():
        return Circuit.circuits

    @property
    def boxes(self) -> List[JunctionBox]:
        return self._boxes

    @boxes.setter
    def boxes(self, new) -> None:
        self._boxes = new

    def merge(self, cc: "Circuit") -> None:
        if self not in Circuit.circuits or cc not in Circuit.circuits:
            raise Exception("One of the circuits is not registered")
        if self == cc:
            return
        # choose the larger circuit as destination to minimize moves
        if self.length >= cc.length:
            dest = self
            src = cc
        else:
            dest = cc
            src = self

        for box in list(src.boxes):
            dest.addBox(box)

        if src in Circuit.circuits:
            Circuit.circuits.remove(src)

    def addBox(self, box: JunctionBox) -> None:
        if box.circuit is self:
            return
        if box.circuit is not None:
            box.circuit.removeBox(box)
        if box not in self.boxes:
            self.boxes.append(box)
        box.circuit = self

    @property
    def length(self) -> int:
        return len(self.boxes)

    def removeBox(self, box: JunctionBox):
        if box.circuit is self:
            box.circuit = None
            self.boxes.remove(box)
        else:
            raise Exception("Box not in this circuit")


def main():
    # reset class-level state so repeated runs behave predictably
    Circuit.circuits = []
    Circuit.last_id = 0
    JunctionBox.last_id = 0

    lines = parse_input("input.txt")
    boxes: List[JunctionBox] = []
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            continue
        x, y, z = parts
        boxes.append(JunctionBox(int(x), int(y), int(z)))

    # merge the closest 1000 pairs (or fewer if not available)
    sorted_distances = pairwise_sorted_by_distance(boxes)
    for dist, a, b in sorted_distances[:1000]:
        a.circuit.merge(b.circuit)

    circuits = Circuit.getcircuits()
    # sort by length descending (largest first)
    circuits.sort(key=lambda x: x.length, reverse=True)

    # multiply lengths of the three largest circuits (or fewer if not available)
    if not circuits:
        print(0)
        return

    top_three = circuits[:3]
    result = 1
    for cc in top_three:
        result *= cc.length

    print(result)


if __name__ == "__main__":
    main()
