# Scrap_engine
by LXGR <lxgr@protonmail.com>

# Installation
Linux:
Copy scrap_engine.py to /usr/lib/python3.9/site-packages

Windoofs:
Idk, you will figure it out.

# Usage
See scrap_test.py

# Dependencies
scrap_test.py and scrape.py both require pynput when running on windows

# File explaination
LICENSE : obvious<br>
README.md : ...<br>
scrap_engine.py : Python module that contains the engine<br>
scrap_engine.cpp : the same but just in c++, is just a proof of concept<br>
a.out : the compiled version of scrap_engine.cpp (x86_64)<br>
scrap_test.py : file that explains basic functionality of scrap_engine and tests them<br>
scrape.py : implimentation of snake<br>
lil_t.py : implimentation of a basic jump and run game<br>
reader.sh : shellscript thats needed to read keyboard input without a running xserver<br>

# Notes
Scrap_engine, scrap_test.py and scrape.py where all tested working in the xfce4-terminal terminal emulator, other terminal emulators will work for sure.
For reading keyboard input in TTY or via ssh or telnet you may use reader.sh to capture the keyboard like demonstrated in scrape.py and lil_t.py instead of pynput.
