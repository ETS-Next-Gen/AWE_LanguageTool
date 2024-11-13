#!/usr/bin/env python3.10
'''
This is a small helper to launch LanguageTool. It is not much more
than running the relevant Java command, and some error handling. We
have this so that LanguageTool can be installed and run as a `pip`
package, and fits into Python installation / deployment workflows.

Copyright © 2022. Educational Testing Service. See license file in
this repository for details.
'''

import argparse
import os
import subprocess
import awe_languagetool

from importlib import resources


def runServer(port=8081, config_file=None):
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

    if config_file and not os.path.isfile(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        sample_config_path = os.path.join(os.path.dirname(__file__), 'languagetool.tmp.cfg')
        print(f"Please copy the sample configuration file using `cp {sample_config_path} {config_file}`")
        raise FileNotFoundError(f"Configuration file '{config_file}' does not exist.")

    if not config_file:
        print('No configuration file set, continuing without one.')
        language_tool_command = f"java -cp {LANGUAGE_TOOL_PATH} \
            org.languagetool.server.HTTPServer \
            --port {port} --allow-origin \"*\""
    else:
        print(f'Using configuration file, {config_file}.')
        language_tool_command = f"java -cp {LANGUAGE_TOOL_PATH} \
            org.languagetool.server.HTTPServer \
            --config {config_file} --port {port} --allow-origin \"*\""

    runner = subprocess.Popen(language_tool_command, shell=True)
    if not runner:
        print("Could not start language tool!")
        raise ChildProcessError("Unable to start Language Tool. Error code: {runner}".format(runner=runner))        


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run the LanguageTool server.")
    parser.add_argument(
        '--config', type=str, default=None,
        help='Path to the configuration file for LanguageTool'
    )
    parser.add_argument(
        '--port', type=int, default=8081,
        help='Port on which to run the LanguageTool server (default: 8081)'
    )

    args = parser.parse_args()

    # Pass the arguments to runServer
    runServer(config_file=args.config, port=args.port)
