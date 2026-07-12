from typing import Literal, Protocol, Self

from scrap_engine.addable.state import State


class IObject(Protocol):
    x: int
    y: int
    state: State
    char: str
    backup: str

    def redraw(self) -> Literal[0, 1]: ...

    def action(self, ob: Self): ...


class IMap(Protocol):
    height: int
    width: int

    def show(self, init: bool = False): ...

    def add_object_to_pos(
        self,
        ob: IObject,
        x: int,
        y: int,
    ) -> str: ...

    def set_object_to_pos(self, ob: IObject, x: int, y: int) -> str: ...

    def get_collision_obs(self, x: int, y: int, state: State) -> list[IObject]: ...

    def remove_ob_from_pos(self, ob: IObject): ...

    def get_char(self, x: int, y: int) -> str: ...

    def set_char(self, char: str, x: int, y: int): ...

    def remove_ob(self, ob: IObject): ...

    def check_collision(self, x: int, y: int) -> bool: ...

    def blur_in(
        self,
        blurmap: Self,
        esccode: str = "\033[37m",
    ): ...

    def resize(
        self,
        height: int,
        width: int,
        background: str = "#",
    ): ...
