from abc import ABC, abstractmethod
from typing import Optional

from ..map.map import Map
from .state import DEFAULT_STATE, State


class Addable(ABC):
    """
    The parent class of any object that can be added to a Map.
    """

    def __init__(self, state: State = DEFAULT_STATE):
        self.x: int = -1
        self.y: int = -1
        # Those are the relativ coordinated used, when grouped
        self.rx = None
        self.ry = None
        self.added: bool = False
        self.group = None
        self.state: State = state
        self.map: Optional[Map] = None

    def set_state(self, state: State):
        self.state = state

    @abstractmethod
    def add(self, _map: Map, x: int, y: int): ...

    @abstractmethod
    def remove(self): ...

    @abstractmethod
    def set(self, x: int, y: int): ...
