# -*- coding: utf-8 -*-

import os
import unittest

from diwork_mains import main_hash

from diwork_ways import rm_folder_content

from unit_tests_sup import MakeRandomDir, mkdir, Global4Tests, create_random_file

class TestModuleHash(unittest.TestCase):
    
    def setUp(self):
        if(Global4Tests.RAM == True):
            self.dir_1 = "/tmp/tests/1"
            self.dir_2 = "/tmp/tests/2"
        else:
            self.dir_1 = "tests/1"
            self.dir_2 = "tests/2"
        rm_folder_content(self.dir_1, root_dir_too=True, does_not_exists_is_ok=True)
        rm_folder_content(self.dir_2, root_dir_too=True, does_not_exists_is_ok=True)

    def test_1(self):
        RES = False
        mkdir(self.dir_1)
        mkdir(self.dir_2)

        MakeRandomDir(self.dir_1, 228).start() # ee831069f18640e1b057163da023ee45733eed9f162fcc988dde25e3dd0aea98
        MakeRandomDir(self.dir_2, 330).start() # 82f3075937a75d918324dc4713860701420011c886ccfca7b3974e99ed6c2a2d

        hashes = main_hash([self.dir_1, self.dir_2])
        print(hashes)
        
        if(hashes[0] == "ee831069f18640e1b057163da023ee45733eed9f162fcc988dde25e3dd0aea98" 
        and hashes[1] == "82f3075937a75d918324dc4713860701420011c886ccfca7b3974e99ed6c2a2d"):
            RES = True

        rm_folder_content(self.dir_1, root_dir_too=True)
        rm_folder_content(self.dir_2, root_dir_too=True)

        self.assertEqual(RES, True)

    def test_2(self):
        RES = False
        mkdir(self.dir_1)
        mkdir(self.dir_2)

        MakeRandomDir(self.dir_1, 330).start() # 82f3075937a75d918324dc4713860701420011c886ccfca7b3974e99ed6c2a2d
        MakeRandomDir(self.dir_2, 330).start() # 82f3075937a75d918324dc4713860701420011c886ccfca7b3974e99ed6c2a2d

        hashes_1 = main_hash([self.dir_1, self.dir_2])
        print(hashes_1)

        hashes_2 = main_hash([self.dir_1, self.dir_2, "--hierarchy"])
        print(hashes_2)

        mkdir(os.path.join(self.dir_1, "keko/"))
        mkdir(os.path.join(self.dir_2, "keko/"))
        mkdir(os.path.join(self.dir_2, "keko/kbl"))
        create_random_file(os.path.join(self.dir_2, "keko/file.txt"), 228, 6719)

        hashes_3 = main_hash([self.dir_1, self.dir_2, "--hierarchy"])
        print(hashes_1)
        print(hashes_2)
        print(hashes_3)

        if(hashes_1[0] == "82f3075937a75d918324dc4713860701420011c886ccfca7b3974e99ed6c2a2d" 
        and hashes_1[1] == "82f3075937a75d918324dc4713860701420011c886ccfca7b3974e99ed6c2a2d"
        and hashes_2[0] == "4d36582d78db3073b6d5411dbd62e4d98acf0eb00f9fc8c3634a0b1dc0552b8c"
        and hashes_2[1] == "4d36582d78db3073b6d5411dbd62e4d98acf0eb00f9fc8c3634a0b1dc0552b8c"
        and hashes_3[0] == "e7d655da91698b4570e3ac110e31b4f0505516d112c1c70773d03ae5c44581bf"
        and hashes_3[1] == "97d029cb75a5b2701540ac2b545a8f17f7e65ac4f0b2329027b42760fbfc0112"):
            RES = True

        rm_folder_content(self.dir_1, root_dir_too=True)
        rm_folder_content(self.dir_2, root_dir_too=True)

        self.assertEqual(RES, True)

