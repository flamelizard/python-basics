"""
    Plenty of space for improvement
    http://blog.amjith.com/fuzzyfinder-in-10-lines-of-python

    Very basic, worthy addition
    - rate match and order matched text accordingly
"""

def match_fuzzy(seq, words, color=False):
    """"
    Simple (own) fuzzy logic where search strings has to
    occur in word in a proper sequence (from left to right)
    """
    res = []
    for word in words:
        if is_match_fuzzy(seq, word):
            res.append(word)
    if color:
        res = [color_match(seq, word) for word in res]
    return res

def is_match_fuzzy(seq, word):
    # print '[fuzzy]', word, len(word)
    i = 0
    cnt = 0
    word = word.lower()
    seq = seq.lower()
    for s in seq:
        while(i < len(word)):
            is_match = True if s == word[i] else False
            i += 1
            if is_match:
                cnt += 1
                break
    if cnt == len(seq):
        return True
    return False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color_match(seq, word):
    """Color matched chars using ANSI escape seq

    Color code does not work in Windows CMD, only bold seems to work

    Unfortunately, escape codes increase string lenght in the terminal
    and auto completed command has some embdedded spaces
    """
    _word = [w for w in word]
    i = -1
    cnt = 0
    for s in seq:
        i = word.find(s, i+1)
        # print '[i]', i, word
        _word[i] = '{}{}{}'.format(bcolors.BOLD, word[i], bcolors.ENDC)
    return ''.join(_word)



