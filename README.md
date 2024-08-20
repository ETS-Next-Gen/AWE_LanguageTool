# AWE_LanguageTool

Python embedding of the LanguageTool error checker, with new classification of error types. To
be required by AWE Workbench, NLP tool to support the Writing Observer project.

## Note about repository

This repository has a major hack. The full LanguageTool has been committed into version
history. This resolves a lot of issues with working in different settings (dev, deployment, etc.) and
being able to find files, but needs to be cleaned up at some point, probably with dependencies,
`pkg_resources`, or otherwise. When this happens, **we will `rebase` and rewrite `git` commit history.**
All downstream users will see `git` security warnings when this happens, and it may created additional
cleanup work for all clones/forks with unmerged changes.

## Installation

1. Clone repo from Github
2. `cd AWE_LanguageTool`
3. `pip install -e .`

## LanguageTool Configuration & Running

The system is run using a client-server model. The server runs the relevant Java command to start the `languagetool-server.jar` file (which comes from LanaguageTool). The client handles wrapping the output and adding in additional error classification categories.

Before running LanguageTool, *you must first copy/write a server config file into* `awe_languagetool/LanguageTool5_5/`. We've provided a sample config file called `languagetool.tmp.cfg`. If you copy this file, you must rename it to `languagetool.cfg`.

By default, LT runs pretty slow with too many incoming requests; you can modify the server settings for LT in `awe_languagetool/LanguageTool5_5/languagetool.cfg`. See [this forum post](https://forum.languagetool.org/t/too-many-parallel-requests/8290/3) on a decent server config file. For a full description of all server config options, see [LT5.5 Source Code](https://github.com/languagetool-org/languagetool/blob/c6321ab5837a9e1ae5501d746f947f5706b4b274/languagetool-server/src/main/java/org/languagetool/server/HTTPServerConfig.java).

With the python LT wrapper, this can be run from anywhere in the project. However, if you decide to run the java command directly (see below), this needs to be run within the `awe_languagetool/LanguageTool5_5/` directory.

1. Start the server

```python
from awe_languagetool import languagetoolServer
languagetoolServer.runServer()
```

This can also be ran using directly using the Java command.
Note that this command has not been fully tested with which directory it needs to be run from.
If running this does not work, see the `languagetoolServer.py` file for more information about how the system is started.

```bash
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --config languagetool.cfg --port {port} --allow-origin "*"
```

1. Connect the client (requires another terminal)

```python
from awe_languagetool import languagetoolClient
import asyncio

client = languagetoolClient.languagetoolClient()
text_to_process = '...'
output = asyncio.run(client.summarizeText(text_to_process))
# Example output
# {
#     'wordcounts': {
#         'tokens': 0,
#         'types': 0,
#         'counts': [('word', 0), ...]
#     },
#     'category_counts': {
#         'Capitalization': 0,
#         'Grammar': 0,
#         ...
#     },
#     'subcategory_counts': {
#         'Capitalization: Abbreviations': 0,
#         'Capitalization: Acronyms': 0,
#         ...,
#         'Grammar: Article Error': 0,
#         ...,
#     },
#     'matches': [
#         {
#             'message': 'Possible spelling mistake found.',
#             'shortMessage': 'Spelling mistake',
#             'replacements': [{'value': 'new_word'}, ...],
#             'offset': 0,
#             'length': 0,
#             'context': {
#                 'text': '...',
#                 'offset': 0,
#                 'length': 0,
#             },
#             'sentences': 'Sentence where spelling error occured.',
#             'type': {'typeName': 'Other'},
#             'rule': {
#                 'id': 'MORFOLOGIK_RULE_EN_US',
#                 'description': 'Possible spelling mistake',
#                 'issueType': 'misspelling',
#                 'category': {'id': 'TYPOS', 'name': 'Possible Typo'}
#             },
#             'ignoreForIncompleteSentences': False,
#             'contextForSureMatch': 0,
#             'label': 'Spelling',
#             'detail': 'Unknown word'
#         },
#         ...
#     ]
# }
```
