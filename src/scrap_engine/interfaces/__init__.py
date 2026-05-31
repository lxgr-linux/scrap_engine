from typing import Literal, Protocol

from scrap_engine.addable.state import State


class IObject(Protocol):
    x: int
    y: int
    state: State

    def redraw(self) -> Literal[0, 1]: ...


class IMap(Protocol):
    def show(self, init: bool = False): ...

    def blur_in(
        self,
        blurmap: "IMap",
        esccode: str = "\033[37m",
    ): ...

    def resize(
        self,
        height: int,
        width: int,
        background: str = "#",
    ): ...
