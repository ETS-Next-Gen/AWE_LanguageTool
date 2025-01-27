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

The system uses a client-server model where the LanguageTool server processes requests, and the client adds further processing and error classification. The server runs a Java command to start `languagetool-server.jar` (provided by LanguageTool), while the client manages and interprets the server's responses.

1. Configure LanguageTool Server (optional)

    Before starting the LanguageTool server, ensure that a server configuration file exists in `awe_languagetool/LanguageTool5_5/`. We provide a sample configuration file called `languagetool.tmp.cfg`. To use it, copy and rename this file to `languagetool.cfg`. Create a copy with the following:

    ```bash
    python -m awe_languagetool.setup.copy_config
    ```

    To improve performance, particularly under high request loads, adjust the server settings in `awe_languagetool/LanguageTool5_5/languagetool.cfg`. For suggested settings, see [this forum post](https://forum.languagetool.org/t/too-many-parallel-requests/8290/3) on server configurations. For a full list of configuration options, refer to the [LanguageTool server code](https://github.com/languagetool-org/languagetool/blob/c6321ab5837a9e1ae5501d746f947f5706b4b274/languagetool-server/src/main/java/org/languagetool/server/HTTPServerConfig.java).

1. Start the server with either

    You can start the server in Python or from the command line.

    **In Python:**

    ```python
    from awe_languagetool import languagetoolServer
    languagetoolServer.runServer()
    # or with a config file
    languagetoolServer.runServer(config_file='/path/to/config')
    ```

    **In Bash:**

    ```bash
    python -m awe_languagetool.languagetoolServer
    // or with a config file
    python -m awe_languagetool.languagetoolServer --config /path/to/config
    ```

    **Directly using Java (if necessary):**

    The server can also be run directly with Java, which may require adjusting the `.jar` file path based on your working directory. For more details, see `languagetoolServer.py`.

    ```bash
    java -cp awe_languagetool/LanguageTool5_5/languagetool-server.jar org.languagetool.server.HTTPServer --config {/path/to/config} --port {port} --allow-origin "*"
    ```

1. Connect the client

    In a separate terminal, you can now connect the LanguageTool client to the running server. The languagetoolClient class accepts `host` and `port` parameters, defaulting to `localhost` and `8081`. Alternatively, you can use the `server_url` parameter, which will override `host` and `port`.

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
