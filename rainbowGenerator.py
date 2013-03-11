lettersLower = 'abcdefghijklmnopqrstuvwxyz'
lettersUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = "0123456789"
allChars = lettersLower + lettersUpper + numbers
words = ['kat', 'vsz', 'rev', 'kax', 'map', 'yjd']

from hashlib import md5, sha1
def generatePasswords(nbChar, chars=lettersLower):
    results = []
    nbDifferentChars = len(chars)
    for i in range(nbDifferentChars**nbChar):
        word = ""
        for j in range(nbChar):
            word = chars[i % nbDifferentChars] + word
            i //= nbDifferentChars
        results.append(word)
    return results


class RainbowTable:
    hashFunctions = {sha1.__name__ : sha1,
                     md5.__name__ : md5}
    
    def __init__(self, columns=0, chars="", pwdLength=0, func=None, rows=1000):
        from RB import RBTree, rbnode
        self.table = RBTree()
        if columns > 0:
            self.columns = columns
            self.chars = chars
            self.pwdLength = pwdLength
            self.func = func
            #for i in range((len(chars)**pwdLength + 1) // columns):
            for i in range(rows):
                pwd = self.randomPassword()
                hashV = self.createChain(pwd)
                self.table.insert(hashV, pwd)

    def __repr__(self):
        return repr(self.table._root)

    def writeToFile(self, output):
        f = open(output, 'w')
        data = [self.columns, self.chars, self.pwdLength, self.func.__name__]
        data = [str(x) for x in data]
        f.write(" ".join(data))
        f.write("\n")
        f.write(repr(self))
        #for entry in self.table:
            #f.write("\n")
            #f.write(" ".join(entry))
        f.close()

    def readFromFile(self, input):
        f = open(input, "r")
        line = f.readline()
        line = line.strip().split(sep=" ", maxsplit=3)
        self.columns, self.chars, self.pwdLength, self.func = line
        self.columns = int(self.columns)
        self.pwdLength = int(self.pwdLength)
        self.func = RainbowTable.hashFunctions[self.func]
        line = f.readline()
        while line != '':
            pwd, hashV = line.strip().split(sep=" ", maxsplit=1)
            self.table.insert(hashV, pwd)
            line = f.readline()
        f.close()

    def getAllKeys(self, input):
        keys = []
        f = open(input, "r")
        line = f.readline()
        line = line.strip().split(sep=" ", maxsplit=3)

    def _find(self, hashV):
        return self.table.search(hashV)

    def hashWord(self, word):
        word = word.encode('utf-8')
        return self.func(word).hexdigest()

    def reduce(self, hashV, column):
        results = []
        # Cast hash from str to int then decompose into bytes
        byteArray = self.getBytes(hashV)
        for i in range(self.pwdLength):
            index = byteArray[(i + column) % len(byteArray)]
            newChar = self.chars[index % len(self.chars)]
            results.append(newChar)
        return "".join(results)

    def getBytes(self, hashV):
            results = []
            remaining = int(hashV, 16)
            while remaining > 0:
                    results.append(remaining % 256)
                    remaining //= 256
            return results
        
    def createChain(self, pwd):
        for col in range(self.columns):
            hashV = self.hashWord(pwd)
            pwd = self.reduce(hashV, col)
        return hashV

    def randomPassword(self):
        from random import randrange
        pwd = ""
        charsLength = len(self.chars)
        for i in range(self.pwdLength):
            pwd += self.chars[randrange(charsLength)]
        return pwd


    def crackPassword(self, startHash):
        resPwd = None
        for col in range(self.columns, -1, -1):
            hashV = self._getFinalHash(startHash, col)
            pwdList = self._find(hashV)
            for pwd in pwdList:
                if pwd != None:
                    resPwd = self._findHashInChain(pwd, startHash)
                    if resPwd != None:
                        return resPwd
        return None

    def _getFinalHash(self, startHash, startCol):
        hashV = startHash
        for col in range(startCol, self.columns-1):
            pwd = self.reduce(hashV, col)
            hashV = self.hashWord(pwd)
        return hashV

    def _findHashInChain(self, startPwd, startHash):
        hashV = self.hashWord(startPwd)
        col = 0
        while col < self.columns:
            pwd = self.reduce(hashV, col)
            hashV = self.hashWord(pwd)
            #print(startHash, hashV, pwd)
            if hashV == startHash:
                return pwd
            col += 1
        return None

    def allPasswords(self):
        """Returns the list of all password this table could and should cover.
TEST Function
"""
        res = []
        length = len(self.chars)
        for i in range(length**self.pwdLength):
            pwd = ""
            for j in range(self.pwdLength):
                pwd += self.chars[i % length]
                i //= length
            res.append(pwd)
        return res

    def testWord(self, word):
        return self.crackPassword(self.hashWord(word))

    def testWords(self, words=words):
        for word in words:
            print(word, self.crackPassword(rain.hashWord(word)))
    
from testRainbow import *

#rain = RainbowTable(100, lettersLower, 3, md5)
rain = RainbowTable() ; rain.readFromFile("D:/Coding/Python/RainbowTable/rain.txt")

