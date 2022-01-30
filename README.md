# docov

Light-weight, recursive docstring coverage analysis for python modules. 

## Overview

`docov` provides light-weight docstring coverage analysis for python modules. 
It recursively collects symbols defined by the specified module and checks whether these
symbols have docstrings and if they are longer than at least 20 symbols.

## Installation

`docov` is available via [PyPI](https://pypi.org/project/docov/):
```
$ pip install docov
```

## Usage

Once installed, `docov` can be used from the command-line
```
$ docov <module-name>
```
which will produce a badge and a report on symbols, which were deemed to have insufficient docstring.

A short help text on available options can be found with

```
$ docov -h
usage: docov [-h] [-o OUTPUT] [-d DEPTH] [--no-badge] [--no-report] MODULE

Command line utility to analyze docstring coverage of python modules.
Works by recursively fetching the module's symbol's docstrings and 
checking that hey are non-empty and consist of at least 20 characters.
Generates a badge and a report if not specified otherwise.

positional arguments:
  MODULE                The module which is to be analyzed.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory.
  -d DEPTH, --depth DEPTH
                        Analysis recursion depth.
  --no-badge            Generate a badge in <output>/docov.svg.
  --no-report           Generate a report in <output>/docov.txt.
```
