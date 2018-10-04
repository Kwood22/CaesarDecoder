#!/usr/bin/python3
import sys
import os,os.path
from spellchecker import SpellChecker


class DictionaryChecker:
    def __init__(self):
        self.dict = SpellChecker()

    def check(self , word):
        wordl = word.lower()
        result = self.dict.known([wordl])
        if (len(result)>0):
            return True
        else:
            return False

    def getNumRealWords (self, wordlist):
        wordlistl = [x.lower() for x in wordlist]
        return len(self.dict.known(wordlistl))
    