from ..consts import DEFAULT_STATE

class Addable:
    """
    The parent class of any object that can be added to a Map.
    """

    def __init__(self, state=None):
        self.x = None
        self.y = None
        # Those are the relativ coordinated used, when grouped
        self.rx = None
        self.ry = None
        self.added = False
        self.group = None
        if state is None:
            self.state = DEFAULT_STATE
        else:
            self.state = state
        self.map = None
