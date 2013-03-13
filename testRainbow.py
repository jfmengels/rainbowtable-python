from rainbowGenerator import *
def test(pwd):
    rain = RainbowTable()
    rain.readFromFile("D:/Coding/Python/RainbowTable/rain.txt")
    return rain.crackPassword(rain.hashWord(pwd))

def testLots(n):
    rain = RainbowTable()
    rain.readFromFile("D:/Coding/Python/RainbowTable/rain2.txt")
    count = 0
    for i in range(1, n):
        pwd = rain.randomPassword()
        hash = rain.hashWord(pwd)
        if rain.crackPassword(hash) == pwd:
            count += 1
            if i % 100 == 0:
                print('Tested', i, '/', n, ':', count, ' ', count / i * 100, '%')
    return count, count / n * 100

def testAll(res=None):
    rain = RainbowTable()
    rain.readFromFile("D:/Coding/Python/RainbowTable/rain.txt")
    if res == None:
        res = rain.allPasswords()
        print('Passwords generated')
    count = 0
    print('Starting cracking passwords')
    for i, pwd in enumerate(res):
        hash = rain.hashWord(pwd)
        if rain.crackPassword(hash) == pwd:
            count += 1
        if i % 100 == 0:
            print('Tested', i, '/', len(res), ':', count, ' ', count / len(res))
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
