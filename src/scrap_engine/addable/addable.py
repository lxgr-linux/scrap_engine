from abc import abstractmethod
from typing import Optional, Protocol

from scrap_engine.interfaces import IMap

from ..map.map import Map
from .state import DEFAULT_STATE, State


class Addable(Protocol):
    """
    The parent class of any object that can be added to a Map.
    """

    x: int
    y: int
    rx: int
    ry: int
    added: bool
    group: Optional["Addable"]
    state: State
    map: Optional[IMap]

    def __init__(self, state: State = DEFAULT_STATE):
        self.x: int = -1
        self.y: int = -1
        # Those are the relativ coordinated used, when grouped
        self.rx: int = -1
        self.ry: int = -1
        self.added: bool = False
        self.group: Optional[Addable] = None
        self.state: State = state
        self.map: Optional[IMap] = None

    def set_state(self, state: State):
        self.state = state

    @abstractmethod
    def add(self, _map: Map, x: int, y: int): ...

    @abstractmethod
    def remove(self): ...

    @abstractmethod
    def set(self, x: int, y: int): ...
