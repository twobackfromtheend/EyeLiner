import dataclasses


@dataclasses.dataclass
class Point:
    x: float
    z: float

    def __str__(self):
        return f"Point: x={self.x:.3f}, z={self.z:.3f}"

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.z - other.z)

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.z - other.z) ** 2) ** 0.5
