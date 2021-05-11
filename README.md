# Scrap_engine
by LXGR <lxgr@protonmail.com>

## Installation
Linux:
Copy scrap_engine.py to /usr/lib/python3.9/site-packages.
```shell
# cp ./scrap_engine.py /usr/lib/python3.9/site-packages
```

Windoofs:
Move the ```scrap_engine.py``` file somehow into your python path.

To run the examples install python and the pynput module via pip. Then just run what ever file you want (for example scrape).

## Usage
See examples and [Documentation](docs/DOCS.md)

## File explaination
- LICENSE : obvious
- README.md : ...
- scrap_engine.py : Python module that contains the engine
- scrap_test.py : file that explains basic functionality of scrap_engine and tests them
- scrap_bench.py : little benchmarking tool that shows frametimes and does some nice looking calculations
- scrape.py : implimentation of snake
- lil_t.py : implimentation of a basic jump and run game

## Notes
Scrap_engine, scrap_test.py and scrape.py where all tested working in the xfce4-terminal terminal emulator, other terminal emulators will work for sure.

## Examples and tests
The examples and tests in ```tests``` and ```examples``` can be ran by either installing scrap_engine like in the installation section or by moving the ```scrap_engine.py``` file in their directorys, and then just executing them.
The examples are resources to understand the key functionality ot scrap_engine and the tests are just used to test some of those functions.
For example for scrape see [scrape](examples/README.md).
