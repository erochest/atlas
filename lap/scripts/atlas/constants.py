
'''This provides classes that act like enumerators (or more properly, records),
and that keep track of long and short descriptions of values.

>>> inftype.II
1
>>> inftype.COMMON
1
>>> inftype.short[1]
'II'
>>> inftype.long[1]
'common'
'''

__all__ = [
    'Boolean',
    'auxiliary',
    'cultivation',
    'doubtflag',
    'inftype',
    'generation',
    'sex',
    'education',
    'occupation',
    'race',
    'gramflag',
    'comtype',
    'tabletype',
    ]

class Boolean:
    range = (0, 1)
    N = NO = 0
    Y = YES = 1
    F = FALSE = 0
    T = TRUE = 1
    short = ('N', 'Y')
    long = ('no', 'yes')

auxiliary = cultivation = doubtflag = Boolean

class inftype:
    range = (0, 1, 2)
    I = FOLK = 0
    II = COMMON = 1
    III = CULTIVATED = 2
    short = ('I', 'II', 'III')
    long = ('folk', 'common', 'cultivated')

class generation:
    range = (0, 1)
    A = OLDER = 0
    B = YOUNGER = 1
    short = ('A', 'B')
    long = ('older', 'younger')

class sex:
    range = (0, 1)
    F = FEMALE = 0
    M = MALE = 1
    short = ('F', 'M')
    long = ('female', 'male')

class education:
    range = (0, 1, 2, 3, 4, 5, 6)
    I = ILLITERATE = 0
    SG = SOME_GRADE_SHOOL = 1
    G = GRADE_SCHOOL = 2
    SH = SOME_HIGH_SCHOOL = 3
    H = HIGH_SCHOOL = 4
    SC = SOME_COLLEGE = 5
    COLLEGE = 6
    short = ( 'I', 'SG', 'G', 'SH', 'H', 'SC', 'C' )
    long = (
        'none/illiterate',
        'some grade school: 1-4 years',
        'grade school: 5-8 years',
        'some high school: 9-11 years',
        'high school: 12 years',
        'some college (also trade school)',
        'college graduate',
        )

class occupation:
    range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    P = PROFESSIONAL = 0
    F = FARMERS = 1
    M = MANAGERIAL = 2
    R = CLERICAL = 3
    C = CRAFTSMEN = 4
    O = OPERATIVES = 5
    H = PRIVATE_HOUSEHOLD = 6
    S = SERVICE = 7
    W = FARM_LABORERS = 8
    K = HOUSEKEEPERS = 9
    L = NON_FARM_LABORERS = 10
    U = UNEMPLOYED = 11
    G = STUDENT = 12
    short = ( 'P', 'F', 'M', 'R', 'C', 'O', 'H', 'S', 'W', 'K', 'L', 'U', 'G' )
    long = (
      'professional and technical',
      'farmers',
      'managers, officials, proprietors',
      'clerical and sales',
      'craftsmen and foremen',
      'operatives',
      'private household workers',
      'service workers',
      'farm laborers',
      'keeping house',
      'non-farm laborers',
      'seeking work', 'student',)
      
class race:
    range = (0, 1)
    W = CAUCASIAN = 0
    B = AFRICAN_AMERICAN = 1
    short = ( 'W', 'B' )
    long = ( 'caucasian', 'african-american' )

class gramflag:
    range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    N = NOUN = 0
    V = VERB = 1
    M = PRONOUN = 2
    C = COPULA = 3
    A = ADJECTIVE = 4
    B = ADVERB = 5
    J = CONJUNCTION = 6
    P = PREPOSITION = 7
    X = VERB_AUXILIARY = 8
    D = DETERMINER = ARTICLE = 9
    R = RELATIVE_PRONOUN = 10
    T = EXISTENTIAL = THERE = IT = 11
    S = CLAUSE = 12
    E = VERB_PHRASE = 13
    Q = PREPOSITIONAL_PHRASE = 14
    O = NOUN_PHRASE = 15
    K = MODIFIER_PHRASE = 16
    short = ( 'N', 'V', 'M', 'C', 'A', 'B', 'J', 'P', 'X', 'D', 'R', 'T',
              'S', 'E', 'Q', 'O', 'K', )
    long = (
        'noun',
        'verb',
        'pronoun',
        'copula',
        'adjective',
        'adverb',
        'conjunction',
        'preposition',
        'verb auxiliary',
        'determiner (article)',
        'relative pronoun',
        "existential 'there', 'it', etc.",
        'complete clause',
        'word group with verb',
        'word group with preposition',
        'word group with noun',
        'word group with adjective or adverb',
        )

class comtype:
    range = (0, 1)
    R = RURAL = 0
    U = URBAN = 1
    short = ('R', 'U')
    long = ('rural', 'urban')

class tabletype:
    range = (0, 1, 2)
    g = GRAMMATICAL = 0
    l = LEXICAL = 1
    p = PHONETIC = 2
    short = ('g', 'l', 'p')
    long = ('grammatical', 'lexical', 'phonetic')


