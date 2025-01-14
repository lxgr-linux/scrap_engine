#!/usr/bin/env python3

import unittest
import scrap_engine as se
import math, time


class CirclerTest(unittest.TestCase):
    def test_circler(self):
        map = se.Map(background=" ")

        def circle(x, y, radius):
            for i in range(map.height)[(y-radius if y-radius in range(map.height) else 0):][:(y+radius if y+radius in range(map.height) else map.height)]:
                for j in range(map.width)[x-radius:][:x+radius]:
                    if math.sqrt((i-y)**2+(j-x)**2) <= radius:
                        try:
                            se.Object("a").add(map, j, i)
                        except:
                            continue

        map.show(init=True)
        for i in range(int(map.width/2)):
            time.sleep(0.1)
            circle(int(map.width/2), int(map.height/2), i)
            map.show()
            while len(map.obs) > 0:
                map.obs[0].remove()
