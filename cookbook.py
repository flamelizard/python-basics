"""Collection of recipes and best practices from any domain"""

"""Operations on sequence"""
def shift_to_range(v, r):
    try:
        # +1 for range 1 <= x <= r
        return (v % r) + 1
    except TypeError:
        return None

"""Circular shift aka bitwise rotation

Simple pattern how to shift either from 1st to last position or the other way
around. Each loop shifts all numbers by one. When loops equals to tuple size,
it will be in original order.

Learnt in Think Java, when comparing card ranks.
"""

def circular_shift(nums, loops=1, leftwise=True):
    """
    :loops number of circular shift runs on the sequence
    :leftwise preset shift direction
    """
    if loops == 0:
        return nums
    res = []
    for num in nums:
        _num = (num+1) if leftwise else (num-1)
        res.append(_num % len(nums))
    print "[circular]", res
    return circular_shift(res, loops-1, leftwise)

# nums = [0, 1, 2, 3]
# circular_shift(nums)
# circular_shift(nums, 4, False)

"""Sorting and algorithms"""

def better_sort():
    """Sort list of tuples based on user-defined key function"""
    lst = [('user', 2), ('admin', 5), ('director', 3), ('intern', 1)]
    lst.sort(key=lambda rec: rec[1])
    print lst
# better_sort()

def is_sorted(seq, asc=True):
    """
    :return boolean
    :asc sort direction, default ascending

    empty list returns True
    """
    if asc:
        return all([seq[i] <= seq[i+1] for i in xrange(len(seq) - 1)])
    else:
        return all([seq[i] >= seq[i+1] for i in xrange(len(seq) - 1)])

def _bisect_recur(seq, item):
    """Bisect algorithm

    Bisect is an algorithm with order of growth O(long n), base 2. This is much
    better than linear growth since the cost of operation constant for higher
    n - just like logarithmic curve.

    Bisect algorithm is simple. It works only for sorted sequence though.
    Bisect will divide seq and will find out to which half the target value
    belong. It will continue until it locates position where to put target in
    order to keep seq sorted.

    In general, bisect module returns index where the item should go to. Index
    can be passed to lst.insert() or use directly bisect method.

    Bisect left and right differs only in situation when target item is in the
    seq already. Left will return the position of existing item, right will
    return index after existing item.

    Bisect (left, right) will return following for border cases:
    - 0 for item under low border
    - len(seq-1) for item above high border

    I've implemented bisect manually below in kind of my own way :-)

    Note
     - sequence must be sorted in ascending manner
    """
    print '[bisect_recur]', seq
    size = len(seq)
    # if item > seq[size-1]:
    #     return None

    if size == 1:
        return seq[0]

    new_seq = seq[:size/2] if item <= seq[size/2] else seq[size/2:]
    return _bisect_recur(new_seq, item)

def b(seq, item):
    """Like bisect right

    More accurate implementation of bisect behaviour

    :return index for insertion of item to seq so it remains sorted
    """
    # handle values off range
    if item < seq[0]:
        return 0
    elif item > seq[-1]:
        return len(seq)-1
    return _b(seq, item)

def _b(seq, item, idx=0):
    """Bisect worker recursive func"""
    size = len(seq)
    if size == 1:
        return idx+1

    if item >= seq[size/2]:
        new_seq = seq[size/2:]
        idx += len(seq[:size/2])
    else:
        new_seq = seq[:size/2]
    return _b(new_seq, item, idx)

def test_bisect():
    """
    interesting are border cases for values under first value and above last
    val - no difference in behaviour of left and right bisect
    """
    seq = [1, 2, 3]
    test_val = [0.5, 1.5, 2, 2.5, 5]
    print '[test bisect]', seq
    for val in test_val:
        # print '{:-10s}'.format('left')
        print '[left] for %s' % val, bisect.bisect_left(seq, val)
        print '[right] for %s' % val, bisect.bisect_right(seq, val)
        print '-' * 10
# test_bisect()

"""String operations"""

def format_text(text):
    print '{0:{fill}{align}{len}}'.format(text, fill='_', align='>', len=10)
# format_text('bob')

def split_list(lst, step):
    """Split list into sub-lists

    :step lenght of sublist
    """
    sub_lst = []
    return [lst[i:i+step] for i in xrange(0, len(lst)-1, step)]
# print split_list(lst, 8)

# Simple cache implemented through class decorator and dict
# Boost fibonnaci perf tremendously
class memoize:
    """Cache func results in dict"""
    def __init__(self, func):
        self.mem = {}
        self.func = func

    def __call__(self, n):
        try:
            return self.mem[n]
        except KeyError:
            self.mem[n] = self.func(n)
            return self.mem[n]

"""Caching"""

@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def fib_seq(n):
    seq = [ ]
    if n > 0:
        seq.extend(fib_seq(n-1))
    seq.append((fib(n), 'n={}'.format(n)))
    return seq
# cProfile.run('print fib_seq(10)')

"""Inspector"""

def print_attrib(o):
    """Print nicely formattted object attributes, name <-> value"""
    lst = []
    for attr in dir(o):
        try:
            val = str(getattr(o, attr))
            lst.append((attr, val))
        except AttributeError:
            pass
    for attr, val in lst:
        print '%s -> %s' % (attr, val)
