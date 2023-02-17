# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import hashlib

class Global():
    outfile = None
    hash_mode = 0 # 0 is sha256sum, 1 is hashlib.sha256, 2 is sha512sum
    


def getFilesList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in files]

def getDirsList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in subdirs]

# return False, if folder_path not exists or folder_path is not folder
def is_folder(folder_path: str) -> bool:
    return os.path.isdir(folder_path)

# return False, if file_path not exists or file_path is not file
def is_file(file_path: str) -> bool:
    return os.path.isfile(file_path)

# return False, if file_path not exists
def is_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def is_folder_empty(folder_path: str) -> bool:
    if(len(os.listdir(folder_path)) == 0):
        return True
    else:
        return False

def rel_path(file_path: str, folder_path: str) -> str:
    return os.path.relpath(file_path, folder_path)

def rm_folder_content(folder_path: str):
    """Удаляет всё содержимое папки. Саму папку не трогает"""
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_i in files:
            os.remove(os.path.join(root, file_i))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    # os.rmdir(folder_path)

def pout(msg : str, endl = True):
    if(endl == False):
        pout_low(msg)
    else:
        pout_low(msg + "\n")

def pout_low(msg: str):
    print(msg)
    if(Global.outfile != None):
        with open(Global.outfile, "a", encoding="utf-8") as fd:
            fd.write(msg)
            fd.flush()

def write2File_str(fileName : str, s : str) -> None:
    with open(fileName, 'w', encoding="utf-8") as temp:
        temp.write(s)
        temp.flush()

def get_hash_file(file_path: str) -> str:
    if(Global.hash_mode == 1):
        buff_BLOCKSIZE = 65536 # 64 kB
        sha = hashlib.sha256()
        with open(file_path, "rb") as temp:
            file_buffer = temp.read(buff_BLOCKSIZE)
            while len(file_buffer) > 0:
                sha.update(file_buffer)
                file_buffer = temp.read(buff_BLOCKSIZE)
    else:
        if(Global.hash_mode == 0):
            shaxxxsum = "sha256sum"
        elif(Global.hash_mode == 2):
            shaxxxsum = "sha512sum"
        exe_res = exe(f"{shaxxxsum} \"{file_path}\"")
        if(exe_res[1] != ""):
            pout(f"Error with {shaxxxsum}: ")
            pout(f"\"{exe_res[1]}\"")
            exit()
        res = exe_res[0]
        return res[:res.find(" ")]

def get_hash_str(s: str):
    if(Global.hash_mode == 1):
        return hashlib.sha256( s.encode("utf-8") ).hexdigest()
    else:
        exe_res = exe(f"sha512sum", stdin_msg=s)
        if(exe_res[1] != ""):
            pout(f"Error with sha512sum: ")
            pout(f"\"{exe_res[1]}\"")
            exit()
        res = exe_res[0]
        return res[:res.find(" ")]

def exe_lowout(command: str, debug: bool = True, std_out_pipe: bool = False, std_err_pipe: bool = False) -> tuple:
    '''
    Аргумент command - команда для выполнения в терминале. Например: "ls -lai ."
    Возвращает кортеж, где элементы:
        0 - строка stdout or None if std_out_pipe == False
        1 - строка stderr or None if std_err_pipe == False
        2 - returncode
    '''
    if(debug):
        pout(f"> {command}")
    
    if(std_out_pipe == True):
        if(std_err_pipe == True):
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # https://stackoverflow.com/questions/1180606/using-subprocess-popen-for-process-with-large-output
            out = process.stdout.read().decode("utf-8")
            err = process.stderr.read().decode("utf-8")
        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            out = process.stdout.read().decode("utf-8")
            err = None
    else:
        if(std_err_pipe == True):
            process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
            out = None
            err = process.stderr.read().decode("utf-8")
        else:
            process = subprocess.Popen(command, shell=True)
            out = None
            err = None
    errcode = process.returncode
    return (out, err, errcode)

def exe(command: str, debug: bool = True, std_out_fd = subprocess.PIPE, std_err_fd = subprocess.PIPE, stdin_msg: str = None) -> tuple:
    '''
    Аргумент command - команда для выполнения в терминале. Например: "ls -lai ."
    if(std_out_fd or std_err_fd) == subprocess.DEVNULL   |=>    No output enywhere
    if(std_out_fd or std_err_fd) == subprocess.PIPE      |=>    All output to return
    if(std_out_fd or std_err_fd) == open(path, "w")      |=>    All output to file path
    Возвращает кортеж, где элементы:
        0 - строка stdout
        1 - строка stderr
        2 - returncode
    '''
    _ENCODING = "utf-8"

    if(debug):
        #pout(f"> " + " ".join(command))
        if(stdin_msg != None):
            pout(f"> {command}, with stdin=\"{stdin_msg}\"")
        else:
            pout(f"> {command}")

    #proc = subprocess.run(command, shell=True, capture_output=True, input=stdin_msg.encode("utf-8"))
    if(stdin_msg == None):
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd)
    else:
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd, input=stdin_msg.encode("utf-8"))
    
    #return (proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"))
    return (proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"), proc.returncode)