import sys
import unittest

import pytest
import os
import json


# each test runs on cwd to its temp dir
@pytest.fixture
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield


class AbstractTest(unittest.TestCase):
    def body(self, json_file: str, folder="tests/resources") -> dict:
        filename = os.path.join(os.path.realpath(folder), json_file)
        with open(filename, "r") as read_file:
            return json.load(read_file)
