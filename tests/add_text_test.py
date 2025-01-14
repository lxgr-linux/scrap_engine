#!/usr/bin/python3

import unittest
import scrap_engine as se

class TextTest(unittest.TestCase):
    def test_text(self):
        map = se.Map(background=" ")

        t = se.Text("Hello")
        t.add(map, 0, 0)

        k = se.Text(" You", esccode="\033[31m")
        t+=k

        map.show()
