import argparse
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, ClassVar
import math
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist
import itertools

def sortByDistance(boxes: List):
    points = np.vstack([jb.to_array() for jb in boxes])
    N = len(boxes)

    # 2) pdist → flaches Array aller i<j-Distanzen
    dists = pdist(points, metric='euclidean')  # Länge = N*(N-1)/2

    # 3) Alle möglichen Paare (i<j)
    pairs = list(itertools.combinations(range(N), 2))  # [(0,1), (0,2), (1,2), ...]

    # 4) Tupel mit Distanz: ((box1, box2), distance)
    pairs_with_dists = [((boxes[i], boxes[j]), dist) for (i, j), dist in zip(pairs, dists)]

    # 5) Sortieren nach Abstand (kleinster zuerst)
    pairs_with_dists.sort(key=lambda x: x[1])

    # 6) Nur die ersten 1000 Paare
    top_1000_pairs = [pair for pair, dist in pairs_with_dists[:1000]]
    return top_1000_pairs

def top_k_nearest_cross_circuit_pairs(boxes: List, top_k: int = 1000,
                                      initial_k: int = 8, max_k_cap: int = 5000):
    """
    Returns a list of up to `top_k` tuples: (box_i, box_j, distance),
    where box_i and box_j belong to different circuits and distance is minimal.
    The result is sorted ascending by distance.
    """
    n = len(boxes)
    if n < 2:
        return []

    # Prepare coordinate array and circuit ids
    coords = np.empty((n, 3), dtype=float)
    circuits = [None] * n
    for i, b in enumerate(boxes):
        coords[i, 0] = b.x
        coords[i, 1] = b.y
        coords[i, 2] = b.z
        circuits[i] = b.circuit

    tree = cKDTree(coords)

    # We'll collect candidate pairs in a dict: {(i,j): dist}
    candidates = {}

    # iterative strategy: start with initial_k, double until we have enough candidates or reach cap
    k = initial_k
    k = min(max(1, k), n - 1)
    max_k = min(max_k_cap, n - 1)

    while True:
        # Query for each point: its k nearest neighbors (excluding itself later)
        kq = min(k + 1, n)  # +1 because the query includes the point itself
        dists_all, idxs_all = tree.query(coords, k=kq)

        # normalize shapes: ensure 2D arrays (n, kq)
        if kq == 1:
            dists_all = dists_all.reshape(n, 1)
            idxs_all = idxs_all.reshape(n, 1)
        else:
            # if returned as 1D when kq==2 and n==1 etc. but generally it's fine
            dists_all = np.atleast_2d(dists_all)
            idxs_all = np.atleast_2d(idxs_all)

        # collect cross-circuit neighbor pairs
        for i in range(n):
            for dist, j in zip(dists_all[i], idxs_all[i]):
                if j == i:
                    continue
                if circuits[i] == circuits[j]:
                    continue
                a, b = (i, j) if i < j else (j, i)
                # keep smallest distance if pair seen multiple times
                prev = candidates.get((a, b))
                if prev is None or dist < prev:
                    candidates[(a, b)] = float(dist)

        # If we have enough distinct candidate pairs to pick top_k, break
        if len(candidates) >= top_k:
            break

        # If we've reached maximum k, stop (can't get more)
        if k >= max_k:
            break

        # Otherwise increase k and try again
        k = min(k * 2, max_k)

    # Convert candidates dict to sorted list by distance
    sorted_pairs = sorted(candidates.items(), key=lambda item: item[1])
    # Each item: ((i,j), dist)

    # Build final list of tuples: (box_i, box_j, dist)
    result = []
    for (i, j), dist in sorted_pairs[:top_k]:
        result.append((boxes[i], boxes[j], dist))

    return result

def parse_input(filename: str):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

def __main__():
    lines = parse_input("input.txt")
    boxes = []
    for line in lines:
        x,y,z = line.split(",")
        boxes.append(JunctionBox(int(x), int(y), int(z)))
    sorted_distances = sortByDistance(boxes)
    for combi in sorted_distances:
        combi[0].circuit.merge(combi[1].circuit)
    circuits = Circuit.circuits
    circuits.sort(key=lambda x: x.length)
    result = 1
    for cc in circuits[0:3]:
        result *= cc.length
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

    def to_array(self):
        """Return numeric 1D array [x,y,z]."""
        return np.array([self.x, self.y, self.z], dtype=float)

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
    ClassVar circuits = []

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
        if self.length <= cc.length:
            newcc = self
            oldcc = cc
        else:
            newcc = cc
            oldcc = self

        for box in oldcc.boxes:
            newcc.addBox(box)

        Circuit.circuits.remove(oldcc)

    def addBox(self, box) -> None:
        if box.circuit is self:
            return
        if box.circuit is not None:
            box.circuit.removeBox(box)
        if box not in self.boxes:
            self.boxes.append(box)
        box.circuit = self
        self.boxes.append(box)

    @property
    def length(self) -> int:
        return len(self.boxes)

    def removeBox(self, box):
        if box.circuit is self:
            box.circuit = None
            self.boxes.remove(box)
        else:
            raise Exception

if __name__ == "__main__":
    __main__()

