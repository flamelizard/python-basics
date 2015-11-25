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
from Lumpy import Lumpy

def get_files(root, exts):
    found = []
    for d, _, files in os.walk(root):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext in exts:
                found.append(os.path.join(d, f))
    return found

def search_file(f, exp):
    lines = []
    with open(f) as fp:
        for line in fp:
            if line.find(exp) != -1:
                lines.append(line.strip('\n'))
    return lines

def collect_live_res(feeds):
    for f, lines in feeds:
        print 'in %s' % f
        for line in lines:
            print '>> %s' % line
        print


root = 'd:/'
suff = ['.py']


found = get_files(root, suff)
# print found

line_match = []
for f in found:
    lines = search_file(f, 'bisect')
    if lines:
        line_match.append((f, lines))

collect_live_res(line_match)



