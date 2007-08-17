
'''This provides the function to simplify the full phonetics.

>>> simplify(\'\\xe1\\xbe\\xec\\xb0b\\xe1\\xbe\\xbam\\xb0\')
\'\\xe1\\xec\\xb0b\\xe1m\\xb0\'
'''

_subdiacritics = [
    chr(141), chr(142), chr(143), chr(144), chr(145), chr(146), chr(147),
    chr(148), chr(149), chr(150), chr(151), chr(152), chr(153), chr(154),
    chr(155), chr(156), chr(157), chr(158), chr(159), chr(172),
    ]

_superdiacritics = [
    chr(134), chr(135), chr(136), chr(137), chr(138), chr(139), chr(140),
    chr(167), chr(187), chr(219), chr(220), chr(221), chr(223), chr(224),
    chr(234), chr(254),
    ]

_stress = [
    chr(94), chr(195), chr(205), chr(229), chr(233), chr(245), chr(132),
    chr(133), chr(160), chr(171), chr(186), chr(188), chr(189), chr(190),
    chr(251),
    ]

# These are left out
_other = [
    chr(191),
    ]


def simplify(string):
    '''This simplifies the phonetics in string.
    >>> simplify(\'\\xe1\\xbe\\xec\\xb0b\\xe1\\xbe\\xbam\\xb0\')
    \'\\xe1\\xec\\xb0b\\xe1m\\xb0\'
    '''
    for item in _subdiacritics+_superdiacritics+_stress:
        string = string.replace(item, '')
    return string

