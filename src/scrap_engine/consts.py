import os

MAXCACHE_LINE = 512
MAXCACHE_FRAME = 64

try:
    screen_width, screen_height = os.get_terminal_size()
except OSError:
    screen_width, screen_height = 100, 100
