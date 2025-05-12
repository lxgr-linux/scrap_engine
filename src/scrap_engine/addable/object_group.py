from .addable import Addable
from .state import DEFAULT_STATE, State


class ObjectGroup(Addable):
    """
    A datatype used to group objects together and do things with them
    simultaniuously.
    """

    def __init__(self, obs, state: State = DEFAULT_STATE):
        super().__init__(state)
        self.obs = obs
        for obj in obs:
            obj.group = self

    def add_ob(self, obj):
        """
        Adds and object to the group.
        """
        self.obs.append(obj)
        obj.group = self

    def add_obs(self, obs):
        """
        Adds a list of objects to th group.
        """
        for obj in obs:
            self.add_ob(obj)

    def rem_ob(self, obj):
        """
        Removes an object from the group.
        """
        if obj in self.obs:
            obj.group = None
            self.obs.pop(self.obs.index(obj))
            return 0
        return 1

    def move(self, x=0, y=0):
        """
        Moves all objects in the group by a certain vector.
        """
        for obj in self.obs:
            obj.remove()
        for obj in self.obs:
            obj.add(self.map, obj.x + x, obj.y + y)

    def remove(self):
        """
        Removes all objects from their maps.
        """
        for obj in self.obs:
            obj.remove()

    def set(self, x: int, y: int):
        """
        Sets the group to a certain coordinate.
        !!! Just use this with inherited classes !!!
        """
        self.move(x - self.x, y - self.y)
        self.x = x
        self.y = y

    def set_state(self, state: State):
        """
        Sets all objects states to a certain state.
        """
        super().set_state(state)
        for obj in self.obs:
            obj.set_state(state)
