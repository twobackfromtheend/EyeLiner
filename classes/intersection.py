import dataclasses
from math import cos, sin, pi
from typing import Tuple, List

import numpy as np

from classes.point import Point
from classes.throw import Throw


@dataclasses.dataclass
class IntersectionWithError:
    point: Point
    x_range: Tuple[float, float]
    z_range: Tuple[float, float]

    def __str__(self):
        return f"Intersection: x={self.point.x:.1f}, z={self.point.z:.1f}; " \
               f"x_range=[{self.x_range[0]:.1f}, {self.x_range[1]:.1f}], " \
               f"z_range=[{self.z_range[0]:.1f}, {self.z_range[1]:.1f}]"

    @classmethod
    def from_throws(cls, throws: List[Throw], d_facing: float = 0.5 + 1e-5) -> 'IntersectionWithError':
        if not len(throws) >= 2:
            raise ValueError(f"2 or more throws required (received {len(throws)}).")
        if len(throws) == 2:
            return cls._from_2_throws(*throws, d_facing=d_facing)
        return cls._from_multiple_throws(throws, d_facing=d_facing)

    @staticmethod
    def _from_2_throws(throw_1: Throw, throw_2: Throw, d_facing: float) -> 'IntersectionWithError':
        best_guess = intersect_2(throw_1, throw_2)
        other_guesses = []
        throw_1_minus = dataclasses.replace(throw_1, facing=throw_1.facing - d_facing)
        throw_1_plus = dataclasses.replace(throw_1, facing=throw_1.facing + d_facing)
        throw_2_minus = dataclasses.replace(throw_2, facing=throw_2.facing - d_facing)
        throw_2_plus = dataclasses.replace(throw_2, facing=throw_2.facing + d_facing)
        for _throw_1, _throw_2 in [
            (throw_1_minus, throw_2_minus),
            (throw_1_plus, throw_2_minus),
            (throw_1_minus, throw_2_plus),
            (throw_1_plus, throw_2_plus),
        ]:
            _guess = intersect_2(_throw_1, _throw_2)
            other_guesses.append(_guess)

        return IntersectionWithError(
            Point(x=best_guess.x, z=best_guess.z),
            x_range=(
                min(_guess.x for _guess in other_guesses),
                max(_guess.x for _guess in other_guesses),
            ),
            z_range=(
                min(_guess.z for _guess in other_guesses),
                max(_guess.z for _guess in other_guesses),
            ),
        )

    @staticmethod
    def _from_multiple_throws(throws: List[Throw], d_facing: float) -> 'IntersectionWithError':
        best_guess = intersect_multiple(throws)

        guesses = 10
        other_guesses = []
        deviations = np.clip(np.random.standard_normal((guesses, len(throws))), -2, 2)
        for _deviations in deviations:
            _guess = intersect_multiple(
                [
                    dataclasses.replace(throw, facing=throw.facing + d_facing * _deviations[i])
                    for i, throw in enumerate(throws)
                ]
            )
            other_guesses.append(_guess)

        return IntersectionWithError(
            Point(x=best_guess.x, z=best_guess.z),
            x_range=(
                min(_guess.x for _guess in other_guesses),
                max(_guess.x for _guess in other_guesses),
            ),
            z_range=(
                min(_guess.z for _guess in other_guesses),
                max(_guess.z for _guess in other_guesses),
            ),
        )


def intersect_2(throw_1: Throw, throw_2: Throw) -> Point:
    heading_1 = throw_1.heading
    cos_1 = cos(heading_1)
    sin_1 = sin(heading_1)
    heading_2 = throw_2.heading
    cos_2 = cos(heading_2)
    sin_2 = sin(heading_2)
    assert heading_1 != heading_2, f"Throw headings must not be aligned, lines do not intersect. ({heading_1} and {heading_2})"

    dx = throw_2.point.x - throw_1.point.x
    dz = throw_2.point.z - throw_1.point.z
    if abs(cos_1) > 0.01:
        k = sin_1 / cos_1
        den = cos_2 * k - sin_2
        t = (dz - dx * k) / den
    else:
        k = cos_1 / sin_1
        den = sin_2 * k - cos_2
        t = (dx - dz * k) / den

    x = throw_2.point.x + t * cos_2
    z = throw_2.point.z + t * sin_2

    t_1 = (x - throw_1.point.x) / cos_1
    t_2 = (z - throw_1.point.z) / sin_1
    assert t > 0 and t_1 > 0 and t_2 > 0, f"Calculated intersection goes backwards (scales: {t:}, {t_1}, {t_2})"
    return Point(x, z)


def intersect_multiple(throws: List[Throw]) -> Point:
    denominator = np.zeros((2, 2), dtype=np.float)
    numerator = np.zeros((2, 1), dtype=np.float)
    for throw in throws:
        throw_heading_normal = throw.heading + pi / 2
        _cos = cos(throw_heading_normal)
        _sin = sin(throw_heading_normal)
        unit_normal = np.array([_cos, _sin]).reshape((2, 1))

        denominator += unit_normal @ unit_normal.T
        numerator += unit_normal @ unit_normal.T @ np.array([throw.point.x, throw.point.z]).reshape((2, 1))

    intersection_array = (np.linalg.inv(denominator) @ numerator).flatten()
    return Point(intersection_array[0], intersection_array[1])
