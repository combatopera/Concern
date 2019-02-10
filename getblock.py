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

import re

indent = re.compile(r'^\s+')
eol = '\n' # FoxDot uses API so anything is fine.
lasteol = '\xb6' + eol # Pilcrow.

def getblock(text, onebasedrow):
    start = onebasedrow - 1
    end = start + 1
    lines = text.splitlines()
    if not lines[start]:
        text = '# Nothing to send.'
    else:
        while 0 <= start - 1 and indent.search(lines[start]) is not None:
            start -= 1
        n = len(lines)
        while end < n and indent.search(lines[end]) is not None:
            end += 1
        text = eol.join(lines[start:end])
    return text + lasteol
