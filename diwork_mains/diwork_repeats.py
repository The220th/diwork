# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_repeats(args: list):
    argc = len(args)
    if(argc != 1):
        pout("Syntax error. Expected: \"python folder_work.py repeats {folder_path}\"")
        exit()
    folder = args[0]
    err_out = []
    folder_abs = os.path.abspath(folder)
    if(is_folder(folder_abs) == False):
        pout(f"\"{folder_abs}\" is not folder. ")
        exit()
    files_abs = sorted(getFilesList(folder_abs))
    hashes = set()
    d = {}
    gi, N = 0, len(files_abs)
    for file_i in files_abs:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        if(file_i_hash not in hashes):
            hashes.add(file_i_hash)
            d[file_i_hash] = [file_i]
        else:
            d[file_i_hash].append(file_i)

    pout("\n===============\nIdentical files: ")
    IF_AT_LEAST_ONE = False
    hashesss = list(d.keys())
    for hash_i in hashesss:
        fl = d[hash_i]
        if(len(fl) > 1):
            IF_AT_LEAST_ONE = True
            pout(f"* Hash \"{hash_i}\" have files: ")
            for file_i in fl:
                pout(f"\t{file_i}")
            pout("")
    if(IF_AT_LEAST_ONE == False):
        pout("\tNo such files")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")
