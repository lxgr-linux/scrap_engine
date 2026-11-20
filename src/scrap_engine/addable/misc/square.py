from typing import override

from scrap_engine.addable.state import DEFAULT_STATE, State

from ..object import ArgProto, Object
from .box import Box


class Square(Box):
    """
    A rectangle, that can be added to a map.
    """

    def __init__(
        self,
        char: str,
        width: int,
        height: int,
        state: State = DEFAULT_STATE,
        ob_class: type[Object] = Object,
        ob_args: ArgProto = None,
    ):
        super().__init__(height, width)
        if ob_args is None:
            ob_args = {}
        self.state = state
        self.ob_class = ob_class
        self.char = char
        self.ob_args = ob_args
        self.__create()

    def __create(self) -> None:
        for ry in range(self.height):
            for rx in range(self.width):
                self.add_ob(
                    self.ob_class(self.char, self.state, arg_proto=self.ob_args),
                    rx,
                    ry,
                )

    def rechar(self, char: str) -> None:
        """
        Changes the chars the Square is filled with.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    @override
    def resize(self, width: int, height: int) -> None:
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
