"""
findIt
Help to show where and how is used an expression in question
Often needs to see real-world example to understand how the command is used or
just to see best practices.

search custom folders
custom folders defined ?
specify script type
do not count uniteresting pieces of code such as import

search line by line

print line matching pattern, print context, file name and line number

show live results

threading for high perf - profile
"""

import os
from fnmatch import fnmatch
# from Lumpy import Lumpy
import threading
import functools
import time
import re
import sys

class Null(object):
    def write(self, *args):
        pass
# sys.stdout = Null()

def get_files(root, exts):
    found = []
    for d, _, files in os.walk(root):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext in exts:
                found.append(os.path.join(d, f))
    return found

# def search_file(f, exp):
#     lines = []
#     with open(f) as fp:
#         for line in fp:
#             if line.find(exp) != -1:
#                 lines.append(line.strip('\n'))
#     return lines

def search_file(f, exp):
    lines = []
    with open(f) as fp:
        for line in fp:
            if re.search(exp, line):
                lines.append(line.strip('\n'))
    return lines

def collect_live_res(feeds):
    for f, lines in feeds:
        print 'in %s' % f
        for line in lines:
            print '>> %s' % line
        print


exp = 'threading'
root = 'd:/'
suff = ['.py']

found = get_files(root, suff)
# print found

regex = re.compile(exp, re.IGNORECASE)
search_file = functools.partial(search_file, exp=regex)

# line_match = []
# for f in found:
#     lines = search_file(f)
#     if lines:
#         line_match.append((f, lines))

# collect_live_res(line_match)


from threading import Thread
from Queue import Queue, Empty

q = Queue()
f_size = 100
search_res = []
safeprint = threading._allocate_lock()
# signal to daemon thread to stop execution, unecessary
_sentinel = object()
nthreads = 3

file_chunks = [found[i:i+f_size] for i in xrange(0, len(found)-1, f_size)]

def tr_print(msg, mute=True):
    """Print on thread - no text overlap"""
    if mute:
        return
    with safeprint:
        print msg

def producer(files, q):
    line_match = []
    for f in files:
        lines = search_file(f)
        if lines:
            line_match.append((f, lines))
    tr_print('[prod] %s' % line_match)
    if line_match:
        q.put(line_match)

def consumer(q):
    while True:
        try:
            item = q.get(timeout=2.0)
        except Empty:
            continue
        q.task_done()
        if item is _sentinel:
            print '[consumer] quit signal received'
            q.put(item)
            break
        tr_print('[consume] %s' % item)
        search_res.append(item)
        tr_print('[res] %s' % search_res)

# main
tc = Thread(target=consumer, args=(q,))
tc.daemon = True
tc.start()

threads = []
used_threads = 0
for i, files in enumerate(file_chunks):

    t = Thread(target=producer, args=(files, q))
    t.start()
    threads.append(t)

    if len(threads) >= nthreads or i >= len(file_chunks)-1:
        for tr in threads:
            tr.join()
            used_threads += 1
            # print '[thread] quit %s' % tr
# wait until all items consumed
q.join()

# stop daemon thread, unneccesary
q.put(_sentinel)
time.sleep(2)

print '[results], threads: %s' % used_threads
for sub_res in search_res:
    for f, match in sub_res:
        print 'File %s' % f
        for row in match:
            print '--> ', row
