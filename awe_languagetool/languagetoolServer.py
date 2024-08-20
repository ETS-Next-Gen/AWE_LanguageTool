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
import subprocess
import awe_languagetool

from importlib import resources


def runServer(fileName=None, port=8081, config_file="languagetool.cfg"):
    '''
    Runs the LanguageTool server, using `importlib.resources` to find the
    jar file.
    '''
    # NOTE: after playing with python3.9, it does not like the 'package.sub' string.
    # So, I added multiple 'joinpaths'; this worked for both 3.9 and 3.11
    with resources.as_file(
            resources.files('awe_languagetool').joinpath('LanguageTool5_5').joinpath('languagetool-server.jar')
        ) as LANGUAGE_TOOL_PATH:
        print("Setting Language Path:",  LANGUAGE_TOOL_PATH)
        MAPPING_PATH = os.path.dirname(LANGUAGE_TOOL_PATH)

    try:
        os.chdir(MAPPING_PATH)
        print("Changed Dir to {}".format(MAPPING_PATH))
    except FileNotFoundError:
        print("Path not found starting LanguageTool: ", MAPPING_PATH)
        raise

    if not config_file:
        language_tool_command = f"java -cp languagetool-server.jar \
            org.languagetool.server.HTTPServer \
            --port {port} --allow-origin \"*\""
    else:
        language_tool_command = f"java -cp languagetool-server.jar \
            org.languagetool.server.HTTPServer \
            --config {config_file} --port {port} --allow-origin \"*\""

    runner = subprocess.Popen(language_tool_command, shell=True)
    if not runner:
        print("Could not start language tool!")
        raise ChildProcessError("Unable to start Language Tool. Error code: {runner}".format(runner=runner))        


if __name__ == '__main__':
    runServer()
