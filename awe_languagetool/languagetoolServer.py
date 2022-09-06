#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import os
from importlib import resources


def runServer(fileName=None):

    MAPPING_PATH = \
        resources.path('awe_languagetool',
                       'LanguageTool-5.5')
                       
    os.chdir(MAPPING_PATH)
    print(os.getcwd())
    os.system("java -cp languagetool-server.jar \
              org.languagetool.server.HTTPServer \
              --port 8081 --allow-origin \"*\"")


if __name__ == '__main__':
    runServer()
