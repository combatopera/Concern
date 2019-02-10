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

from getblock import getblock
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
something else'''

def seq(first, last):
    return range(first, last + 1)

class TestGetBlock(unittest.TestCase):

    def test_works(self):
        self.assertEqual('# Nothing to send.\xb6\n', getblock(text, 1))
        self.assertEqual('hello\xb6\n', getblock(text, 2))
        for r in seq(3, 4):
            self.assertEqual('function with\n indented block\xb6\n', getblock(text, r))
        clazz = 'class with\n  block after blank\n  \tand its own indented block\n  and back again after a wrong blank\xb6\n'
        for r in seq(5, 10):
            self.assertEqual(clazz, getblock(text, r))
        self.assertEqual('something else\xb6\n', getblock(text, 11))
