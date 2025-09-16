from scrap_engine.addable.addable import Addable
from scrap_engine.addable.area import HasArea
from scrap_engine.addable.object_group import ObjectGroup
from scrap_engine.addable.state import DEFAULT_STATE


class Box(ObjectGroup[Addable], HasArea):
    """
    A datastucture used to group objects(groups) relative to a certain
    coordinate, that can be added to a map.
    """

    def __init__(self, height: int, width: int):
        super().__init__([], DEFAULT_STATE)
        self.__height: int = height
        self.__width: int = width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def add(self, _map, x: int, y: int):
        """
        Adds the box to a certain coordinate on a certain map.
        """
        self.x = x
        self.y = y
        self.map = _map
        for obj in self.obs:
            obj.add(self.map, obj.rx + self.x, obj.ry + self.y)
        self.added = True

    def add_ob(self, obj: Addable, x: int, y: int):
        """
        Adds an object(group) to a certain coordinate relative to the box.
        """
        if self.is_ob_added(obj):
            self.set_ob(obj, x, y)
            return
        obj.rx = x
        obj.ry = y
        super().add_ob(obj)
        if self.added:
            obj.add(self.map, obj.rx + self.x, obj.ry + self.y)

    def set_ob(self, obj: Addable, x: int, y: int):
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

    def resize(self, height: int, width: int):
        """
        Resizes the box.
        """
        self.__height = height
        self.__width = width
