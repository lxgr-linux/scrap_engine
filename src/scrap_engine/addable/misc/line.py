import math

from .box import Box
from ..object import Object


class Line(Box):
    """
    A line described by a vector, that cam be added to map.
    """

    def __init__(self, char, cx, cy, l_type="straight", state=None,
                 ob_class=Object, ob_args=None):
        super().__init__(0, 0)
        if ob_args is None:
            ob_args = {}
        self.char = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        if state is not None:
            self.state = state
        self.type = l_type
        self.__gen(cx, cy)

    def __gen(self, cx, cy):
        self.cx = cx
        self.cy = cy
        if cx ** 2 >= cy ** 2:
            for i in range(int(math.sqrt(cx ** 2))):
                i = int(cx / math.sqrt(cx ** 2) * i)
                j = {"straight": int, "crippled": round}[self.type](cy * i / cx)
                self.add_ob(self.ob_class(self.char, state=self.state,
                                          arg_proto={**self.ob_args, **{"x": i, "y": cy * i / cx}}),
                            i, j)
        else:
            for j in range(int(math.sqrt(cy ** 2))):
                j = int(cy / math.sqrt(cy ** 2) * j)
                i = {"straight": int, "crippled": round}[self.type](cx * j / cy)
                self.add_ob(self.ob_class(self.char, state=self.state,
                                          arg_proto={**self.ob_args, **{"x": cx * j / cy, "y": j}}),
                            i, j)

    def rechar(self, char):
        """
        Changes the chars the line is made from.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    def resize(self, cx, cy):
        """
        Resizes the line.
        """
        if added := self.added:
            self.remove()
        self.obs = []
        self.__gen(cx, cy)
        if added:
            self.add(self.map, self.x, self.y)
