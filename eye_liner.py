from classes.intersection import IntersectionWithError
from classes.point import Point
from classes.throw import Throw


if __name__ == '__main__':
    throw_1 = Throw(Point(36.596, 422.8), -52.2)
    throw_2 = Throw(Point(-42.5, 146.5), -47.6)

    throw_1 = Throw(Point(5000.5, 101.4), 19.4)
    throw_2 = Throw(Point(5049.9, 329.9), 26.9)

    throw_1 = Throw(Point(10000.5, 119.5), -39.6)
    throw_2 = Throw(Point(10010, 260), -44.8)
    throw_3 = Throw(Point(9967.6, 39.84), -37.8)
    # throw_1 = Throw(Point(10000.5, 1269), -120.9)
    # throw_2 = Throw(Point(5049.9, 329.9), 26.9)

    # print(calculate_raw_intersection(throw_1, throw_2))
    # intersection = calculate_intersection(throw_1, throw_2)
    # print(intersection, intersection.point.distance_to())

    # print(IntersectionWithError.from_throws([throw_1, throw_2, throw_3]))
    print(
        IntersectionWithError.from_throws(
        [
            # Throw(Point(100, -102), -175.5),
            # Throw(Point(-6, -2222), -22.8),
            # Throw(Point(-66.5, -112), -119.8),

            # Throw(Point(106.4, -246.5), -119.4),
            # Throw(Point(272.2, -246.7), -121.8),
            # Throw(Point(588.14, -467.2), -121.1),
            # Throw(Point(877.3, -591.3), -123.3),

            # Throw(Point(-217.5, 165.5), 9.4),
            # Throw(Point(-372, 272), 4.6),

            # Throw(Point(73.5, 16.5), 68.1),
            # Throw(Point(-36.66, -65.5), 64.8),
            Throw(Point(-223, 0), 59.1),
            Throw(Point(-351, 512), 78.8),
            # Throw(Point(-36.66, -65.5), 64.8),
        ]
        )
    )
