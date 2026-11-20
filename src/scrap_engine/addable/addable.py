from abc import abstractmethod
from typing import Literal, Optional, Protocol

from scrap_engine.interfaces import IMap

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
    map: IMap | None

    def __init__(self, state: State = DEFAULT_STATE):
        self.x: int = -1
        self.y: int = -1
        # Those are the relativ coordinated used, when grouped
        self.rx: int = -1
        self.ry: int = -1
        self.added: bool = False
        self.group: Addable | None = None
        self.state: State = state
        self.map: IMap | None = None

    def set_state(self, state: State):
        self.state = state

    @abstractmethod
    def add(self, _map: IMap, x: int, y: int) -> Literal[0, 1] | None: ...

    @abstractmethod
    def remove(self) -> Literal[0, 1] | None: ...

    @abstractmethod
    def set(self, x: int, y: int) -> Literal[0, 1] | None: ...
