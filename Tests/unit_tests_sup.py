# -*- coding: utf-8 -*-

import random
import os

from diwork_ways import mkdir

def get_rnd_str(n: int = 10, r: "Random" = None) -> str:
    if(r == None):
        r = random.Random()
    alphas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    S = ''.join(r.choices(alphas, k=n))
    return S



class Global4Tests():
    RAM=False

class MakeRandomDir():

    def __init__(self, root_path: str, seed: int = None, max_files_count: int = None, max_size: int = None, file_prob: float = None, dir_prob: float = None):
        
        if(os.path.isdir(root_path) != True):
            raise AttributeError(f"\"{root_path}\" not directory. ")

        if(seed == None):
            seed = random.randint(-1027, 3036)
        self.r = random.Random(seed)
        if(max_files_count == None):
            max_files_count = self.r.randint(5, 500)
        if(file_prob == None):
            file_prob = self.r.random()
        if(dir_prob == None):
            dir_prob = self.r.random()
        if(max_size == None):
            max_size = self.r.randint(5000, 1024*1024*30)
        
        self.N = max_files_count
        self.curN = 0
        self.root = root_path
        self.p = file_prob
        self.dp = dir_prob
        self.max_size = max_size

        self.ONCE = False

    def start(self):
        if(self.ONCE == True):
            raise RuntimeError("This class only one time can be start!")
        
        cur_dir = self.root
        while(self.curN < self.N):
            r_i = self.r.random()
            if(r_i < self.p):
                create_random_file(os.path.join(cur_dir, get_rnd_str(self.r.randint(5, 15), self.r)), 
                                                self.r.randint(5, self.max_size), None, self.r)
                self.curN-=-1
            else:
                r_i = self.r.random()
                if(r_i < self.dp):
                    new_dir = os.path.join(cur_dir, get_rnd_str(self.r.randint(5, 15), self.r))
                    mkdir(new_dir)
                    self.__next_node(new_dir)
                
        
        self.ONCE == True

    def __next_node(self, cur_path: str):
        cur_dir = cur_path
        while(self.curN < self.N):
            r_i = self.r.random()
            if(r_i < self.p):
                create_random_file(os.path.join(cur_dir, get_rnd_str(self.r.randint(5, 15), self.r)), 
                                                self.r.randint(5, self.max_size), None, self.r)
                self.curN-=-1
            else:
                r_i = self.r.random()
                if(r_i < self.dp):
                    new_dir = os.path.join(cur_dir, get_rnd_str(self.r.randint(5, 15), self.r))
                    mkdir(new_dir)
                    self.__next_node(new_dir)
                else:
                    return



def create_random_file(path: str, bytes_count: int = 1027, seed: int = None, r: "Random" = None):
    if(seed != None and r != None):
        raise Exception("Cannot seed != None and r != None")
    if(seed == None):
        seed = random.randint(-1027, 3036)
    if(r == None):
        r = random.Random(seed)
    with open(path, 'wb') as fd:
        fd.write(r.randbytes(bytes_count))
        fd.flush()
