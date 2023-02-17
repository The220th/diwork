# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_calc_hash(args: list):
    argc = len(args)
    if(argc != 1):
        pout("Syntax error. Expected: \"python folder_work.py hash {path_to_folder_or_file}\"")
        exit()
    folder = args[0]
    err_out = []
    folder_abs = os.path.abspath(folder)
    if(is_file(folder_abs) == True):
        pout(f"Hash of the file \"{folder_abs}\": \"{get_hash_file(folder_abs)}\"")
    elif(is_folder(folder_abs) == True):
        files = getFilesList(folder_abs)
        files = sorted(files)
        files_len = len(files)
        hashes = []
        d_4table = {}
        gi = 0
        for file_i in files:
            gi+=1
            if(is_file(file_i) == False):
                err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
                continue
            hash_i = get_hash_file(file_i)
            hashes.append(hash_i)
            d_4table[file_i] = hash_i
            pout(f"({gi}/{files_len}) Hash of \"{file_i}\" = \"{hash_i}\"")
        hashes = sorted(hashes)

        hash_files = ""
        li = 0
        for hash_i in hashes:
            hash_files += hash_i
            li-=-1
            if(li == 30):
                hash_files = get_hash_str(hash_files)
                li = 0
        hash_files = get_hash_str(hash_files)

        try:
            import tabulate
            files_4table = list(d_4table.keys())
            rows = []
            for file_i in files_4table:
                rows.append([file_i, d_4table[file_i]])
            table_str = tabulate.tabulate(rows, headers=["file_name", "hash"])
            pout(table_str)
            #write2File_str("table_out.txt", table_str)
        except:
            pout(f"Cannot import tabulate. No table. ")

        # from io import StringIO
        # o = StringIO()
        # for hash_i in hashes:
        #     o.write(hash_i)
        # hash_files = get_hash_str(o.getvalue())
        if(len(err_out) != 0):
            pout(f"\n===============\nSome troubles happened:")
            for err_i in err_out:
                pout(f"\t{err_i}")
            pout(f"===============")

        pout(f"\n\nHash (not considering the files hierarchy) of the directory \"{folder_abs}\": \n==============================\n{hash_files}\n==============================\n")

    else:
        pout(f"No such file or directory: \"{folder_abs}\"")
    
    pout("=============== Done! ===============")
