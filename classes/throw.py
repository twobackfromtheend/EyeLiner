from dataclasses import dataclass
from math import pi

from classes.point import Point


@dataclass
class Throw:
    point: Point
    facing: float

    @property
    def heading(self) -> float:
        angle_in_degrees = self.facing + 90
        if angle_in_degrees > 180:
            angle_in_degrees -= 360
        angle = angle_in_degrees / 180 * pi
        return angle
