from scrap_engine.addable.state import DEFAULT_STATE
from ..object_group import ObjectGroup

class Box(ObjectGroup):
    """
    A datastucture used to group objects(groups) relative to a certain
    coordinate, that can be added to a map.
    """

    def __init__(self, height:int, width:int):
        super().__init__([], DEFAULT_STATE)
        self.height:int = height
        self.width:int = width

    def add(self, _map, x:int, y:int):
        """
        Adds the box to a certain coordinate on a certain map.
        """
        self.x = x
        self.y = y
        self.map = _map
        for obj in self.obs:
            obj.add(self.map, obj.rx + self.x, obj.ry + self.y)
        self.added = True

    def add_ob(self, obj, x:int, y:int):
        """
        Adds an object(group) to a certain coordinate relative to the box.
        """
        self.obs.append(obj)
        obj.rx = x
        obj.ry = y
        obj.group = self
        if self.added:
            obj.add(self.map, obj.rx + self.x, obj.ry + self.y)

    def set_ob(self, obj, x, y):
        """
        Sets an object(group) to a certain coordinate relative to the box.
        """
        obj.rx = x
        obj.ry = y
        if self.added:
            obj.set(obj.rx + self.x, obj.ry + self.y)

    def remove(self):
        """
        Removes the box from the map.
        """
        for obj in self.obs:
            obj.remove()
        self.added = False

    def resize(self, height, width):
        """
        Resizes the box.
        """
        self.height = height
        self.width = width
