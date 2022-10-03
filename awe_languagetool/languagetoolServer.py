#!/usr/bin/env python3.10
'''
This is a small helper to launch LanguageTool. It is not much more
than running the relevant Java command, and some error handling. We
have this so that LanguageTool can be installed and run as a `pip`
package, and fits into Python installation / deployment workflows.

Copyright © 2022. Educational Testing Service. See license file in
this repository for details.
'''

import os
import awe_languagetool

from importlib import resources


def runServer(fileName=None):
    '''
    Runs the LanguageTool server, using `importlib.resources` to find the
    jar file.
    '''
    with resources.path('awe_languagetool.LanguageTool5_5',
                        'languagetool-server.jar') as LANGUAGE_TOOL_PATH:
        MAPPING_PATH = os.path.dirname(LANGUAGE_TOOL_PATH)

    try:
        os.chdir(MAPPING_PATH)
    except FileNotFoundError:
        print("Path not found starting LanguageTool: ", MAPPING_PATH)
        raise

    language_tool_command = "java -cp languagetool-server.jar \
              org.languagetool.server.HTTPServer \
              --port 8081 --allow-origin \"*\""

    runner = os.system(language_tool_command)
    if runner != 0:
        print("Could not start language tool!")
        raise ChildProcessError("Unable to start Language Tool. Error code: {runner}".format(runner=runner))        


if __name__ == '__main__':
    runServer()
