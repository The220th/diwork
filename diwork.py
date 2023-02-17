#!/usr/bin/env python3

# -*- coding: utf-8 -*-

VERSION = "V0.52"

import os
import sys

__WORK_DIR = os.path.dirname(__file__)

sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/diwork_ways"))
sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/diwork_mains"))

from diwork_ways import pout, Global

from diwork_mains import main_calc_hash, main_clone, main_diff, main_difx, main_repeats, main_exec


if __name__ == "__main__":
    SyntaxError_str = "Syntax error. Expected: \"> python folder_work.py {hash, clone, diff, difx, repeats, exec} ...\""
    argc = len(sys.argv)
    Global.version = VERSION
    if(argc < 2):
        pout(SyntaxError_str)
        exit()
    else:
        sub_modul_name = sys.argv[1]
        if(sub_modul_name == "hash"):
            main_calc_hash(sys.argv[2:])
        elif(sub_modul_name == "clone"):
            main_clone(sys.argv[2:])
        elif(sub_modul_name == "diff"):
            main_diff(sys.argv[2:])
        elif(sub_modul_name == "repeats"):
            main_repeats(sys.argv[2:])
        elif(sub_modul_name == "difx"):
            main_difx(sys.argv[2:])
        elif(sub_modul_name == "exec"):
            main_exec(sys.argv[2:])
        else:
            pout(SyntaxError_str)
            exit()

