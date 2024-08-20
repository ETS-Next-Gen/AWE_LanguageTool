# --- [ Test: languagetoolServer.py ] ----------------------------------------------
# 
# Set of "sanity tests" for languagetool server. Ideally, these should be run on
# a fresh install to ensure that methods like 'path()' are working for the 
# current version of python.
# 
# Author: Caleb Scott (cwscott3@ncsu.edu)
# ----------------------------------------------------------------------------------

# --- [ IMPORTS ] ------------------------------------------------------------------

import unittest

from awe_languagetool import languagetoolServer

# --- [ CONSTS ] -------------------------------------------------------------------

# This describes the desired mapping path directory (where languagetool jar is)
EXPECTED_MAPPING_PATH = "awe_languagetool/LanguageTool5_5"

# This describes the full path to the language tool jar file
EXPECTED_LANGTOOL_PATH = "awe_languagetool/LanguageTool5_5/languagetool-server.jar"

# --- [ SETUP ] --------------------------------------------------------------------

# --- [ CLASSES ] ------------------------------------------------------------------

class LanguageToolServerTest(unittest.TestCase):

    def test_client_init(self):
        try:
            languagetoolServer.runServer()
        except FileNotFoundError as e:
            self.fail()
        except ChildProcessError as e:
            self.fail()

# --- [ END ] ----------------------------------------------------------------------