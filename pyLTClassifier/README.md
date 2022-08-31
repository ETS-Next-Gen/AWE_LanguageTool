Note that the installation of LanguageTool 5.5 included in this 
directory has been modified to work with AWE Workbench.

In particular, org/languagetool/rules/en/grammar.xml has been 
modified to activate some rules not activated by default and by
the editing of some old rules and addition of some new rules
to make it work better in conjunction with the category system
built into this installation. 

A copy of this grammar.xml is included in this directory.
If you update to a newer version of LanguageTool, use it to
replace the original grammar.xml under org/languagetool/rules/en/

Note that to develop versions of AWE Workbench for another language,
you will need to develop a comparable adaptation of that language's
grammar.xml file.