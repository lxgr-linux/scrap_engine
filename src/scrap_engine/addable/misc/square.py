from typing import Type
from scrap_engine.addable.state import DEFAULT_STATE, State
from .box import Box
from ..object import Object


class Square(Box):
    """
    A rectangle, that can be added to a map.
    """

    def __init__(
        self, char, width, height, state:State=DEFAULT_STATE,
        ob_class:Type[Object]=Object, ob_args=None
    ):
        super().__init__(height, width)
        if ob_args is None:
            ob_args = {}
        if state is not None:
            self.state = state
        self.ob_class = ob_class
        self.char = char
        self.ob_args = ob_args
        self.__create()

    def __create(self):
        for ry in range(self.height):
            for rx in range(self.width):
                self.add_ob(
                    self.ob_class(
                        self.char, self.state, arg_proto=self.ob_args
                    ),
                    rx, ry
                )

    def rechar(self, char):
        """
        Changes the chars the Square is filled with.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    def resize(self, width, height):
        """
        Resizes the rectangle to a certain size.
        """
        super().resize(height, width)
        if added := self.added:
            self.remove()
        self.obs = []
        self.__create()
        if added:
            self.add(self.map, self.x, self.y)
