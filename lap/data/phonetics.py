

__version__ = '0.0'
__all__ = [
    'simplify',
    ]


import re


SUBSCRIPT = u'\u0317\u0323\u0325\u032c\u032f\u032a\u033a\u0331\u032b\u0329' \
            u'\u032e\u031e\u031d\u031f\u032d\u0318\u0319\u031c\u203f\u0327'
SUPERSCRIPT = u"\u030b\u0319\u0318\u0311\u030a\u0302\u0361'\u0307\u030c" \
              u"\u0300\u0306\u0304\u0308\u0301\u0303"
STRESS = u'^\u02b9\u02cb\u02c8\u02d8\u02cc\u02d5\u02d4\u02b2\u02c4\xb7' \
         u'\u02c2\u02c5\u02c3~'
REMOVENDA = SUBSCRIPT + SUPERSCRIPT + STRESS
re_remove = re.compile(u'[' + re.escape(REMOVENDA) + ']', re.UNICODE)


def simplify(unistring, regex=re_remove):
    return regex.sub('', unistring)


