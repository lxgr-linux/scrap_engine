import math
from .box import Box
from ..object import Object


class Circle(Box):
    """
    A circle, that can be added to a map.
    """

    def __init__(self, char, radius, state=None, ob_class=Object,
                 ob_args=None):
        super().__init__(0, 0)
        if ob_args is None:
            ob_args = {}
        self.char = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        if state is not None:
            self.state = state
        self.__gen(radius)

    def __gen(self, radius):
        self.radius = radius
        for i in range(-(int(radius) + 1), int(radius + 1) + 1):
            for j in range(-(int(radius) + 1), int(radius + 1) + 1):
                if math.sqrt(i ** 2 + j ** 2) <= radius:
                    self.add_ob(self.ob_class(self.char, state=self.state,
                                              arg_proto=self.ob_args), i, j)

    def rechar(self, char):
        """
        Changes the chars the circle is filled with.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    def resize(self, radius):
        """
        Resizes the circle.
        """
        if added := self.added:
            self.remove()
        self.obs = []
        self.__gen(radius)
        if added:
            self.add(self.map, self.x, self.y)
