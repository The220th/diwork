# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil

from diwork_ways import *

from tqdm import tqdm


def calc_hash_dict_of_dir(dir_path: str) -> dict:
    d = {}
    dir_path = os.path.abspath(dir_path)
    files = getFilesList(dir_path)
    files = sorted(files)
    for file_i in tqdm(files):
        file_i_rel = os.path.relpath(file_i, dir_path)
        d[file_i_rel] = get_hash_file(file_i)
    return d


def main_diffclone(args: list):
    parser = argparse.ArgumentParser(prog = "diwork diffclone",
        description="This module will clone all the contents of {folder_src} to {folder_dest}, but only files, which does not already contains in {folder_dest}."
                    "Old files will be renamed if needed.")
    parser.add_argument("folder_src", type=str, nargs=1,
                       help="Path to source directory")
    parser.add_argument("folder_dest", type=str, nargs=1,
                       help="Path to destination directory")
    # TODO: symlinks
    # parser.add_argument("--symlink_mode", type=int, choices=[0, 1, 2], default=2, required=False,
    #                    help="What to do with links: 0 - ignor, 1 - consider link content, 2 - use the file where the link refers to. Default 2.")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    folder1 = args.folder_src[0]
    folder2 = args.folder_dest[0]
    err_out = []
    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)
    if not is_folder(folder1_abs):
        pout(f"\"{folder1_abs}\" is not folder. ")
        exit()
    if not is_folder(folder2_abs):
        pout(f"\"{folder2_abs}\" is not folder. ")
        exit()

    if folder1_abs in folder2_abs:
        pout(f"Directory \"{folder1_abs}\" contains directory \"{folder2_abs}\". Exiting...")
        input("Enter to continue...")
    if folder2_abs in folder1_abs:
        pout(f"Directory \"{folder2_abs}\" contains directory \"{folder1_abs}\". Exiting...")
        input("Enter to continue...")

    pout(f"Calculating hash tree of directory \"{folder1_abs}\"...")
    d1 = calc_hash_dict_of_dir(folder1_abs)

    pout("Diffclonning...")
    # 3 варианта:
    # 1. Такого файла не существует в folder2, тогда просто копируем
    # 2. Такой файл существует в folder2 и hash совпадает, тогда ничего не делаем
    # 3. Такой файл существует в folder2 и hash не совпадает, тогда старый переименовываем, а новый копируем

    dirs_abs_1 = getDirsList(folder1_abs)
    dirs_abs_1 = sorted(dirs_abs_1)
    for dir_i_1 in dirs_abs_1:
        dir_i_rel = rel_path(dir_i_1, folder1_abs)
        dir_i_2 = os.path.join(folder2_abs, dir_i_rel)
        if not os.path.exists(dir_i_2):
            mkdir(dir_i_2, p=True)

    files1, files2 = getFilesList(folder1_abs), getFilesList(folder2_abs)
    for file1_i in tqdm(files1):
        try:
            file1_i_rel = str(os.path.relpath(file1_i, folder1_abs))
            file2_i = os.path.join(folder2_abs, file1_i_rel)
            if not os.path.isfile(file2_i):  # case 1
                shutil.copy(file1_i, file2_i)
                os.sync()
            else:
                file2_i_hash = get_hash_file(file2_i)
                if d1[file1_i_rel] == file2_i_hash:  # case 2
                    pass  # ничего не делаем
                else:  # case 3
                    file2_i_time = get_time_file(file2_i)
                    os.rename(file2_i, f"{file2_i}---{file2_i_time}.bak")
                    shutil.copy(file1_i, file2_i)
                    os.sync()
        except Exception as e:
            pout(str(e))
            err_out.append(f"\"{file1_i}\"")

    if len(err_out) != 0:
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")