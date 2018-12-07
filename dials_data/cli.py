from __future__ import absolute_import, division, print_function

import argparse
import sys
from .datasets import cli_show


def main():
    parser = argparse.ArgumentParser(
        usage="dials.data <command> [<args>]",
        description="""DIALS regression data manager

The most commonly used commands are:
   show     Show available data sets
   get      Download data sets
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("subcommand", help=argparse.SUPPRESS)
    # parse_args defaults to [1:] for args, but need to
    # exclude the rest of the args too, or validation will fail
    parameters = sys.argv[1:2]
    if not parameters:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args(parameters)
    subcommand = globals().get("cli_" + args.subcommand)
    if subcommand:
        return subcommand(sys.argv[2:])
    parser.print_help()
    print()
    sys.exit("Unrecognized command: {}".format(args.subcommand))
