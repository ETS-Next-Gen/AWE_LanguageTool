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
import asyncio
import time

from awe_languagetool import languagetoolClient
from awe_languagetool.languagetoolClient import mappingPathError

# --- [ CONSTS ] -------------------------------------------------------------------

# This describes the desired mapping path pointing to a rulemapping.json file
EXPECTED_RULEMAP_PATH = "awe_languagetool/languagetool_rulemapping.json"

TEXT_BASE = "test_texts/"
LION_TEXT = TEXT_BASE + "lion.txt"

CENSORSHIP_TEXTS = [
    "censorship1.txt",
    "censorship2.txt",
    "censorship3.txt",
    "censorship4.txt",
    "censorship5.txt",
    "censorship6.txt",
    "censorship7.txt",
    "censorship8.txt",
    "censorship9.txt",
    "censorship10.txt",
    "censorship11.txt",
    "censorship12.txt",
    "censorship13.txt",
    "censorship14.txt",
    "censorship15.txt",
    "censorship16.txt",
    "censorship17.txt",
    "censorship18.txt",
    "censorship19.txt",
    "censorship20.txt",
    "censorship21.txt",
    "censorship22.txt",
    "censorship23.txt",
    "censorship24.txt",
    "censorship25.txt"
]

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
            self.assertTrue(
                new_client.MAPPING_PATH.endswith(EXPECTED_RULEMAP_PATH)
            )
        except mappingPathError as e:
            self.fail()

    def test_client_timing_java_single(self):
        """
        Attempt to start up a client, and pass in a sample text.
        We are measuring runtime of how well the server responds to a 
        single request.

        Precondition: languagetoolServer is running.
        """
        try:
            client = languagetoolClient.languagetoolClient()
            with open(LION_TEXT, 'r') as text_file:

                # Grab the text
                sample_text = text_file.read()

                # Start timing benchmark
                start = time.time()
                output = asyncio.run(client.summarizeText(sample_text))
                end = time.time()

                # Show results
                print()
                print("---------[ TIMING BENCHMARK ]---------")
                print(f"Time Elapsed: {end - start}")
                print("--------------------------------------")
        except mappingPathError as e:
            self.fail()

    def test_client_timing_java_multiple_sequential(self):
        """
        Attempt to start up a client, and pass in a sample text.
        We are measuring runtime of how well the server responds to
        many sequential requests.

        Precondition: languagetoolServer is running.
        """
        try:
            client = languagetoolClient.languagetoolClient()

            # Pre-load all texts
            all_texts = {}
            index = 0
            for text_filename in CENSORSHIP_TEXTS:
                with open(TEXT_BASE + text_filename) as censorship_file:
                    all_texts[index] = censorship_file.read()
                    index = index + 1

            # Make multiple requests
            start = time.time()
            output = asyncio.run(
                client.summarizeMultipleTexts(
                    list(all_texts.keys()), 
                    list(all_texts.values())
                )
            )
            end = time.time()

            # Show results
            print()
            print("---------[ TIMING BENCHMARK ]---------")
            print(f"Time Elapsed: {end - start}")
            print("--------------------------------------")

        except mappingPathError as e:
            self.fail()

# --- [ END ] ----------------------------------------------------------------------