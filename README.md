# Scrap_engine
By lxgr <lxgr@protonmail.com>

## Installation
Manually:
```shell
# python setup.py install
```

Via pip (This will just install the latest stable release):
```shell
# python -m pip install scrap_engine
```

From the AUR (When using Arch Linux):
```shell
$ buildaur -S python-scrap_engine-git  # You can use what ever AUR-helper you want
```

To run the examples install python and the pynput module via pip.

See the project on [pypi](https://pypi.org/project/scrap-engine/)

## Usage
See [examples](examples) and [Documentation](docs/DOCS.md). For further documentation see ```pydoc scrap_engine.py```

## Examples and tests
The examples in [examples](examples) are made to show how scrap_engine works in a simple and commented way by, in case of scrap_test, building a little game. For more examples you can look at [tests](tests) which also contain explanatory programs.

They can be ran by either installing scrap_engine like in the installation section or by moving the ```scrap_engine.py``` file in their directories, and then just executing them.

Another source to understand the functionality of scrap_engine is the small snake implementation [scrape](https://github.com/lxgr-linux/scrape), that was firstly designed to be a tutorial but was later split out due to it's size. This may also help to implement a proper game using scrap_engine.

## Notes
The examples and tests where all tested on Arch Linux x86 and Windows 10.
