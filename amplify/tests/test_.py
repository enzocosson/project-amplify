import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest 

def test_userhandler():
    from amplify.userhandler import UserHandler
    assert 1 == 1