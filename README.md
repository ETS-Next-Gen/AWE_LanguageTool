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
1. `cd AWE_LanguageTool`
1. `pip install -e .`
1. NOTE: should this just be included in AWE Components? That's what we use to interface with the other NLP stuff

## Running

The system is ran using a client-server model.
The server runs the relevant Java command to start the `languagetool-server.jar` file.
This files comes from directly from the original Language Tool.
The client handles wrapping the output and adding in additional error classification categories.

1. Start the server

```python
from awe_languagetool import languagetoolServer
languagetoolServer.runServer()
```

This can also be ran using directly using the Java command.
Note that this command has not been fully tested with which directory it needs to be run from.
If running this does not work, see the `languagetoolServer.py` file for more information about how the system is started.
```bash
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port {port} --allow-origin "*"
```

1. Connect the client (requires another terminal)

```python
from awe_languagetool import languagetoolClient
client = languagetoolClient.languagetoolClient()
text_to_process = '...'
output = client.summarizeText(text_to_process)
# Example of output
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
