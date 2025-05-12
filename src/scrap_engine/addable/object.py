from ..error import CoordinateError
from ..map.map import Map
from .addable import Addable
from .state import DEFAULT_STATE, State


class Object(Addable):
    """
    An object, containing a character, that can be added to a map.
    """

    def __init__(self, char: str, state: State = DEFAULT_STATE, arg_proto=None):
        if arg_proto is None:
            arg_proto = {}
        super().__init__(state)
        self.char: str = char
        self.arg_proto = arg_proto
        self.backup = None

    def add(self, _map: Map, x: int, y: int):
        """
        Adds the object to a certain coordinate on a certain map.
        """
        if not 0 <= x < _map.width or not 0 <= y < _map.height:
            raise CoordinateError(self, _map, x, y)
        if len(lis := _map.obmap[y][x]) != 0 and lis[-1].state == "solid":
            return 1
        self.backup = _map.map[y][x]
        self.x = x
        self.y = y
        _map.map[y][x] = self.char
        _map.obmap[y][x].append(self)
        _map.obs.append(self)
        self.map = _map
        self.added = True
        return 0

    def set(self, x: int, y: int):
        """
        Sets the object to a certain coordinate.
        """
        if not self.added:
            return 1
        elif not (0 <= x < self.map.width and 0 <= y < self.map.height):
            self.bump(None, x - self.x, y - self.y, side=True)
            return 1
        elif self.x > self.map.width - 1 or self.y > self.map.height - 1:
            self.pull_ob()
            return 1
        for obj in self.map.obmap[y][x]:
            if obj.state == "solid":
                self.bump(obj, x - self.x, y - self.y)
                return 1
        self.__backup_setter()
        self.map.obmap[y][x].append(self)
        self.backup = self.map.map[y][x]
        self.x = x
        self.y = y
        self.map.map[y][x] = self.char
        for obj in self.map.obmap[y][x]:
            if obj.state == "float":
                obj.action(self)
        return 0

    def redraw(self):
        """
        Redraws the object on the map.
        """
        if not self.added:
            return 1
        self.backup = self.map.map[self.y][self.x]
        self.map.map[self.y][self.x] = self.char
        return 0

    def __backup_setter(self):
        if (
            len(self.map.obmap[self.y][self.x])
            > self.map.obmap[self.y][self.x].index(self) + 1
        ):
            self.map.obmap[self.y][self.x][
                self.map.obmap[self.y][self.x].index(self) + 1
            ].backup = self.backup
        else:
            self.map.map[self.y][self.x] = self.backup
        del self.map.obmap[self.y][self.x][
            self.map.obmap[self.y][self.x].index(self)
        ]

    def action(self, ob):
        """
        This is triggered when another object is set over this one.
        """
        return

    def bump(self, ob, x, y, side=False):
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

    def rechar(self, char):
        """
        Changes the objects character.
        """
        self.char = char
        if not self.added:
            return 1
        self.map.map[self.y][self.x] = self.backup
        self.redraw()
        return 0

    def remove(self):
        """
        Removes the object from the map.
        """
        if not self.added:
            return 1
        self.added = False
        self.__backup_setter()
        del self.map.obs[self.map.obs.index(self)]
        return 0
