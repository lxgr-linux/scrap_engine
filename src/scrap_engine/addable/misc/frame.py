from typing import Optional, Type
from scrap_engine.addable.state import DEFAULT_STATE, State
from .box import Box
from .square import Square
from ..object import Object


class Frame(Box):
    """
    A Frame made of ascii charactes:

    +----+
    |    |
    |    |
    +----+

    That can be added to map.
    """

    def __init__(
        self, height:int, width:int, corner_chars:Optional[list[str]]=None,
        horizontal_chars:Optional[list[str]]=None, vertical_chars:Optional[list[str]]=None,
        state:State=DEFAULT_STATE, ob_class:Type[Object]=Object, ob_args=None
    ):
        super().__init__(height, width)
        if ob_args is None:
            ob_args = {}
        if vertical_chars is None:
            vertical_chars = ["|", "|"]
        if horizontal_chars is None:
            horizontal_chars = ["-", "-"]
        if corner_chars is None:
            corner_chars = ["+", "+", "+", "+"]
        self.state = state
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.corner_chars = corner_chars
        self.horizontal_chars = horizontal_chars
        self.vertical_chars = vertical_chars
        self.__gen_obs()

    def __gen_obs(self):
        # Corners
        self.corners = [
            self.ob_class(
                i, arg_proto=self.ob_args, state=self.state
            )
            for i, j in zip(self.corner_chars, range(4))
        ]
        for obj, rx, ry in zip(
            self.corners, [0, self.width - 1, 0, self.width - 1],
            [0, 0, self.height - 1, self.height - 1]
        ):
            self.add_ob(obj, rx, ry)
        # Horizontals
        self.horizontals = [
            Square(
                char=i, width=self.width - 2, height=1,
                state=self.state, ob_class=Object, ob_args=self.ob_args
            )
            for i, j in zip(self.horizontal_chars, range(2))
        ]
        for obj, rx, ry in zip(self.horizontals, [1, 1], [0, self.height - 1]):
            self.add_ob(obj, rx, ry)
        # Verticals
        self.verticals = [
            Square(
                char=i, width=1, height=self.height - 2,
                state=self.state, ob_class=Object, ob_args=self.ob_args
            )
            for i, j in zip(self.vertical_chars, range(2))
        ]
        for obj, rx, ry in zip(self.verticals, [0, self.width - 1], [1, 1]):
            self.add_ob(obj, rx, ry)

    def rechar(self, corner_chars=None, horizontal_chars=None,
               vertical_chars=None):
        """
        Rechars the frame.
        """
        if corner_chars is not None:
            self.corner_chars = corner_chars
        if horizontal_chars is not None:
            self.horizontal_chars = horizontal_chars
        if vertical_chars is not None:
            self.vertical_chars = vertical_chars

        for obj, _c in zip(self.corners, self.corner_chars):
            obj.rechar(_c)
        for obj, _c in zip(self.horizontals, self.horizontal_chars):
            obj.rechar(_c)
        for obj, _c in zip(self.verticals, self.vertical_chars):
            obj.rechar(_c)

    def resize(self, height, width):
        """
        Changes the frames size.
        """
        super().resize(height, width)
        if added := self.added:
            self.remove()
        self.obs = []
        self.__gen_obs()
        if added:
            self.add(self.map, self.x, self.y)
