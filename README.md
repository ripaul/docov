# docov

![docov](https://github.com/ripaul/docov/actions/workflows/main.yml/docov.svg)

Light-weight, recursive docstring coverage analysis for python modules. 

## Overview

`docov` provides light-weight docstring coverage analysis for python modules. 
It recursively collects symbols defined by the specified module and checks whether these
symbols have docstrings and if they are longer than at least 20 symbols.

The docstring coverage is computed simply as the fraction of symbols which are deemed
to have a sufficient docstring and the total number of symbols found.

The command-line utility will generate a badge indicating the docstring coverage and 
a report listing all symbols found in the module, which do not have sufficient
docstrings.

In order to not distort the docstring coverage, symbols and modules (and their symbols)
can be ignored in the analysis. 
This allows for some fine-tuning in really only considering the desired module's symbols.
Builtin types are currently always ignored, meaning that e.g. methods of a string object
in a module will not be assessed.

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
usage: docov [-h] [-o DIR] [-p PREFIX] [-i SYMBOL [SYMBOL ...]] [-d DEPTH] [--no-badge] [--no-report] MODULE

Command line utility to analyze docstring coverage of python modules.
Works by recursively fetching the module's symbol's docstrings and 
checking that they consist of at least 20 characters.

Generates a SVG-badge and a report if not specified otherwise, stored in
DIR/[PREFIX_]docov.svg and DIR/[PREFIX_]docov.txt respectively.

positional arguments:
  MODULE                The module which is to be analyzed.

optional arguments:
  -h, --help            show this help message and exit
  -o DIR, --output DIR  Output directory.
  -p PREFIX, --prefix PREFIX
                        Output file prefix: PREFIX_docov.[txt,svg]
  -i SYMBOL [SYMBOL ...], --ignore SYMBOL [SYMBOL ...]
                        Ignore symbols. If the symbol names a module, all its types will be ignored in the recursion.
  -d DEPTH, --depth DEPTH
                        Analysis recursion depth.
  --no-badge            Suppress badge generation.
  --no-report           Suppress report generation.

```
