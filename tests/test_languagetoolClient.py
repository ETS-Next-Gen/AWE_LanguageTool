# --- [ Test: languagetoolClient.py ] ----------------------------------------------
# 
# Set of "sanity tests" for languagetool client. Ideally, these should be run on
# a fresh install to ensure that methods like 'path()' are working for the 
# current version of python.
# 
# Author: Caleb Scott (cwscott3@ncsu.edu)
# ----------------------------------------------------------------------------------

# --- [ IMPORTS ] ------------------------------------------------------------------

import unittest

from awe_languagetool import languagetoolClient
from awe_languagetool.languagetoolClient import mappingPathError

# --- [ CONSTS ] -------------------------------------------------------------------

# This describes the desired mapping path pointing to a rulemapping.json file
EXPECTED_RULEMAP_PATH = "awe_languagetool/languagetool_rulemapping.json"

# --- [ SETUP ] --------------------------------------------------------------------

# Make sure you are running the server before running client tests.
# NOTE: you must ensure that the java server is not already running; otherwise,
# this setup step will fail saying that the port is already in use.

# languagetoolServer.runServer()

# --- [ CLASSES ] ------------------------------------------------------------------

class LanguageToolClientTest(unittest.TestCase):

    def test_client_init(self):
        try:
            new_client = languagetoolClient.languagetoolClient()
            self.assertTrue(new_client.MAPPING_PATH.endswith(EXPECTED_RULEMAP_PATH))
        except mappingPathError as e:
            self.fail()

# --- [ END ] ----------------------------------------------------------------------