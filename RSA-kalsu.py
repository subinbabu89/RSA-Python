import itertools
import argparse
import copy
import math
import pickle
import random
from itertools import combinations

def primeSieve(k):
    """return a list with length k + 1, showing if list[i] == 1, i is a prime
    else if list[i] == 0, i is a composite, if list[i] == -1, not defined"""
    listofPrime = []

    def isPrime(n):
        """return True is given number n is absolutely prime,
        return False is otherwise."""
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    result = [-1] * (k + 1)
    for i in range(2, int(k + 1)):
        if isPrime(i):
            listofPrime.append(i)
            result[i] = 1
        else:
            result[i] = 0
    return listofPrime

def genPrimes(digit):
    firstNumber = random.randint(10**(digit-1),10**(digit))
    if(firstNumber%2 ==0):
        firstNumber += 1
    p = getPrime(firstNumber)

    secondNumber = random.randint(10 ** (digit - 1), 10 ** (digit))
    if (secondNumber % 2 == 0):
        secondNumber += 1
    q = getPrime(secondNumber)

    while (p ==q):
        secondNumber = random.randint(10 ** (digit - 1), 10 ** (digit))
        if (secondNumber % 2 == 0):
            secondNumber += 1
        q = getPrime(secondNumber)

    return p,q


def genKey(digits):
    p,q = genPrimes(digits)

    n = p * q
    phiN = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, phiN)
        if coPrime(e, phiN):
            break
    d = moduloInverse(e, phiN)
    return n,e,d


def coPrime(i, j):
    if getGCD(i, j) != 1:
        return False
    return True


def getGCD(a, b):
    if a < b:
        temp = b
        b = a
        a = temp
    while b != 0:
        temp = a
        a = b
        b = temp % b
    return a


def moduloInverse(a, b):
    if coPrime(a, b):
        euclidAnswer = extendedEuclid(a, b)
        return euclidAnswer[1] % b
    else:
        return 0


def extendedEuclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        euclidAnswer = extendedEuclid(b % a, a)
        g = euclidAnswer[0]
        y = euclidAnswer[1]
        x = euclidAnswer[2]
        return g, x - (b / a) * y, y

def rabinMiller(num):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def getPrime(x):
    while (not rabinMiller(x)):
        x +=2
    return x;

def modExp(a, d, n):
    binnary = "{0:b}".format(d)
    s = a
    out = 1
    i = len(binnary)-1
    while(i>=0):
        if(binnary[i]=="1"):
            out = (out * s ) % n
        s = (s * s) % n
        i -= 1
    return out

def encrypt(message, modN, e, blockSize):
    numList = string2numList(message)
    numBlocks = numList2blocks(numList, blockSize)

    encryptedMessage = []

    for blocks in numBlocks:
        encryptedMessage.append(modExp(blocks, e, modN))

    return encryptedMessage

def string2numList(strn):
    """Converts a string to a list of integers based on ASCII values"""
    # Note that ASCII printable characters range is 0x20 - 0x7E
    return [ord(chars) for chars in strn]


def numList2string(l):
    """Converts a list of integers to a string based on ASCII values"""
    # Note that ASCII printable characters range is 0x20 - 0x7E
    return ''.join(map(chr, l))


def numList2blocks(l, n):
    """Take a list of integers(each between 0 and 127), and combines them
    into block size n using base 256. If len(L) % n != 0, use some random
    junk to fill L to make it."""
    # Note that ASCII printable characters range is 0x20 - 0x7E
    returnList = []
    toProcess = copy.copy(l)
    if len(toProcess) % n != 0:
        for i in range(0, n - len(toProcess) % n):
            toProcess.append(random.randint(32, 126))
    for i in range(0, len(toProcess), n):
        block = 0
        for j in range(0, n):
            block += toProcess[i + j] << (8 * (n - j - 1))
        returnList.append(block)
    return returnList


def blocks2numList(blocks, n):
    toProcess = copy.copy(blocks)
    returnList = []
    for numBlock in toProcess:
        inner = []
        for i in range(0, n):
            inner.append(numBlock % 256)
            numBlock >>= 8
        inner.reverse()
        returnList.extend(inner)
    return returnList

def decrypt(secret, modN, d, blockSize):
    numBlocks = []
    for blocks in secret:
        numBlocks.append(modExp(blocks, d, modN))

    numList = blocks2numList(numBlocks, blockSize)
    return numList2string(numList)

if __name__ == '__main__':
    n, e, d = genKey(100)
    print ('n = {0}'.format(n))
    print ('e = {0}'.format(e))
    print ('d = {0}'.format(d))
    message = """
        We were the Leopards, the Lions, those who'll take our place will be
        little jackals, hyenas; But we'll go on thinking ourselves the salt of
        the earth.
    """
    print(message)
    cipher = encrypt(message, n, e, 15)
    print(cipher)
    deciphered = decrypt(cipher, n, d, 15)
    print(deciphered)