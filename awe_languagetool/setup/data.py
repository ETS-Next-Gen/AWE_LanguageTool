#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import argparse

from distutils.command.build import build
from distutils.command.build import build as _build
from distutils.command.install import install
from distutils.command.install import install as _install

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.develop import develop as _develop

from importlib import resources

import os
from pathlib import Path

import zipfile
from clint.textui import progress
import requests
from distutils.sysconfig import get_python_lib
import shutil
import sysconfig

import nltk
from nltk.corpus import wordnet
from spacy.cli.download import download


def extra_build_commands(develop=False, install=False):

    cwd = os.path.dirname(__file__)
    cwd_true = os.getcwd()

    if develop:

        #################################################################
        # Copy the data files needed to run our version of languagetool #
        # and extract our category system for languagetool errors.      #
        #                                                               #
        # We have a copy of this tarball in source control, but I leave #
        # this code in place so that we can in future easily upgrade to #
        # a new version of LT. It's hard to make sure that LT is in-    #
        # stalled correctly in any environment w/o this hard-copy       #
        # approach.                                                     #
        #################################################################

        # Since python 3.11, we cannot use 'path', but this:
        with resources.as_file(resources.files('awe_languagetool')) as path:
            dir_name = str(path)

        extension = ".zip"
        os.makedirs(dir_name, exist_ok=True)

        print('Downloading LanguageTool tarball')
        fname = 'LanguageTool-5.5.zip'
        url = 'https://languagetool.org/download/' + fname
        r = requests.get(url, stream=True)
        with open(fname, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                      expected_size=(total_length
                                                     / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()

        print('Extracting LanguageTool tarball to', dir_name)
        for item in os.listdir(os.getcwd()):
            # loop through items in dir

            if item.endswith(extension):
                # check for ".zip" extension

                file_name = os.path.abspath(item)
                # get full path of files

                zip_ref = zipfile.ZipFile(file_name)
                # create zipfile object

                zip_ref.extractall(dir_name)
                # extract file to dir

                zip_ref.close()
                # close file

                os.remove(file_name)
                # delete zipped file
                
        print('Copying additional LanguageTool datafiles')

        grammarfile = \
            os.path.join(cwd, '../grammar.xml')
        engrammarfile = \
            os.path.join(cwd, '../grammar_en_us.xml')

        grammardest = \
            os.path.join(dir_name,
                         'LanguageTool-5.5/org/languagetool/rules/en/grammar.xml')
        engrammardest = \
            os.path.join(dir_name,
                         'LanguageTool-5.5/org/languagetool/rules/en/en-US/grammar.xml')

        shutil.copy2(grammarfile, grammardest)
        shutil.copy2(engrammarfile, engrammardest)

        shutil.move(os.path.join(dir_name,'LanguageTool-5.5'),os.path.join(dir_name,'LanguageTool5_5'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run AWE \
                                     Workbench data download')
    parser.add_argument("-d",
                        "--develop",
                        help="Runs the data downloads to the development \
                              rather than the build location.",
                        action="store_true")
    parser.add_argument("-i",
                        "--install",
                        help="Runs the data downloads to the development \
                              rather than the build location.",
                        action="store_true")

    args = parser.parse_args()

    extra_build_commands(develop=args.develop,
                         install=args.install)

