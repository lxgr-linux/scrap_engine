from typing import Type
from scrap_engine.addable.state import DEFAULT_STATE, State
from ..object_group import ObjectGroup
from ..object import Object


class Text(ObjectGroup):
    """
    A datatype containing a string, that can be added to a map.
    Different Texts can be added together with the '+' operator.
    """

    def __init__(
        self, text, state:State=DEFAULT_STATE, esccode="",
        ob_class:Type[Object]=Object, ob_args=None, ignore=""
    ):
        super().__init__([], state)
        if ob_args is None:
            ob_args = {}
        self.ob_class = ob_class
        self.text = text
        self.esccode = esccode
        self.ignore = ignore
        self.ob_args = ob_args
        self.__texter(text)

    @property
    def width(self):
        """
        The Texts peak width
        """
        return sorted(len(i) for i in self.text.split("\n"))[-1]

    @property
    def height(self):
        """
        The Texts height
        """
        return len(self.text.split("\n"))

    def __add__(self, other):
        self.text += other.text
        self.obs += other.obs
        for obj in self.obs:
            obj.group = self
        if self.added:
            self.remove()
            self.add(self.map, self.x, self.y)
        return self

    def __texter(self, text):
        for txt in text.split("\n"):
            for char in txt:
                if self.esccode != "":
                    char = self.esccode + char + "\033[0m"
                obj = self.ob_class(
                    char, self.state, arg_proto=self.ob_args
                )
                obj.group = self
                self.obs.append(obj)
        for obj in self.obs:
            obj.group = self

    def add(self, _map, x, y):
        """
        Adds the text to a certain coordinate on a certain map.
        """
        self.added = True
        self.map = _map
        self.x = x
        self.y = y
        count = 0
        for l, text in enumerate(self.text.split("\n")):
            for i, obj in enumerate(self.obs[count:count + len(text)]):
                if obj.char != self.ignore:
                    obj.add(self.map, x + i, y + l)
            count += len(text)

    def remove(self):
        """
        Removes the text from the map.
        """
        self.added = False
        for obj in self.obs:
            obj.remove()

    def rem_ob(self, obj):
        """
        Removes an object from the group.
        """
        if obj in self.obs:
            obj.group = None
            index = self.obs.index(obj)
            idx = 0
            while idx < len(self.text):
                if self.text[idx:idx+2] == "\n":
                    idx += 2
                    continue
                if idx == index:
                    self.text = self.text[:idx] + self.text[idx + 1:]
                    break
                idx += 1
            self.obs.pop(index)
            return 0
        return 1

    def rechar(self, text, esccode=""):
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
            self.add(self.map, self.x, self.y)
