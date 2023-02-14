#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import pickle
import base64
import math
import time
import os
import sys
import pandas as pd
import pandas.testing as pd_testing
import random
import threading
import unittest
from multiprocessing import Process, Queue

import awe_languagetool.languagetoolServer
from awe_languagetool.languagetoolClient import languagetoolClient


def startServers():
    queue = Queue()
    p1 = Process(target=awe_languagetool.languagetoolServer.runServer, args=())
    p1.start()

    time.sleep(60)
    return p1


def initialize():
    """
    Initialize
    """
    lt = languagetoolClient()

    # Initialize the parser
    parser.set_uri("ws://localhost:8766")

    # return spellchecker and parser objects
    return  lt

labels = ['GRE_Sample_Essay_1', 'GRE_Sample_Essay_2', 'Aesop']
texts = ["The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands fropython force script to exitm emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination.", "In recent centuries, humans have developed the technology very rapidly, and you may accept some merit of it, and you may see a distortion in society occured by it. To be lazy for human in some meaning is one of the fashion issues in thesedays. There are many symptoms and resons of it. However, I can not agree with the statement that the technology make humans to be reluctant to thinkng thoroughly.\n\nOf course, you can see the phenomena of human laziness along with developed technology in some place. However, they would happen in specific condition, not general. What makes human to be laze of thinking is not merely technology, but the the tendency of human that they treat them as a magic stick and a black box. Not understanding the aims and theory of them couses the disapproval problems.\n\nThe most important thing to use the thechnology, regardless the new or old, is to comprehend the fundamental idea of them, and to adapt suit tech to tasks in need. Even if you recognize a method as a all-mighty and it is extremely over-spec to your needs, you can not see the result you want. In this procedure, humans have to consider as long as possible to acquire adequate functions. Therefore, humans can not escape from using their brain.\n\nIn addition, the technology as it is do not vain automatically, the is created by humans. Thus, the more developed tech and the more you want a convenient life, the more you think and emmit your creativity to breakthrough some banal method sarcastically.\n\nConsequently, if you are not passive to the new tech, but offensive to it, you would not lose your ability to think deeply. Furthermore, you may improve the ability by adopting it.", "A lion lay asleep in the forest, his great head resting on his paws. A timid little mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the lion's nose. Roused from his nap, the lion laid his huge paw angrily on the tiny creature to kill her.\n\n\"Spare me!\" begged the poor mouse. \"Please let me go and some day I will surely repay you.\"\n\nThe lion was much amused to think that a mouse could ever help him. But he was generous and finally let the mouse go.\n\nSome days later, while stalking his prey in the forest, the lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The mouse knew the voice and quickly found the lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the lion was free.\n\n\"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion.\""]

class ServerAPITest(unittest.TestCase):

    p1 = None
    lt = None

    @classmethod
    def setUpClass(self):
        self.p1  = startServers()
       self.lt = initialize()

    @classmethod
    def tearDownClass(self):
        self.p1.terminate()
        self.p1 = None
        self.lt = None

    def testLTMatch(self):
        record = None
        matches = self.lt.processText(record, texts[1])

    def testLTSummary(self):
        df1 = self.lt.summarizeMultipleTexts(labels, texts)
        df1.set_index('ID', inplace=True)
        print(df1)

