"""
findIt
Help to show where and how is used an expression in question
Often needs to see real-world example to understand how the command is used or
just to see best practices.

search custom folders
custom folders defined ?
do not count uniteresting pieces of code such as import

a bit of fuzzy search - match more key words on a line to better target search
it might search for key words on multiple lines

Changelist
ok - optionally, print context after and before match
ok - print line numbers
ok - do not show this script in results
no - show live results

"""

import sys
import os
from fnmatch import fnmatch
import threading
import functools
import time
import re
import sys
from threading import Thread
from Queue import Queue, Empty
import collections
import utils

class Null(object):
    def write(self, *args):
        pass
# sys.stdout = Null()


class GrepFiles(object):
    """Search for regular expr in all files with suffix

    :root starting filesystem path
    :context control context printing of grep results
    """
    def __init__(self, root, regex, suff=('.py', '.java'), case=False,
                 context=()):
        self.root = root
        self.regex = re.compile(regex) if case else re.compile(regex, re.IGNORECASE)
        self.suff = suff
        self.q = Queue()    # shared thread-safe var for sub-results
        self.results = []   # used only for run with threads
        self.chunk_size = 100
        self.n_threads = 3
        self._sentinel = object()   # signal end to daemon thread
        self.safeprint = threading._allocate_lock()
        self.stats = collections.Counter()
        self.live_res = True
        self.context = context

        if not regex:
            print '[Error] No search string given'
            sys.exit(0)

    def test(self):
        for i in range(3):
            files = self.get_files()
            # files.insert(0, '>>%i' % i)
            utils.dump_to_file('findIt_%i.dump' % i, '\n'.join(files))

    def get_files(self):
        found = []
        for d, _, files in os.walk(self.root):
            for f in files:
                _, ext = os.path.splitext(f)
                if ext in self.suff:
                    # mixed up forward and backward slash from .walk and .join
                    fpath = os.path.normcase(os.path.join(d, f))
                    found.append(fpath)

        # del caller script
        caller = os.path.basename(sys.argv[0])
        for i, f in enumerate(found):
            if caller == os.path.basename(f):
                found.pop(i)
                break
        return found

    # def search_file(self, f):
    #     lines = []  # list of tuples
    #     cnt = 0     # track line number
    #     with open(f) as fp:
    #         for line in fp:
    #             cnt += 1
    #             if re.search(self.regex, line):
    #                 lines.append((cnt, line.strip('\n')))
    #     return lines

    def search_file(self, f):
        lines = []  # list of tuples
        cnt = 0     # track line number
        context = False
        with open(f) as fp:
            for line in fp:
                cnt += 1
                if re.search(self.regex, line):
                    lines.append((cnt, line.strip('\n')))
        return lines

    def gather_context_lines(self, file, line_no, aft=2, bef=0):
        # print '[context]', file
        res = []
        with open(file) as fp:
            lines = fp.readlines()

        line_no -= 1    # account for 0-th element
        lines = [line.strip('\n').strip() for line in lines]
        low = 0 if line_no-bef < 0 else line_no-bef
        high = len(lines)-1 if line_no+aft > len(lines)-1 else line_no+aft

        for i in range(low, high+1):
            if i == line_no:
                # print '{0}: -- {1}'.format(i, lines[i])
                res.append('{0}: -- {1}'.format(i+1, lines[i]))
            else:
                # print '{0}:    {1}'.format(i, lines[i])
                res.append('{0}:    {1}'.format(i+1, lines[i]))
        print
        return res

    def run(self):
        res = []
        for f in self.get_files():
            try:
                match = self.search_file(f)
            except IOError as e:
                print 'Error: {0}'.format(e)
                continue
            if match:
                res.append((f, match))
        self.show_results(res)

    def run_threaded(self):
        """threading hands-on

        Python threading is NOT for compute intensive ops. For that, there is
        module multiprocessing. It is way slower here than single thread
        approach.
        """
        file_chunks = self.split_list(self.get_files())

        tc = Thread(target=self.consumer, args=(self.q,))
        tc.daemon = True
        tc.start()

        threads = []
        for i, files in enumerate(file_chunks):

            t = Thread(target=self.producer, args=(files,))
            t.start()
            threads.append(t)

            if len(threads) >= self.n_threads or i >= len(file_chunks)-1:
                for tr in threads:
                    tr.join()
                    self.stats['used_threads'] += 1
                    # print '[thread] quit %s' % tr
                threads = []
        # wait until all items consumed
        self.q.join()

        # stop daemon thread, unneccesary
        self.q.put(self._sentinel)
        time.sleep(5)

        all_res = []
        for partial in self.results:
            all_res.extend(partial)
        self.show_results(all_res)

    def tr_print(self, msg, mute=True):
        """Print on thread - no text overlap"""
        if mute:
            return
        with self.safeprint:
            print msg

    def producer(self, files):
        """Search for string in file chunk"""
        line_match = []
        for f in files:
            lines = self.search_file(f)
            if lines:
                line_match.append((f, lines))
        self.tr_print('[prod] %s' % line_match)
        if line_match:
            self.q.put(line_match)

    def consumer(self, q):
        """Offload search results to the instance var"""
        while True:
            try:
                item = q.get(timeout=2.0)
            except Empty:
                continue
            if item is self._sentinel:
                self.tr_print('[consumer] quit signal received')
                q.put(item)
                break
            self.tr_print('[consume] %s' % item)
            self.results.append(item)
            q.task_done()

    def split_list(self, lst):
        """Split list to smaller chunks"""
        assert isinstance(lst, list)
        return ([lst[i:i+self.chunk_size] for i in
                xrange(0, len(lst)-1, self.chunk_size)])

    def show_results(self, res):
        print '== Search results =='
        threads = self.stats['used_threads']
        if threads > 0:
            print '[threads: %s]' % threads

        cutter = StringCutter()
        if self.context:
            aft, bef = self.context
            for f, lines in res:
                print "==> {}".format(cutter.cut(f))

                for line_no, line in lines:
                    s = self.gather_context_lines(f, line_no, aft, bef)
                    print '\n'.join(s)
                print
        else:
            for f, lines in res:
                print "==> {}".format(cutter.cut(f))

                for line_no, line in lines:
                    print '{0:>4}:  {1}'.format(line_no, line.strip())
                print

class StringCutter(object):
    def __init__(self, limit=78):
        self.limit = limit

    def _file_path(self, s):
        """Cut file path
        :return string

        Remove leading components until length is met
        """
        components = s.split(os.path.sep)
        # print '[cut]', components, os.path.sep
        line_len = 0
        new_path = []

        components.reverse()
        for comp in components:
            line_len += len(comp)+1             # account for separator
            if line_len > self.limit:
                new_path.insert(0, '...')
                break
            new_path.insert(0, comp)
        return os.path.sep.join(new_path)

    def cut(self, s):
        """Cut string to specified length

        File path is cut only on a separator
        """
        if len(s) > self.limit:
            fspath = re.compile(r'\\\w+\\', re.IGNORECASE)
            if re.search(fspath, s):
                s = self._file_path(s)
            else:
                s = s[:self.limit]
        return s

if __name__ == '__main__':

    exp = 'unittest'
    # root = 'c:/Users/Tom/ideaprojects/'
    root = "d:/devel/"

    grep = GrepFiles(root, exp, context=(2,0))
    grep.run()
    # grep.run_threaded()
    # grep.test()
