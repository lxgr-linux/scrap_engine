import math
from typing import Type, override

from scrap_engine.addable.state import DEFAULT_STATE, State

from ..object import ArgProto, Object
from .box import Box


class Circle(Box):
    """
    A circle, that can be added to a map.
    """

    def __init__(
        self,
        char: str,
        radius: int,
        state: State = DEFAULT_STATE,
        ob_class: Type[Object] = Object,
        ob_args: ArgProto = None,
    ):
        super().__init__(0, 0)
        if ob_args is None:
            ob_args = {}
        self.char: str = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.state = state
        self.__gen(radius)

    def __gen(self, radius: int):
        self.radius = radius
        for i in range(-(int(radius) + 1), int(radius + 1) + 1):
            for j in range(-(int(radius) + 1), int(radius + 1) + 1):
                if math.sqrt(i**2 + j**2) <= radius:
                    self.add_ob(
                        self.ob_class(
                            self.char, state=self.state, arg_proto=self.ob_args
                        ),
                        i,
                        j,
                    )

    def rechar(self, char: str):
        """
        Changes the chars the circle is filled with.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    @override
    def resize(self, radius: int):
        """
        Resizes the circle.
        """
        if added := self.added:
            self.remove()
        self.obs = []
        self.__gen(radius)
        if added:
            self.add(self.map, self.x, self.y)
