# Copyright 2019, 2021, 2022 Andrzej Cichocki

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

import re, sys

toplevel = re.compile(r'^\S')
anytext = re.compile(r'\S')
eol = '\n' # FoxDot uses API so anything is fine.
pilcrow = eol

def _istoplevel(line):
    return toplevel.search(line) is not None

def _hastext(line):
    return anytext.search(line) is not None

def getblock(text, first, last, pilcrow):
    return Block.get(text.splitlines(), first, last, pilcrow).block

class Block:

    @classmethod
    def get(cls, lines, first, last, pilcrow):
        max = len(lines) - 1
        first -= 1
        last -= 1
        i = first
        while i < max and not _hastext(lines[i]):
            if i >= last and _istoplevel(lines[i + 1]):
                return cls(None, None, '# Nothing to send.' + pilcrow + eol)
            i += 1
        while last < max and not _istoplevel(lines[last + 1]):
            last += 1
        while first < last and not _hastext(lines[first]):
            first += 1
        while first and not _istoplevel(lines[first]):
            first -= 1
        lines[last] # Check for out of range.
        return cls(first, last, eol.join(l for l in lines[first:last + 1] if _hastext(l)) + pilcrow + eol)

    def __init__(self, first, last, block):
        self.first = first
        self.last = last
        self.block = block

class ReadBlocks:

    def __init__(self, stroke):
        self.lines = sys.stdin.read().splitlines()
        def _readbounds():
            self.first, self.last = map(int, sys.argv[1:])
        def default():
            _readbounds()
            self.last = len(self.lines)
        def alternate():
            _readbounds()
        locals()[stroke]()

    def monolith(self):
        return Block.get(self.lines, self.first, self.last, pilcrow).block

    def chunked(self, n):
        first = self.first
        for i in range(n):
            # Most importantly last must achieve self.last:
            last = first + (self.last - first) // (n - i)
            actual = Block.get(self.lines, first, last, '')
            if actual.last is not None:
                yield actual.block
                first = actual.last + 1
