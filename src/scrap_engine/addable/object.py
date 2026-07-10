from typing import Any, Optional, override

from scrap_engine.interfaces import IMap, IObject

from ..error import CoordinateError
from .addable import Addable
from .area import HasArea
from .state import DEFAULT_STATE, State

type ArgProto = Optional[dict[str, Any]]  # pyright: ignore[reportExplicitAny]


class Object(HasArea, Addable):
    """
    An object, containing a character, that can be added to a map.
    """

    def __init__(
        self, char: str, state: State = DEFAULT_STATE, arg_proto: ArgProto = None
    ):
        if arg_proto is None:
            arg_proto = {}
        super().__init__(state)
        self.char: str = char
        self.arg_proto = arg_proto
        self.backup: str = ""

    def add(self, _map: IMap, x: int, y: int):
        """
        Adds the object to a certain coordinate on a certain map.
        """
        if not 0 <= x < _map.width or not 0 <= y < _map.height:
            raise CoordinateError(self, _map, x, y)
        if _map.check_collision(x, y):
            return 1
        self.x = x
        self.y = y
        self.backup = _map.add_object_to_pos(self, x, y)
        self.map = _map
        self.added = True
        return 0

    def set(self, x: int, y: int):
        """
        Sets the object to a certain coordinate.
        """
        assert self.map
        if not self.added:
            return 1
        elif not (0 <= x < self.map.width and 0 <= y < self.map.height):
            self.bump(None, x - self.x, y - self.y, side=True)
            return 1
        elif self.x > self.map.width - 1 or self.y > self.map.height - 1:
            self.pull_ob()
            return 1
        for obj in self.map.get_collision_obs(x, y, "solid"):
            self.bump(obj, x - self.x, y - self.y)
            return 1
        self.map.remove_ob_from_pos(self)
        self.backup = self.map.set_object_to_pos(self, x, y)
        self.x = x
        self.y = y
        for obj in self.map.get_collision_obs(x, y, "float"):
            obj.action(self)
        return 0

    def redraw(self):
        """
        Redraws the object on the map.
        """
        if not self.added:
            return 1
        assert self.map
        self.backup = self.map.get_char(self.x, self.y)
        self.map.set_char(self.char, self.x, self.y)
        return 0

    @property
    @override
    def height(self) -> int:
        return 1

    @property
    @override
    def width(self) -> int:
        return 1

    def action(self, ob: IObject):
        """
        This is triggered when another object is set over this one.
        """
        return

    def bump(self, ob, x: int, y: int, side=False):
        """
        This is triggered, when this object is tried to be set onto another
        solid object. Or it hits the side of the map, in which case `side == True`.
        `x` and `ỳ` are the vectore self should have been set to.
        """
        return

    def pull_ob(self):
        """
        This is triggered, when trying to set an object from a non existing
        spot on the map to an existing one.
        This is just usefull when resizing maps with objects out of the
        new size.
        """
        return

    def rechar(self, char: str):
        """
        Changes the objects character.
        """
        self.char = char
        if not self.added:
            return 1
        assert self.map
        self.map.set_char(self.backup, self.x, self.y)
        self.redraw()
        return 0

    @override
    def __repr__(self) -> str:
        return f"Object[{self.char}]"

    @override
    def remove(self):
        """
        Removes the object from the map.
        """
        if not self.added:
            return 1
        assert self.map
        self.added = False
        self.map.remove_ob(self)
        return 0
