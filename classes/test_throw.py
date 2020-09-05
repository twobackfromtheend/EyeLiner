import unittest
from math import pi

from classes.throw import Throw


class TestThrow(unittest.TestCase):
    def test_heading(self):
        for facing, desired_heading in [
            (-180, -pi / 2),
            (-90, 0),
            (0, pi / 2),
            (90 - 1e-5, pi),
            (90 + 1e-5, -pi),
            (180, -pi / 2),
        ]:
            heading = Throw(0, 0, facing).heading
            print(f"Facing: {facing}. Heading: {heading}. Heading should be {desired_heading}.")
            self.assertAlmostEqual(
                heading,
                desired_heading,
                places=4
            )


if __name__ == '__main__':
    unittest.main()
