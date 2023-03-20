#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import sys
import unittest

__WORK_DIR = os.path.dirname(__file__)

sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/../diwork_ways"))
sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/../diwork_mains"))
sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/.."))

from diwork_ways import pout, Global

from diwork_mains import *

from unit_tests_sup import Global4Tests


if __name__ == "__main__":

    Global4Tests.RAM = True # Need ~8 GB RAM

    from HashTest import TestModuleHash
    from CloneTest import TestModuleClone
    unittest.main()