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


def runServer(fileName=None, port=8081):
    '''
    Runs the LanguageTool server, using `importlib.resources` to find the
    jar file.
    '''
    # In order for python 3.9 to work we have to make a slight hack to the
    # language tools module in order to ensure that this works.  To do that
    # we first import the tool and then set the origin explicitly.  
    #
    # This cheap hack does just that by using the submodule_search_location
    # value which *does* seem to be set by default to supply the location
    # for origin.  Having done that we can then go about the rest of it
    # without error.
    import platform
    if (platform.python_version()[0:3] == "3.9"):
        import awe_languagetool.LanguageTool5_5
        LTSpec = awe_languagetool.LanguageTool5_5.__spec__
        LTSpec.origin = LTSpec.submodule_search_locations[0]

    with resources.path('awe_languagetool.LanguageTool5_5',
                        'languagetool-server.jar') as LANGUAGE_TOOL_PATH:
        print("Setting Language Path:",  LANGUAGE_TOOL_PATH)
        MAPPING_PATH = os.path.dirname(LANGUAGE_TOOL_PATH)

        
    try:
        os.chdir(MAPPING_PATH + "/LanguageTool5_5")
        print("Changed Dir to {}".format(MAPPING_PATH))
        # os.chdir(MAPPING_PATH)
    except FileNotFoundError:
        print("Path not found starting LanguageTool: ", MAPPING_PATH)
        raise

    language_tool_command = f"java -cp languagetool-server.jar \
              org.languagetool.server.HTTPServer \
              --port {port} --allow-origin \"*\""

    runner = subprocess.Popen(language_tool_command, shell=True)
    if not runner:
        print("Could not start language tool!")
        raise ChildProcessError("Unable to start Language Tool. Error code: {runner}".format(runner=runner))        


if __name__ == '__main__':
    runServer()
