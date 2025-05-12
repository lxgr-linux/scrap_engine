#!/usr/bin/env python3
"""
Ascii game engine for the terminal.

The main data structures are Map and Object.
Maps are objects, Object objects can be added to and then can be shown on
the screen.

ObjectGroup and their daughters can be used to automate generating, adding,
removing etc. for a list of objects in their defined manner.

States:
    Possible states an object can have are 'solid' and 'float'.
    If an objects state is 'solid' no other object can be set over it,
    so the other objects .set() method will return 1.
    If an objects state is 'float' other objects can be set over them,
    so their .set() methods will return 0.

arg_proto:
    arg_proto is an dictionary that is given to an object by
    the programmer or an object_group(circle, frame, etc.) via the ob_args
    argument.
    This can be used to store various extra values and is especially useful
    when using daughter classes of Object that needs extra values.

This software is licensed under the GPL3
You should have gotten an copy of the GPL3 license alongside this software
Feel free to contribute what ever you want to this engine
You can contribute here: https://github.com/lxgr-linux/scrap_engine
"""

__author__ = "lxgr <lxgr@protonmail.com>"
__version__ = "1.4.4"

from .addable import *
from .consts import *
from .error import CoordinateError
from .map import *
