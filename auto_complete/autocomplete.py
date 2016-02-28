import readline
import logging
import os
from pprint import pprint
from fileutils import find_file_type_paths, get_fs_drives
from fuzzy import match_fuzzy, bcolors

"""
autocomplete.py
status: complete

Scans filesystem for folders having source code in java and python and build a
list of dir paths.

Shows prompt that can autocomplete dir paths based on user string.
Press tab to trigger autocomplete.

By default, list of suggestion is cut if it exceeds lenght of 5. The rest si
shown as '...'.

Suggestions shown have highlighted letters that match the string. Match
algorithm is kind of fuzzy, meaning that words can occur anywhere in the match
string but has to be in proper order. It is very basic fuzzy match though.

Reference
http://stackoverflow.com/questions/7821661/how-to-code-autocompletion-in-python
"""

log_file = 'junk.log'
# logging.basicConfig(filename=log_file,
                    # level=logging.DEBUG)

class Completer(object):
    """Completer for readline CLI auto-complete feature

    readline will call method .complete with user text
    and state counting from 0 to n until .complete returns
    response as non string. Then it will show all responses
    to user.

    :limit_output limit number of suggestion shows, set 0 to disable
    :opts list of all strings to be auto-completed
    """
    def __init__(self, opts, limit_output=5):
        self.opts = opts
        self.matches = []
        self.limit = limit_output

    def complete(self, text, state):
        if state == 0:
            if text:
                # self.matches = [opt for opt in self.opts if opt.startswith(text)]
                # self.matches = match_anywhere(text, self.opts)
                self.matches = match_fuzzy(text, self.opts, color=True)
            else:
                self.matches = self.opts[:]
        logging.debug('[matches] {}'.format(self.matches))

        try:
            response =  self.matches[state]
            if self.limit > 0:
                if state == self.limit:
                    response = '...'
                elif state > self.limit:
                    response = None
        except IndexError:
            response = None
        logging.debug('Text {}, state {}, response {}'.format(
                      text, state, response))
        return response

def match_anywhere(sub, items):
    return [item for item in items if item.find(sub) > -1]


class FreshReader(object):
    """File reader that shows only new content

    Use case is to make regular calls against file that
    has been updated over time. Each call wil show only
    new lines added since previous call.
    """
    def __init__(self, fname):
        self.fname = fname
        self.last_seek = 0

    # def write(self, s):
    #     with open(self.fname, 'a+') as fp:
    #         fp.write(s)

    def show_fresh(self):
        print '[show fresh] >>'
        with open(self.fname) as fp:
            fp.seek(self.last_seek)
            for line in fp:
                print line.strip('\n')
            self.last_seek = fp.tell()

# verify fuzzy match manually
# fi = find_file_type_paths('d:\\')
# pprint(fi)
# rep = ''
# while(rep != 'q'):
#     rep = raw_input('>> ').strip('\n')
#     pprint(match_fuzzy(rep, fi))

# opts = ('card', 'bar', 'barman', 'capybara', 'canyon', 'zebra')
# opts = ('card', bcolors.BOLD + 'ba' + bcolors.ENDC + 'r' , 'barman')

# run only on 'd:', takes too long on 'c:', no searching for specific file type
# helps to cut time but it still hangs on 'c:' longer than acceptable
opts = find_file_type_paths(root='d:\\')
readline.set_completer(Completer(opts).complete)
readline.parse_and_bind('tab: complete')

reply = ''
while reply != 'q':
    reply = raw_input('Prompt ("q" to quit): ')



