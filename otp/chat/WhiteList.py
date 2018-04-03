# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.chat.WhiteList
import os
import string
import sys
from bisect import bisect_left


class WhiteList:
    __module__ = __name__

    def __init__(self, wordlist):
        self.words = []
        for line in wordlist:
            self.words.append(line.strip('\n\r').lower())

        self.words.sort()
        self.numWords = len(self.words)

    def cleanText(self, text):
        text = text.strip('.,?!')
        text = text.lower()
        return text

    def isWord(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        if i == self.numWords:
            return False
        return self.words[i] == text

    def isPrefix(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        if i == self.numWords:
            return False
        return self.words[i].startswith(text)

    def prefixCount(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        j = i
        while j < self.numWords and self.words[j].startswith(text):
            j += 1

        return j - i

    def prefixList(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        j = i
        while j < self.numWords and self.words[j].startswith(text):
            j += 1

        return self.words[i:j]
# okay decompiling .\otp\chat\WhiteList.pyc
