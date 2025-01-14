import scrap_engine as se
import math
import unittest

class CircleTest(unittest.TestCase):
    def test_circle(self):
        class Circle(se.Box):
            def __init__(self, char, radius):
                super().__init__(0, 0)
                self.char = char
                self.radius = radius
                for i in range(-(int(radius)+1), int(radius+1)+1):
                    for j in range(-(int(radius)+1), int(radius+1)+1):
                        if math.sqrt((i)**2+(j)**2) <= radius:
                            self.add_ob(se.Object(char), i, j)

        map = se.Map(background=" ")

        circle = Circle("#", 4.3)
        circle.add(map, 6, 6)
        circle.set(20, 10)

        map.show()
