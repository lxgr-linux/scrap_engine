import functools

from ..consts import screen_height, screen_width
from .map import Map


class Submap(Map):
    """
    Behaves just like a map, but it self contains a part of another map.
    """

    def __init__(
        self,
        bmap,
        x,
        y,
        height=screen_height - 1,
        width=screen_width,
        dynfps=True,
    ):
        super().__init__(height, width, dynfps=dynfps)
        del self.background
        self.y = y
        self.x = x
        self.bmap = bmap
        self.remap()

    def remap(self):
        """
        Updates the map (rereads the map, the submap contains a part from)
        """
        self.map = self.__full_bg(self.bmap.background, self.width, self.height)
        self.map = self.__map_to_parent(
            self.height,
            self.width,
            self.y,
            self.x,
            (tuple(line) for line in self.map),
            (tuple(line) for line in self.bmap.map),
        )
        for obj in self.obs:
            obj.redraw()

    @staticmethod
    @functools.lru_cache()
    def __map_to_parent(height, width, _y, _x, parent, child):
        parent = [list(line) for line in parent]
        child = [list(line) for line in child]
        for sy, y in zip(range(0, height), range(_y, _y + height)):
            for sx, x in zip(range(0, width), range(_x, _x + width)):
                try:
                    parent[sy][sx] = child[y][x]
                except IndexError:
                    continue
        return parent

    @staticmethod
    @functools.lru_cache(1)
    def __full_bg(background, width, height):
        return [[background for _ in range(width)] for _ in range(height)]

    def set(self, x, y):
        """
        Changes the coordinates on the map, the submap is at.
        """
        if x < 0 or y < 0:
            return 1
        self.x = x
        self.y = y
        self.remap()
        return 0

    def full_show(self, init=False):
        """
        Combines remap() and show().
        """
        self.remap()
        self.show(init)
