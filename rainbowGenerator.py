lettersLower = 'abcdefghijklmnopqrstuvwxyz'
lettersUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = "0123456789"
allChars = lettersLower + lettersUpper + numbers
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

from hashlib import md5
def hashWord(word, func=md5):
    word = word.encode('utf-8')
    return func(word).hexdigest()

def reduce(hashV, column, chars, pwdLength):
    results = []
    # Cast hash from str to int then decompose into bytes
    #nbBytes = len(hashV) // 2
    #byteArray = [h % 256 for int(hashV, 16) in range(nbBytes)]
    byteArray = getBytes(hashV)
    for i in range(pwdLength):
        index = byteArray[(i + column) % len(byteArray)]
        newChar = chars[index % len(chars)]
        results.append(newChar)
    return "".join(results)

def getBytes(hashV):
	results = []
	remaining = int(hashV, 16)
	while remaining > 0:
		results.append(remaining % 256)
		remaining //= 256
	return results


def createChain(startPwd, columns, chars, pwdLength, func):
    pwd = startPwd
    for col in range(columns):
        hashV = hashWord(pwd, func)
        pwd = reduce(hashV, col, chars, pwdLength)
    return startPwd, hashV

def randomPassword(chars, pwdLength):
    from random import randrange
    pwd = ""
    charsLength = len(chars)
    for i in range(pwdLength):
        pwd += chars[randrange(charsLength)]
    return pwd

class RainbowTable:
    from hashlib import sha1, md5
    hashFunctions = {sha1.__name__ : sha1,
                     md5.__name__ : md5}
        
    def __init__(self, columns=0, chars="", pwdLength=0, func=None):
        self.table = []
        if columns > 0:
            self.columns = columns
            self.chars = chars
            self.pwdLength = pwdLength
            self.func = func
            for i in range((len(chars)**pwdLength + 1) // columns):
                pwd = randomPassword(chars, pwdLength)
                self.table.append(createChain(pwd, columns, chars, pwdLength, func))

    def writeToFile(self, output):
        f = open(output, 'w')
        data = [self.columns, self.chars, self.pwdLength, self.func.__name__]
        data = [str(x) for x in data]
        f.write(" ".join(data))
        for entry in self.table:
            f.write("\n")
            f.write(" ".join(entry))
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
            line = line.strip().split(sep=" ", maxsplit=1)
            self.table.append(line)
            line = f.readline()
        f.close()

def createTable(columns, chars, pwdLength, func):
    return RainbowTable(columns, chars, pwdLength, func)



def findPassword(hashV, tableFile):
    # Not yet implemented
    pass
