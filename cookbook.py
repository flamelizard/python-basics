"""Collection of recipes and best practices from any domain"""


def shift_to_range(v, r):
    try:
        # +1 for range 1 <= x <= r
        return (v % r) + 1
    except TypeError:
        return None

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
