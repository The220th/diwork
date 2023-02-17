# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_exec(args: list):
    argc = len(args)
    IN_REP = "{in}"
    OUT_REP = "{out}"
    if(argc != 3):
        pout("Syntax error. Expected: \"python folder_work.py exec {folder_in} {folder_out} {command}\", where: ")
        pout("\t{command} like this \"convert {in} {out}\", where: ")
        pout("\t\t{in} each files from {folder_in} ")
        pout("\t\t{out} all files from {folder_out} ")
        pout("\t{folder_out} must be empty. {folder_out} can be empty string \"\"")
        pout("\n\tFor exampe, convert all jpg-pictures from \"path/to/jpg/image/folder\" to png-image:")
        pout("\t> python folder_work.py exec \"path/to/jpg/image/folder\" \"path/to/png/image/folder\" \"convert {in} {out}.png\"")
        exit()
    folder_in = args[0]
    folder_out = args[1]
    command = args[2]
    err_out = []
    if(is_folder(folder_in) == False):
        pout(f"\"{folder_in}\" is not folder. ")
        exit()
    folder_in_abs = os.path.abspath(folder_in)
    if(folder_out != "" and is_folder(folder_out) == False):
        pout(f"\"{folder_out}\" is not folder. ")
        exit()
    if(folder_out == ""):
        if OUT_REP in command:
            pout(f"{OUT_REP} in {command} finded, but folder_out is empty string. Exitting")
            exit()
    else:
        folder_out_abs = os.path.abspath(folder_out)


    if(folder_out != "" and is_folder_empty(folder_out_abs) == False):
        pout(f"Folder \"{folder_out_abs}\" is not empty. ")
        pout(f"===============\n\t All files in \"{folder_out_abs}\" will be removed before exec. \n===============")
        pout("Continue? Type \"yes\" in capital letter if continue \n> ", endl=False)
        user_in = input()
        if(user_in.strip() != "YES"):
            pout("Exitting")
            exit()
        rm_folder_content(folder_out_abs)
        if(is_folder_empty(folder_out_abs) == True):
            pout(f"All files from folder \"{folder_out_abs}\" removed. This folder is empty now. Clonning...")
        else:
            pout(f"Cannot clean folder \"{folder_out_abs}\"! Exiting ")

    if(folder_out != ""):
        dirs_abs_in = getDirsList(folder_in_abs)
        dirs_abs_in = sorted(dirs_abs_in)
        for dir_in_i in dirs_abs_in:
            dir_in_i_rel = rel_path(dir_in_i, folder_in_abs)
            dir_out_i_abs = os.path.join(folder_out_abs, dir_in_i_rel)
            exe_out = exe(f"mkdir -p \"{dir_out_i_abs}\"")
            if(exe_out[1] != ""):
                pout(f"ERROR: {exe_out[1]}")
                exit()

    files_abs_in = getFilesList(folder_in_abs)
    files_abs_in = sorted(files_abs_in)
    gi, N = 0, len(files_abs_in)
    for file_in_i in files_abs_in:
        gi+=1
        if(is_file(file_in_i) == False):
            err_out.append(f"\"{file_in_i}\" is not file or does not exists, it will be skipped. ")
            continue
        
        command_i = command.replace(IN_REP, file_in_i)
        if(folder_out != ""):
            file_i_rel = rel_path(file_in_i, folder_in_abs)
            file_out_i = os.path.join(folder_out_abs, file_i_rel)
            command_i = command_i.replace(OUT_REP, file_out_i)
        pout(f"({gi}/{N}) Executing... ")
        exe_out = exe(command_i)
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
