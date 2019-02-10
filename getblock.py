import re, os

indent = re.compile(r'^\s+')
eol = os.linesep
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
