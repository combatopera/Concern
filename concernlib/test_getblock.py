# Copyright 2019 Andrzej Cichocki

# This file is part of Concern.
#
# Concern is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Concern is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Concern.  If not, see <http://www.gnu.org/licenses/>.

from .getblock import getblock
import unittest

text = '''
hello
function with
 indented block
class with

  block after blank
  \tand its own indented block
\t
  and back again after a wrong blank

something else
\t
 \t
last'''

class TestGetBlock(unittest.TestCase):

    def test_works(self):
        r = 0
        def block():
            nonlocal r
            r += 1
            return getblock(text, r, r, '\xb6')
        self.assertEqual('# Nothing to send.\xb6\n', block())
        self.assertEqual('hello\xb6\n', block())
        for _ in range(2):
            self.assertEqual('function with\n indented block\xb6\n', block())
        for _ in range(6):
            self.assertEqual('class with\n  block after blank\n  \tand its own indented block\n  and back again after a wrong blank\xb6\n', block())
        self.assertEqual('# Nothing to send.\xb6\n', block())
        self.assertEqual('something else\xb6\n', block())
        for _ in range(2):
            self.assertEqual('# Nothing to send.\xb6\n', block())
        self.assertEqual('last\xb6\n', block())
        self.assertRaises(IndexError, block)

    def test_visual(self):
        def block():
            nonlocal last
            last += 1
            return getblock(text, first, last, '')
        first = last = 10
        self.assertEqual('class with\n  block after blank\n  \tand its own indented block\n  and back again after a wrong blank\n', block())
        for _ in range(3):
            self.assertEqual('class with\n  block after blank\n  \tand its own indented block\n  and back again after a wrong blank\nsomething else\n', block())
        self.assertEqual('class with\n  block after blank\n  \tand its own indented block\n  and back again after a wrong blank\nsomething else\nlast\n', block())
        self.assertRaises(IndexError, block)
        first = last = 11
        for _ in range(3):
            self.assertEqual('something else\n', block())
        self.assertEqual('something else\nlast\n', block())
        self.assertRaises(IndexError, block)
        first = last = 12
        for _ in range(2):
            self.assertEqual('something else\n', block())
        self.assertEqual('something else\nlast\n', block())
        self.assertRaises(IndexError, block)
        first = last = 13
        self.assertEqual('# Nothing to send.\n', block())
        self.assertEqual('last\n', block())
        self.assertRaises(IndexError, block)
        first = last = 14
        self.assertEqual('last\n', block())
        self.assertRaises(IndexError, block)
