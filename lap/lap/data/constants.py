

__version__ = '0.0'
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


from lap.util import Data


Boolean = {'N': 'No', 'Y': 'Yes'}

Informants = Data(
    auxiliary=Boolean,
    inftype={'I': 'Folk', 'II': 'Common', 'III': 'Cultivated'},
    generation={'A': 'Older', 'B': 'Younger'},
    cultivation=Boolean,
    sex={'F': 'Female', 'M': 'Male'},
    education={'0': 'Illiterate',
               '1': 'Some grade school',
               '2': 'Grade school',
               '3': 'Some high school',
               '4': 'High school',
               '5': 'Some college',
               '6': 'College'},
    occupation={'P': 'Professional and technical',
                'F': 'Farmers',
                'M': 'Managers, officials, proprietors',
                'R': 'Clerical and sales',
                'C': 'Craftsmen and foremen',
                'O': 'Operatives',
                'H': 'Private household workers',
                'S': 'Service workers',
                'W': 'Farm laborers',
                'K': 'Keeping house',
                'L': 'Non-farm laborers',
                'U': 'Seeking work',
                'G': 'Students'},
    race={'W': 'Caucasian', 'B': 'African-American'},
    )

Communities = Data(type={'R': 'Rural', 'U': 'Urban'})

Targets = Data(
    type={'p': 'Phonetic', 'g': 'Grammatical', 'l': 'Lexical'}
    )

Responses = Data(
    gramflag={'N': 'Noun', 'V': 'Verb', 'M': 'Pronoun', 'C': 'Copula',
              'A': 'Adjective', 'B': 'Adverb', 'J': 'Conjunction',
              'P': 'Preposition', 'X': 'Verb Auxiliary', 'D': 'Determiner',
              'R': 'Relative pronoun', 'T': 'Existential (there/it)',
              'S': 'Clause', 'E': 'Verb phrase', 'Q': 'Prepsitional phrase',
              'O': 'Noun phrase', 'K': 'Modifier phrase'},
    doubtflag=Boolean,
    )

