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
import time

from awe_languagetool import languagetoolClient
from awe_languagetool.languagetoolClient import mappingPathError

# --- [ CONSTS ] -------------------------------------------------------------------

# This describes the desired mapping path pointing to a rulemapping.json file
EXPECTED_RULEMAP_PATH = "awe_languagetool/languagetool_rulemapping.json"

LION_TEXT = "test_texts/lion.txt"

# --- [ SETUP ] --------------------------------------------------------------------

# Make sure you are running the server before running client tests.
# NOTE: you must ensure that the java server is not already running; otherwise,
# this setup step will fail saying that the port is already in use.

# languagetoolServer.runServer()

# --- [ CLASSES ] ------------------------------------------------------------------

class LanguageToolClientTest(unittest.TestCase):

    def test_client_init(self):
        """
        Basic test to see if the client properly aligns its paths 
        for files in its package.
        """
        try:
            new_client = languagetoolClient.languagetoolClient()
            self.assertTrue(new_client.MAPPING_PATH.endswith(EXPECTED_RULEMAP_PATH))
        except mappingPathError as e:
            self.fail()

    def test_client_timing_java(self):
        """
        Attempt to start up a client, and pass in a sample text.
        We are measuring runtime of how well the server responds to a single request.

        Precondition: ltServer is running.
        """
        try:
            new_client = languagetoolClient.languagetoolClient()
            with open(LION_TEXT, 'r') as text_file:

                # Grab the text
                sample_text = text_file.read()

                # Start timing benchmark
                start = time.process_time()
                output = new_client.summarizeText(sample_text)
                end = time.process_time()

                # Show results
                print("---------[ TIMING BENCHMARK ]---------")
                print(f"Time Elapsed: {end - start}")
                print("--------------------------------------")
        except mappingPathError as e:
            self.fail()

# --- [ END ] ----------------------------------------------------------------------