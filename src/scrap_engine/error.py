class CoordinateError(Exception):
    """
    An Error that is thrown, when an object is added to a non-existing
    part of a map.
    """

    def __init__(self, obj, _map, x, y):
        self.ob = obj
        self.x = x
        self.y = y
        self.map = _map
        super().__init__(
            f"The {obj}s coordinate ({x}|{y}) is "
            f"not in {self.map.width - 1}x{self.map.height - 1}"
        )
