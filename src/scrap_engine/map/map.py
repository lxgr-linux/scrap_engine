import functools
from typing import Callable, override

from scrap_engine.addable.state import State
from scrap_engine.interfaces import IMap, IObject

from ..consts import MAXCACHE_FRAME, MAXCACHE_LINE, screen_height, screen_width


class Map(IMap):
    """
    The map, objects can be added to.
    """

    def __init__(
        self,
        height: int = screen_height - 1,
        width: int = screen_width,
        background: str = "#",
        dynfps: bool = True,
    ):
        self.height: int = height
        self.width: int = width
        self.dynfps: bool = dynfps
        self.background: str = background
        self.map: list[list[str]] = [
            [self.background for _ in range(width)] for _ in range(height)
        ]
        self.obmap: list[list[list[IObject]]] = [
            [[] for _ in range(width)] for _ in range(height)
        ]
        self.obs: list[IObject] = []
        self.out_old: str = ""

    @override
    def remove_ob_from_pos(self, ob: IObject):
        if len(self.obmap[ob.y][ob.x]) > self.obmap[ob.y][ob.x].index(ob) + 1:
            self.obmap[ob.y][ob.x][
                self.obmap[ob.y][ob.x].index(ob) + 1
            ].backup = ob.backup
        else:
            self.map[ob.y][ob.x] = ob.backup
        del self.obmap[ob.y][ob.x][self.obmap[ob.y][ob.x].index(ob)]

    @override
    def get_char(self, x: int, y: int) -> str:
        return self.map[y][x]

    @override
    def set_char(self, char: str, x: int, y: int):
        self.map[y][x] = char

    @override
    def remove_ob(self, ob: IObject):
        self.remove_ob_from_pos(ob)
        del self.obs[self.obs.index(ob)]

    @override
    def check_collision(self, x: int, y: int) -> bool:
        return len(lis := self.obmap[y][x]) != 0 and lis[-1].state == "solid"

    @override
    def add_object_to_pos(self, ob: IObject, x: int, y: int) -> str:
        self.obs.append(ob)
        return self.set_object_to_pos(ob, x, y)

    @override
    def get_collision_obs(self, x: int, y: int, state: State) -> list[IObject]:
        return [obj for obj in self.obmap[y][x] if obj.state == state]

    @override
    def set_object_to_pos(self, ob: IObject, x: int, y: int) -> str:
        backup = self.map[y][x]
        self.map[y][x] = ob.char
        self.obmap[y][x].append(ob)
        return backup

    @override
    def blur_in(self, blurmap: "Map", esccode: str = "\033[37m"):
        """
        Sets another maps content as its background.
        """
        for h in range(self.height):
            for w in range(self.width):
                if blurmap.map[h][w] != " ":
                    self.map[h][w] = (
                        esccode
                        + blurmap.map[h][w].replace("\033[0m", "")[-1]
                        + "\033[0m"
                    )
                else:
                    self.map[h][w] = " "
        for obj in self.obs:
            obj.redraw()

    @override
    def show(self, init: bool = False):
        """
        Prints the maps content.
        """
        _map = (tuple(arr) for arr in self.map)
        out = self.__show_map(self.__show_line, _map)
        if self.out_old != out or not self.dynfps or init:
            print(out + "\n\033[0E\033[2K", end="")
            self.out_old = out

    @staticmethod
    @functools.lru_cache(MAXCACHE_FRAME)
    def __show_map(
        show_line: Callable[[tuple[str]], str], _map: tuple[tuple[str]]
    ) -> str:
        out = "\033[H"
        for arr in _map:
            out += show_line(arr)
        return out

    @staticmethod
    @functools.lru_cache(MAXCACHE_LINE)
    def __show_line(arr: tuple[str]) -> str:
        out_line = ""
        for char in arr:
            out_line += char
        return out_line

    @override
    def resize(self, height: int, width: int, background: str = "#"):
        """
        Resizes the map to a certain size.
        """
        self.background = background
        self.map = [[self.background for _ in range(width)] for _ in range(height)]
        self.obmap = [
            [[] for _ in range(max(width, self.width))]
            for _ in range(max(height, self.height))
        ]
        self.width = width
        self.height = height
        for obj in self.obs:
            if obj.y < height and obj.x < width:
                self.obmap[obj.y][obj.x].append(obj)
                obj.redraw()
