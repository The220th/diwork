# -*- coding: utf-8 -*-

import unittest

from diwork_mains import main_clone
from diwork_mains import main_hash

from diwork_ways import rm_folder_content

from unit_tests_sup import MakeRandomDir, mkdir, Global4Tests

class TestModuleClone(unittest.TestCase):
    
    def setUp(self):
        if(Global4Tests.RAM == True):
            self.dir_1 = "/tmp/tests/src"
            self.dir_2 = "/tmp/tests/dst"
        else:
            self.dir_1 = "tests/src"
            self.dir_2 = "tests/dst"
        rm_folder_content(self.dir_1, root_dir_too=True, does_not_exists_is_ok=True)
        rm_folder_content(self.dir_2, root_dir_too=True, does_not_exists_is_ok=True)

        mkdir(self.dir_1)
        mkdir(self.dir_2)

        mrd = MakeRandomDir(self.dir_1, 228) # ee831069f18640e1b057163da023ee45733eed9f162fcc988dde25e3dd0aea98
        mrd.start()
    
    def test_2(self):
        RES = False

        src_hash = main_hash([self.dir_1])[0]

        main_clone([self.dir_1, self.dir_2])

        dst_hash = main_hash([self.dir_2])[0]

        rm_folder_content(self.dir_1, root_dir_too=True)
        rm_folder_content(self.dir_2, root_dir_too=True)

        if(src_hash == dst_hash and src_hash == "ee831069f18640e1b057163da023ee45733eed9f162fcc988dde25e3dd0aea98"):
            RES = True

        self.assertEqual(RES, True)