#!/usr/bin/env python3
"""
docov

Light-weight, recursive docstring coverage analysis for python modules.
"""

from . docov import *
from . docov import *
from . docov import *
del docov

class _submodules:
    import argparse
    import importlib

def parse_args():
    """Parse the command line arguments."""

    parser = _submodules.argparse.ArgumentParser(formatter_class=_submodules.argparse.RawDescriptionHelpFormatter,
                                     description='''\
Command line utility to analyze docstring coverage of python modules.
Works by recursively fetching the module's symbol's docstrings and 
checking that hey are non-empty and consist of at least 20 characters.
Generates a badge and a report if not specified otherwise.
''')

    parser.add_argument('-o', '--output', type=str, help='Output directory.', default=".")
    parser.add_argument('-d', '--depth', type=int, help='Analysis recursion depth.', default=3)
    parser.add_argument('--no-badge', action="store_true", help='Generate a badge in <output>/docov.svg.')
    parser.add_argument('--no-report', action="store_true", help='Generate a report in <output>/docov.txt.')
    parser.add_argument('module', metavar='MODULE', type=str, help='The module which is to be analyzed.')

    return parser.parse_args()


def main(args = None):
    """
        Command line utility main function.

        Parameters:
            args: command line arguments as returned from argparse.parse_args()
    """
    if args is None:
        args = parse_args()

    module = _submodules.importlib.import_module(args.module)
    result = analyze(module, depth = args.depth)

    if not args.no_badge:
        create_badge(*result, output = args.output)

    if not args.no_report:
        create_report(*result, output = args.output)


if __name__ == "__main__":
    main()
