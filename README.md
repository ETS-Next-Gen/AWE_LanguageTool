# aWE_LanguageTool

Python embedding of the LanguageTool error checker, with new classification of error types. To
be required by AWE Workbench, NLP tool to support the Writing Observer project.

Note: This repository has a major hack. The full LanguageTool has been committed into version
history. This resolves a lot of issues with working in different settings (dev, deployment, etc.) and
being able to find files, but needs to be cleaned up at some point, probably with dependencies,
`pkg_resources`, or otherwise. When this happens, **we will `rebase` and rewrite `git` commit history.**
All downstream users will see `git` security warnings when this happens, and it may created additional
cleanup work for all clones/forks with unmerged changes.
