# -*- coding: utf-8 -*-

import os
import sys
import argparse

from diwork_ways import *

def main_hash(args: list):

    parser = argparse.ArgumentParser(prog = "diwork hash",
        description="Calculate hash of directory(s)")
    parser.add_argument("folders_paths", type=str, nargs="+",
                       help="Paths to directories whose hash will be calculated")
    parser.add_argument("--exclude", type=str, nargs="+", default=None, action="append",
                       help="Do not take these files or directories into consideration when calculating the hash")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    folders = args.folders_paths
    files_exclude = args.exclude
    if(files_exclude != None):
        files_exclude = [shit[0] for shit in files_exclude]
        check_files_exists_or_exit(files_exclude)
    err_out = []
    folders_abs = [os.path.abspath(folder_i) for folder_i in folders]
    for folder_i in folders_abs:
        if(is_folder(folder_i) == False):
            pout(f"No such directory: \"{folder_i}\"")
            exit()
        if(folders_abs.count(folder_i) > 1):
            pout(f"Directory \"{folder_i}\" occurs several ({folders_abs.count(folder_i)}) times. Exiting...")
            exit()

    dir_hashes = {}
    for folder_i in folders_abs:
        pout(f"\nCalculating hash of directory \"{folder_i}\":")
        files = getFilesList(folder_i)
        files = sorted(files)
        files = exclude_files(files, files_exclude)
        files_len = len(files)
        hashes = []
        gi = 0
        for file_i in files:
            gi+=1
            if(is_file(file_i) == False):
                err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
                continue
            hash_i = get_hash_file(file_i)
            hashes.append(hash_i)
            pout(f"({gi}/{files_len}) Hash \"{hash_i}\" have file \"{file_i}\". ")
        hashes = sorted(hashes)

        # IF CHANGE, then change make_archive_one_folder in diwork_archive.py (its legacy_version)
        hash_files = get_hash_of_hashes(hashes) 

        pout(f"\n\nHash (not considering the files hierarchy) of the directory \"{folder_i}\": \n==============================\n{hash_files}\n==============================\n")
        dir_hashes[folder_i] = hash_files


    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    col_1 = []
    col_2 = []
    for el in dir_hashes:
        col_1.append(dir_hashes[el])
        col_2.append(el)
    pout("\n\nHashes of directories: ")
    for i in range(len(col_1)):
        print(f"{col_1[i]} | {col_2[i]}")
    pout("\n=============== Done! ===============")
