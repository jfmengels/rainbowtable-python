from rainbowGenerator import *
def test(pwd):
    rain = RainbowTable()
    rain.readFromFile("D:/Coding/Python/RainbowTable/rain.txt")
    return rain.crackPassword(rain.hashWord(pwd))

def testLots():
    rain = RainbowTable()
    rain.readFromFile("D:/Coding/Python/RainbowTable/rain.txt")
    i = 0
    found = False
    while not found:
        i+=1
        pwd = rain.randomPassword()
        hash = rain.hashWord(pwd)
        if rain.crackPassword(hash) == pwd:
            found = True
            print(pwd, hash)
        elif i % 100 == 0:
            print(i)
    return i

def testAll(res=None):
    rain = RainbowTable()
    rain.readFromFile("D:/Coding/Python/RainbowTable/rain.txt")
    if res == None:
        res = allPasswords(rain.chars, rain.pwdLength)
    count = 0
    for pwd in res:
        hash = rain.hashWord(pwd)
        if rain.crackPassword(hash) == pwd:
            count += 1
    return count, count / len(res)
    

def testCollision(chars, pwdLength, func=md5):
    table = MockTable(chars, pwdLength, func)
    allPwd = table.allPasswords(table)
    hashes = []
    count = 0
    for pwd in allPwd:
        h = table.hashWord(table, pwd)
        if h in hashes:
            count += 1
    hashes.append(h)
    return count


class MockTable:
    def __init__(self, chars, pwdLength, func):
        self.chars = chars
        self.pwdLength = pwdLength
        self.func = func
        self.allPasswords = RainbowTable.allPasswords
        self.hashWord = RainbowTable.hashWord
