

__all__ = [
    'VIEWS',
    'RESPONSE_VIEWS',
    'NAMES',
    ]


NAMES = ('Minimal', 'Basic', 'Full')

VIEWS = {
    'minimal': (('Informants', 'infid'), ('Informants', 'informid'),
                ('Informants', 'yearinterviewed'), ('Informants', 'sex'),
                ('Informants', 'age'), ('Communities', 'state'),
                ),

    'basic': (('Informants', 'infid'), ('Informants', 'informid'),
              ('Informants', 'oldnumber'), ('FieldWorkers', 'code'),
              ('Informants', 'yearinterviewed'), ('Informants', 'inftype'),
              ('Informants', 'generation'), ('Informants', 'sex'),
              ('Informants', 'age'), ('Informants', 'education'),
              ('Informants', 'occupation'), ('Informants', 'race'),
              ('Communities', 'type'), ('Communities', 'state'),
              ),

    'full': (('Informants', 'infid'), ('Communities', 'comid'),
             ('Informants', 'informid'), ('Informants', 'oldnumber'),
             ('Informants', 'auxiliary'), ('FieldWorkers', 'code'),
             ('WorkSheets', 'code'), ('Informants', 'yearinterviewed'),
             ('Informants', 'inftype'), ('Informants', 'generation'),
             ('Informants', 'cultivation'), ('Informants', 'sex'),
             ('Informants', 'age'), ('Informants', 'education'),
             ('Informants', 'occupation'), ('Informants', 'race'),
             ('Informants', 'latitude'), ('Informants', 'longitude'),
             ('Communities', 'type'), ('Communities', 'state'),
             ),
    }

RESPONSE_VIEWS = {
    'minimal': ((('Responses', 'item'), 2), (('Responses', 'simplephone'), 3),
                (('Responses', 'doubtflag'), 4),
                ),

    'basic': ((('Responses', 'item'), 3), (('Responses', 'gramflag'), 4),
              (('Responses', 'doubtflag'), 5),
              (('Responses', 'commentcodes'), 6),
              (('Responses', 'commenttext'), 7),
              (('Responses', 'simplephone'), 8),
              ),

    'full': ((('Responses', 'item'), 2),
             (('Responses', 'gramflag'), 3), (('Responses', 'doubtflag'), 4),
             (('Responses', 'commentcodes'), 5),
             (('Responses', 'commenttext'), 6),
             (('Responses', 'simplephone'), 7),
             ),
    }

