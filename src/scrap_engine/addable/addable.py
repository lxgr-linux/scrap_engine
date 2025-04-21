from typing import Optional

from scrap_engine.addable.state import DEFAULT_STATE, State
from scrap_engine.map.map import Map

class Addable:
    """
    The parent class of any object that can be added to a Map.
    """

    def __init__(self, state:State=DEFAULT_STATE):
        self.x = None
        self.y = None
        # Those are the relativ coordinated used, when grouped
        self.rx = None
        self.ry = None
        self.added:bool = False
        self.group = None
        self.state: State = state
        self.map: Optional[Map] = None
