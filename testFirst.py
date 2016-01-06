from findItOO import StringCutter
import unittest
import os
import findItOO
import tempfile
import re

class Tester(unittest.TestCase):
    def testFilepathCutting(self):
        paths = ('c:', os.path.sep, 'a', 'b', 'c', 'd')
        path = os.path.join(*paths)

        cutter = StringCutter(78)
        self.assertEquals(cutter.cut(''), '')
        cutter.limit = 100
        self.assertEquals(cutter.cut(path), path)
        cutter.limit = 4
        self.assertEquals(cutter.cut(path), r'...\c\d')
        cutter.limit = 9
        self.assertEquals(cutter.cut(path), r'...\a\b\c\d')

    def testSearchContextPrint(self):
        txt = """short text
        to test functionality
        of printing search context
        in the vein of unit grep
        with some additonal features
        to assist in coding and other
        stuffs"""

        print '>> Unittest context print'
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(txt)
            test_file = temp.name

        try:
            uut = findItOO.GrepFiles('fake', 'fake')
            res = uut.gather_context_lines(test_file, 4, 1, 1)
            expect = ('of printing search context'
                '-- in the vein of unit grep'
                'with some additonal features')
            self.assertEquals(''.join(self.strip_headers(res)), expect)

            res = uut.gather_context_lines(test_file, 1, 2, 3)
            expect = ('-- short text'
                      'to test functionality'
                      'of printing search context')
            self.assertEquals(''.join(self.strip_headers(res)), expect)

            res = uut.gather_context_lines(test_file, 7, 5, 0)
            expect = ('-- stuffs')
            self.assertEquals(''.join(self.strip_headers(res)), expect)

        finally:
            print '[remove test file] ', test_file
            os.unlink(test_file)

    def strip_headers(self, lines):
        return [re.sub('\d+:\s+', '', line) for line in lines]

unittest.main()

