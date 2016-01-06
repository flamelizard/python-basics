"""Collection of various tools, utils and helper funcs"""

import timeit
from functools import wraps
import random

"""Profile code"""

def _timethis(func):
    @wraps(func)
    def wrapper(*args):
        print '[timethis]', timeit.timeit(lambda: func(*args), number=100)
        return func(*args)
    return wrapper

def timethis(repeat=100):
    def decor(func):
        @wraps(func)
        def wrapper(*args):
            print '[timethis]', timeit.timeit(lambda: func(*args),
                                              number=repeat)
            return func(*args)
        return wrapper
    return decor

"""Test data generators"""

def generate_random_numbers(size, k):
    """
    .sample generates k-lenght list of numbers, k has to be <= size
    .seed without arg will see based on system time
    """
    random.seed()
    return random.sample(xrange(size), k)
# print generate_random_numbers(100, 30)

"""Algorithms"""

def bubble_sort(vals):
    """Faster bubble sort"""
    size = len(vals)-1
    while True:
        for i in range(size):
            if vals[i] > vals[i+1]:
                vals[i], vals[i+1] = vals[i+1], vals[i]
        size -= 1
        if size <= 1:
            break
    return vals

def simple_bubble_sort(lst):
    """Simple sorting algorithm

    For each iteration, it compares adjacent items and swaps their position
    if the latter item is smaller.

    For each iteration, the current biggest value bubble up to the very right
    and can be locked in (not compared anymore).

    The algorithm is very basic and thus very slow and useless.
    """
    for j in range(len(lst)-1):
        for i in range(len(lst)):
            try:
                if lst[i] > lst[i+1]:
                    lst[i], lst[i+1] = lst[i+1], lst[i]
            except IndexError:
                pass
        # print lst
    return lst

# lst = generate_random_numbers(100, 40)
# print simple_bubble_sort(lst)
# print bubble_sort2(lst)

def dump_to_file(filepath, txt, mode='a+'):
    try:
        with open(filepath, mode) as fp:
            fp.write(txt)
    except IOError:
        print 'File %s not found' % filepath
