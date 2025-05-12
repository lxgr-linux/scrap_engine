import functools

from ..consts import MAXCACHE_FRAME, MAXCACHE_LINE, screen_height, screen_width


class Map:
    """
    The map, objects can be added to.
    """

    def __init__(
        self,
        height=screen_height - 1,
        width=screen_width,
        background="#",
        dynfps=True,
    ):
        self.height = height
        self.width = width
        self.dynfps = dynfps
        self.background = background
        self.map = [
            [self.background for _ in range(width)] for _ in range(height)
        ]
        self.obmap = [[[] for _ in range(width)] for _ in range(height)]
        self.obs = []
        self.out_old = ""

    def blur_in(self, blurmap, esccode="\033[37m"):
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

    def show(self, init=False):
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
    def __show_map(show_line, _map):
        out = "\033[H"
        for arr in _map:
            out += show_line(arr)
        return out

    @staticmethod
    @functools.lru_cache(MAXCACHE_LINE)
    def __show_line(arr):
        out_line = ""
        for char in arr:
            out_line += char
        return out_line

    def resize(self, height, width, background="#"):
        """
        Resizes the map to a certain size.
        """
        self.background = background
        self.map = [
            [self.background for _ in range(width)] for _ in range(height)
        ]
        self.obmap = [
            [[] for _ in range(width if width > self.width else self.width)]
            for _ in range(height if height > self.height else self.height)
        ]
        self.width = width
        self.height = height
        for obj in self.obs:
            if obj.y < height and obj.x < width:
                self.obmap[obj.y][obj.x].append(obj)
                obj.redraw()
