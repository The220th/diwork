# -*- coding: utf-8 -*-

import os
import unittest

from diwork_mains import main_hash

from diwork_ways import rm_folder_content

from unit_tests_sup import MakeRandomDir, mkdir, Global4Tests

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
        

