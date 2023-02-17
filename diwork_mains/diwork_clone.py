# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_clone(args: list):
    argc = len(args)
    if(argc != 2):
        pout("Syntax error. Expected: \"python folder_work.py clone {folder_src} {folder_dest}\"")
        exit()
    folder1 = args[0]
    folder2 = args[1]
    err_out = []
    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)
    if(is_folder(folder1_abs) == False):
        pout(f"\"{folder1_abs}\" is not folder. ")
        exit()
    if(is_folder(folder2_abs) == False):
        pout(f"\"{folder2_abs}\" is not folder. ")
        exit()
    
    if(folder1_abs in folder2_abs):
        pout(f"Directory \"{folder1_abs}\" contains directory \"{folder2_abs}\". Exiting...")
        exit()
    if(folder2_abs in folder1_abs):
        pout(f"Directory \"{folder2_abs}\" contains directory \"{folder1_abs}\". Exiting...")
        exit()
    
    if(is_folder_empty(folder2_abs) == False):
        pout(f"Folder \"{folder2_abs}\" is not empty. ")
        pout(f"===============\n\t All files in \"{folder2_abs}\" will be removed before clonning. \n===============")
        pout("Continue? Type \"yes\" in capital letter if continue \n> ", endl=False)
        user_in = input()
        if(user_in.strip() != "YES"):
            pout("Exitting")
            exit()
        rm_folder_content(folder2_abs)
        if(is_folder_empty(folder2_abs) == True):
            pout(f"All files from folder \"{folder2_abs}\" removed. This folder is empty now. Clonning...")
        else:
            pout(f"Cannot clean folder \"{folder2_abs}\"! Exiting ")

    dirs_abs_1 = getDirsList(folder1_abs)
    dirs_abs_1 = sorted(dirs_abs_1)
    for dir_i_1 in dirs_abs_1:
        dir_i_rel = rel_path(dir_i_1, folder1_abs)
        dir_i_2 = os.path.join(folder2_abs, dir_i_rel)
        exe_out = exe(f"mkdir -p \"{dir_i_2}\"")
        if(exe_out[1] != ""):
            pout(f"ERROR: {exe_out[1]}")
            exit()

    files_abs_1 = getFilesList(folder1_abs)
    files_abs_1 = sorted(files_abs_1)
    gi, N = 0, len(files_abs_1)
    for file_i_1 in files_abs_1:
        gi+=1
        if(is_file(file_i_1) == False):
            err_out.append(f"\"{file_i_1}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_rel = rel_path(file_i_1, folder1_abs)
        file_i_2 = os.path.join(folder2_abs, file_i_rel)
        # In windows cp=copy
        pout(f"({gi}/{N}) Copying \"{file_i_rel}\"... ")
        exe_out = exe(f"cp \"{file_i_1}\" \"{file_i_2}\"")
        if(exe_out[1] != ""):
            err_out.append(f"ERROR: {exe_out[1]}")
            continue
    exe("sync")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")