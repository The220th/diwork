# -*- coding: utf-8 -*-

import os
import sys
import argparse

from . import Global

def common_init_parser(parser: "ArgumentParser") -> "ArgumentParser":
    # https://docs.python.org/3/library/argparse.html
    # https://stackoverflow.com/questions/20063/whats-the-best-way-to-parse-command-line-arguments

    parser.add_argument("--dublicate_out_to_file", type=str, default=None,
                       help="Duplicate program output to file")

    parser.add_argument("--hash_mode", type=int, choices=[0,1,2], default=0,
                       help="Hash mode: 0 is sha256sum, 1 is hashlib.sha256, 2 is sha512sum. Default 0.")

    return parser

def common_init_parse(args: "ArgumentParser.parse_args") -> None:
    Global.outfile = args.dublicate_out_to_file
    Global.hash_mode = args.hash_mode