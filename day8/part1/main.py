from dataclasses import dataclass, field
from typing import Optional, List
import math

def __main__():
    circuits = Circuit.circuits
    circuits.sort(key=lambda x: x.length)
    result = math.prod(circuits[0:3])
    print(result)


@dataclass
class JunctionBox:
    def __init__(self,x,y,z):
        self._x = x
        self._y = y
        self._z = z
        self._cc = Circuit([self])

    def __hash__(self):
        return hash(self.id)

    def calculateDistance(self, x, y, z):
        distance = math.sqrt((self._x - x)**2 + (self._y - y)**2 + (self._z - z)**2)

    def connect(self, box):
        if self.circuit != box.circuit:
            self.circuit.merge(box.circuit)

    @property
    def circuit(self):
        return self._cc

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def z(self) -> int:
        return self._z

    @circuit.setter
    def circuit(self, new):
        self._cc = new

    @x.setter
    def x(self, new):
        self._x = new

    @y.setter
    def y(self, new):
        self._y = new

    @z.setter
    def z(self, new):
        self._z = new


@dataclass
class Circuit:
    circuits = []

    def __init__(self, boxes=None):
        if boxes is None:
            boxes = []
        Circuit.circuits.append(self)
        self._boxes = boxes

    @property
    def boxes(self) -> List[JunctionBox]:
        return self._boxes

    @boxes.setter
    def boxes(self, new) -> None:
        self._boxes = new

    def merge(self, cc) -> None:
        for box in cc.boxes:
            self.addBox(box)

    def addBox(self, box) -> None:
        if box.circuit is self:
            return
        if box.circuit is not None:
            box.circuit.removeBox(box)
        if box not in self.boxes:
            self.boxes.append(box)
        # box.circuit = self
        box.setCircuit(self)
        self.boxes.append(box)

    @property
    def length(self) -> int:
        return len(self.boxes)

    def removeBox(self, box):
        if box.circuit is self:
            # box.circuit = None
            box.setCircuit(None)
            self.boxes.remove(box)
        else:
            raise Exception
