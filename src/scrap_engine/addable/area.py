from abc import ABC, abstractmethod

from scrap_engine.addable.addable import Addable

type Area = tuple[tuple[int, int], tuple[int, int]]


class HasArea(Addable, ABC):
    @property
    @abstractmethod
    def height(self) -> int: ...

    @property
    @abstractmethod
    def width(self) -> int: ...

    def get_area(self) -> Area:
        return (
            (self.x, self.y),
            (self.x + self.width - 1, self.y + self.height - 1),
        )
