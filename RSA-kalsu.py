"""
RSA implementation using Python
Information Security 2
Team : Subin Babu & Kalyani More
"""

import copy
import random


def gen_primes(digit):
    # type: (object) -> object
    first_number = random.randint(10 ** (digit - 1), 10 ** digit)
    if first_number % 2 == 0:
        first_number += 1
    p = get_prime(first_number)

    second_number = random.randint(10 ** (digit - 1), 10 ** digit)
    if second_number % 2 == 0:
        second_number += 1
    q = get_prime(second_number)

    while p == q:
        second_number = random.randint(10 ** (digit - 1), 10 ** digit)
        if second_number % 2 == 0:
            second_number += 1
        q = get_prime(second_number)

    return p, q


def gen_key(digits):
    p, q = gen_primes(digits)

    n = p * q
    phi_of_n = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, phi_of_n)
        if is_co_prime(e, phi_of_n):
            break
    d = get_modulo_inverse(e, phi_of_n)
    return n, e, d


def is_co_prime(i, j):
    if get_gcd(i, j) != 1:
        return False
    return True


def get_gcd(a, b):
    if a < b:
        temp = b
        b = a
        a = temp
    while b != 0:
        temp = a
        a = b
        b = temp % b
    return a


def get_modulo_inverse(a, b):
    if is_co_prime(a, b):
        euclid_answer = perform_extended_euclid(a, b)
        return euclid_answer[1] % b
    else:
        return 0


def perform_extended_euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        euclid_answer = perform_extended_euclid(b % a, a)
        g = euclid_answer[0]
        y = euclid_answer[1]
        x = euclid_answer[2]
        return g, x - (b / a) * y, y


def is_composite_using_miller_rabin(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s //= 2
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
                    i += 1
                    v = (v ** 2) % num
    return True


def get_prime(x):
    while not is_composite_using_miller_rabin(x):
        x += 2
    return x


def perform_exponent_and_mod(a, d, n):
    binary_format = "{0:b}".format(d)
    s = a
    out = 1
    i = len(binary_format) - 1
    while i >= 0:
        if binary_format[i] == "1":
            out = (out * s) % n
        s = (s * s) % n
        i -= 1
    return out


def encrypt(message, mod_of_n, e, block_size):
    num_list = string2numList(message)
    num_blocks = numList2blocks(num_list, block_size)

    # perform encryption
    encrypted_message = []

    for blocks in num_blocks:
        encrypted_message.append(perform_exponent_and_mod(blocks, e, mod_of_n))

    return encrypted_message


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


def decrypt(secret, mod_of_n, d, block_size):
    # perform decryption
    num_blocks = []
    for blocks in secret:
        num_blocks.append(perform_exponent_and_mod(blocks, d, mod_of_n))

    num_list = blocks2numList(num_blocks, block_size)
    return numList2string(num_list)


if __name__ == '__main__':
    # 100 - digit key generation 
    n, e, d = gen_key(100)

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
