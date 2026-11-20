from typing import Self, TypeVar, override

from scrap_engine.addable.area import HasArea
from scrap_engine.addable.state import DEFAULT_STATE, State
from scrap_engine.error import CoordinateError
from scrap_engine.interfaces import IMap

from ..object import ArgProto, Object
from ..object_group import ObjectGroup

T = TypeVar("T", bound=Object)


class Text[T: Object](HasArea, ObjectGroup[T]):
    """
    A datatype containing a string, that can be added to a map.
    Different Texts can be added together with the '+' operator.
    """

    def __init__(
        self,
        text: str,
        state: State = DEFAULT_STATE,
        esccode: str = "",
        ob_class: type[T] = Object,
        ob_args: ArgProto = None,
        ignore: str = "",
    ):
        super().__init__([], state)
        if ob_args is None:
            ob_args = {}
        self.ob_class = ob_class
        self.text: str = text
        self.esccode: str = esccode
        self.ignore: str = ignore
        self.ob_args = ob_args
        self.__texter(text)

    @property
    @override
    def width(self) -> int:
        """
        The Texts peak width
        """
        return max(len(i) for i in self.text.split("\n"))

    @property
    @override
    def height(self) -> int:
        """
        The Texts height
        """
        return len(self.text.split("\n"))

    def __add__(self, other: Self):
        self.text += other.text
        self.obs += other.obs
        for obj in self.obs:
            obj.group = self
        if self.added:
            self.remove()
            self.add(self.map, self.x, self.y)
        return self

    def __texter(self, text: str):
        for txt in text.split("\n"):
            for char in txt:
                if self.esccode != "":
                    char = self.esccode + char + "\033[0m"
                obj = self.ob_class(char, self.state, arg_proto=self.ob_args)
                obj.group = self
                self.obs.append(obj)
        for obj in self.obs:
            obj.group = self

    @override
    def add(self, _map: IMap, x: int, y: int, failsafe: bool = False):
        """
        Adds the text to a certain coordinate on a certain map.
        """
        self.added = True
        self.map = _map
        self.x = x
        self.y = y
        count = 0
        for line, text in enumerate(self.text.split("\n")):
            for i, obj in enumerate(self.obs[count : count + len(text)]):
                if obj.char != self.ignore:
                    try:
                        obj.add(self.map, x + i, y + line)
                    except CoordinateError:
                        if not failsafe:
                            raise
            count += len(text)

    @override
    def remove(self):
        """
        Removes the text from the map.
        """
        self.added = False
        for obj in self.obs:
            obj.remove()

    def rem_ob(self, obj: T):
        """
        Removes an object from the group.
        """
        if obj in self.obs:
            obj.group = None
            index = self.obs.index(obj)
            idx = 0
            while idx < len(self.text):
                if self.text[idx : idx + 2] == "\n":
                    idx += 2
                    continue
                if idx == index:
                    self.text = self.text[:idx] + self.text[idx + 1 :]
                    break
                idx += 1
            self.obs.pop(index)
            return 0
        return 1

    def rechar(self, text: str, esccode: str = "", failsafe: bool = False):
        """
        Changes the string contained in the text.
        """
        self.esccode = esccode
        if self.added:
            for obj in self.obs:
                obj.remove()
        self.obs = []
        self.__texter(text)
        self.text = text
        if self.added:
            self.add(self.map, self.x, self.y, failsafe=failsafe)
