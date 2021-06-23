from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    include_package_data=True,
    name='scrap_engine',
    version='0.1.1',
    py_modules=['scrap_engine'],
    url='https://github.com/lxgr-linux/scrap_engine',
    license='GPL3',
    author='lxgr',
    author_email='lxgr@protonmail.com',
    description='A 2D ascii game engine for the terminal',
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
