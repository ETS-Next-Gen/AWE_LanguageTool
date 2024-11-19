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

from importlib import resources

def find_config_file(filename):
    '''Confirm that the configuration file, if not None, exists
    on the filesystem.
    '''
    if filename and not os.path.isfile(filename):
        sample_config_path = os.path.join(os.path.dirname(__file__), 'languagetool.tmp.cfg')
        error_message = f"Error: Configuration file '{filename}' not found.\n"\
            f"Please copy the sample configuration file using `cp {sample_config_path} {filename}`"
        raise FileNotFoundError(error_message)
    if not filename:
        print('No configuration file set, continuing without one.')
    else:
        print(f'Using configuration file, {filename}.')


def runServer(port=8081, config_file=None):
    '''
    Runs the LanguageTool server, using `importlib.resources` to find the
    jar file.
    '''
    with resources.as_file(
            resources.files('awe_languagetool').joinpath('LanguageTool5_5').joinpath('languagetool-server.jar')
        ) as LANGUAGE_TOOL_PATH:
        print("Setting LanguageTool path to", LANGUAGE_TOOL_PATH)

    find_config_file(config_file)
    config_file_param = f'--config {config_file}' if config_file else ''

    language_tool_command = f"java -cp {LANGUAGE_TOOL_PATH} \
        org.languagetool.server.HTTPServer \
        {config_file_param} --port {port} --allow-origin \"*\""

    runner = subprocess.Popen(language_tool_command, shell=True)
    if not runner:
        raise ChildProcessError("Unable to start Language Tool. Error code: {runner}".format(runner=runner))        


def setup_and_parse_args():
    '''Handle setting up and parsing arguments
    '''
    parser = argparse.ArgumentParser(description="Run the LanguageTool server.")
    parser.add_argument(
        '--config', type=str, default=None,
        help='Path to the configuration file for LanguageTool'
    )
    parser.add_argument(
        '--port', type=int, default=8081,
        help='Port on which to run the LanguageTool server (default: 8081)'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = setup_and_parse_args()

    runServer(config_file=args.config, port=args.port)
