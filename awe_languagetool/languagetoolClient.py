#!/usr/bin/env python3.10
'''
A thin, async wrapper to languagetool.

Copyright © 2022. Educational Testing Service. See license file in
this repository for details.
'''

import asyncio
import inspect
import aiohttp
import math
import sys
import json
import os
import argparse
import pandas as pd
from importlib import resources
from collections import Counter


def cleanstring(a_string):
    '''
    Make a clean string from LanguageTool codes. This has two steps:

    * Remove all non-printable characters from a string. This allows
      unicode like “你好，” “cześć,” and similar. It does not allow
      control codes, newlines, tabs, etc., and extra whitespace.
    * Convert To Title Case (Which Looks Like This Bullet)

    "  hell\no, friend\n" ==> "Hello, Friend"
    '''
    filtered_characters = list(s for s in a_string if s.isprintable())
    return ''.join(filtered_characters).title().strip()


class mappingPathError(Exception):
    pass


class languagetoolClient:

    ruleInfo = None
    categoryList = []
    subcategoryList = []
    session = None
    MAPPING_PATH = None

    # build a table mapping all non-printable characters to None
    NOPRINT_TRANS_TABLE = {
        i: None for i in range(0,
                               sys.maxunicode
                               + 1) if not chr(i).isprintable()
    }

    def __init__(self, port=8081):

        self.port = port
        self.MAPPING_PATH = \
            resources.path('awe_languagetool',
                           'languagetool_rulemapping.json')
        print(self.MAPPING_PATH)

        # The importlib.resources objects behave differently than standard paths
        # so it is necessary to adjust the code to use the resource context functions
        # rather than standard file functions.
        #if not os.path.exists(self.MAPPING_PATH):
        if not resources.is_resource('awe_languagetool',
                                               'languagetool_rulemapping.json'):
            raise mappingPathError(
                "Trying to load AWE Workbench Lexicon Module \
                 without supporting datafiles"
            )
        # Adjusting for context functions.
        #fo = open(self.MAPPING_PATH, "r")
        fo = resources.open_text('awe_languagetool', 'languagetool_rulemapping.json')
        jsonContent = fo.read()
        self.ruleInfo = json.loads(jsonContent)
        fo.close()
        for rule in self.ruleInfo:
            for subrule in self.ruleInfo[rule]:
                [cat, subcat] = self.ruleInfo[rule][subrule]
                if cleanstring(cat).title() not in self.categoryList:
                    self.categoryList.append(cleanstring(cat).title())
                subcat_name = cleanstring(cat).title() + ': ' + cleanstring(subcat).title()
                if cleanstring(subcat_name) not in self.subcategoryList:
                    self.subcategoryList.append(cleanstring(subcat_name))

        self.categoryList.sort()
        self.subcategoryList.sort()

    def make_printable(self, s):
        """Replace non-printable characters in a string."""

        # the translate method on str removes characters
        # that map to None from the string
        return s.translate(self.NOPRINT_TRANS_TABLE)

    async def check(self, language, text):
        '''
        Takes a language (e.g. `en-US`), and a text.

        Returns a JSON object of the LanguageTool spell / grammar
        check
        '''

        if text is None:
            return None

        try:
            query = {
                'language': language,
                'text': text
            }

            returnVal = None
            async with aiohttp.ClientSession() as session:
                async with session.post(f'http://localhost:{self.port}/v2/check',
                                        data=query) as response:
                    returnVal = await response.json()
            await session.close()
            return returnVal
        except Exception as e:
            print(e)
            return None

    async def processText(self, event, text):
        """
        """

        matches = []
        try:
            result = \
                await self.check('en-US', self.make_printable(text.replace('\n', '<p>')).replace('<p>', '\n'))
            for match in result['matches']:
                newmatch = match
                try:
                    if 'rule' in match:
                        if 'id' in match['rule']:
                            ruleId = match['rule']['id']
                            if ruleId in self.ruleInfo.keys():
                                if 'subId' in match['rule']:
                                    ruleSubId = match['rule']['subId']
                                    if ruleSubId is not None \
                                       and ruleSubId in self.ruleInfo[ruleId]:
                                        label = \
                                            self.ruleInfo[ruleId][ruleSubId][0]
                                        detail = \
                                            self.ruleInfo[ruleId][ruleSubId][1]
                                    else:
                                        print('ruleSubID not in \
                                              ruleInfo for ruleId '
                                              + ruleId, match)
                                elif 'nil' in self.ruleInfo[ruleId]:
                                    label = self.ruleInfo[ruleId]['nil'][0]
                                    detail = self.ruleInfo[ruleId]['nil'][1]
                                else:
                                    # ruleSubID is not defined in this path of code.
                                    if ruleSubID is not None:
                                        print('no valid match for ruleId '
                                              + ruleId + ' ' + ruleSubID)
                                    else:
                                        print('no valid match for ruleId '
                                              + ruleId)
                                newmatch['label'] = label
                                newmatch['detail'] = detail
                                matches.append(newmatch)
                            else:
                                print('ruleId not in match', match)
                        elif 'nil' in self.ruleInfo[ruleId]:
                            label = self.ruleInfo[ruleId]['nil'][0]
                            detail = self.ruleInfo[ruleId]['nil'][1]
                        else:
                            print("'id' not in match:", match)
                    else:
                        print("'rule' not in match:", match)
                except Exception as e:
                    print(match)
                    print('Error a', e)

        except Exception as e:
            print('Error b', e)
        return matches

    def wordCounts(self, text):
        for char in '-.,\n':
            text = text.replace(char, ' ')
            text = text.lower()
        word_list = text.split()
        counts = Counter(word_list).most_common()
        tokens = 0
        types = 0
        for pair in counts:
            tokens += pair[1]
            types += 1
        returnVal = {}
        returnVal['tokens'] = tokens
        returnVal['types'] = types
        returnVal['counts'] = counts
        return returnVal

    def summarizeMatches(self, text, matches):
        categories = {}
        subcategories = {}
        for item in self.categoryList:
            if cleanstring(item) not in categories:
                categories[cleanstring(item)] = int(0)
        for item in self.subcategoryList:
            if cleanstring(item) not in subcategories:
                subcategories[cleanstring(item)] = int(0)
        for item in matches:
            if cleanstring(item['label']) in categories:
                categories[cleanstring(item['label'])] += int(1)
            else:
                categories[cleanstring(item['label'])] = int(1)
            subcat = cleanstring(item['label']) \
                + ': ' + cleanstring(item['detail'])
            if subcat in subcategories:
                subcategories[subcat] += int(1)
            else:
                subcategories[subcat] = int(1)
        returnVal = {}
        returnVal['wordcounts'] = self.wordCounts(text)
        returnVal['category_counts'] = categories
        returnVal['subcategory_counts'] = subcategories
        returnVal['matches'] = matches
        return returnVal

    async def summarizeText(self, text):
        record = {}
        matches = await self.processText(record, text)
        freqInfo = self.wordCounts(text)
        returnVal = {}
        matches = self.summarizeMatches(text, matches)
        return matches

    async def summarizeMultipleTexts(self, ids, documents):

        wordcounts = {}
        category_counts = {}
        subcategory_counts = {}
        matches = {}
        category_names = []
        subcategory_names = []
        for i, doc in enumerate(documents):
            result = await self.summarizeText(doc)
            wordcounts[i] = result['wordcounts']
            category_counts[i] = result['category_counts']
            subcategory_counts[i] = result['subcategory_counts']
            matches[i] = result['matches']
            for category in category_counts[i]:
                if category not in category_names:
                    category_names.append(category)
            for subcategory in subcategory_counts[i]:
                if subcategory not in subcategory_names:
                    subcategory_names.append(subcategory)
                for match in matches[i]:
                    text = match['context']['text']
                    offset = match['context']['offset']
                    length = match['context']['length']
                    head = text[:offset]
                    mid = text[offset:offset+length]
                    tail = text[offset+length:]
            sum = wordcounts[i]['tokens']

        featnames = ['ID'] + category_names + subcategory_names
        data = []
        for i in range(0, len(documents)):
            label = ids[i]
            values = [label]
            for category in category_names:
                if category in category_counts[i]:
                    values.append(-1 *
                                  math.sqrt(category_counts[i][category]
                                            / sum))
                else:
                    values.append(0)
            for subcategory in subcategory_names:
                if subcategory in subcategory_counts[i]:
                    values.append(-1 * math.sqrt(
                                  subcategory_counts[i][subcategory] / sum))
                else:
                    values.append(0)
            data.append(values)
        return pd.DataFrame(data, columns=featnames)
