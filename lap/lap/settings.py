
'''
The 'lap.settings' module.

This provides locale-dependant settings for the site.

This looks at the 'ATLASSITE_TARGET' environment variable, which should
be one of these values:

    'DEVEL' -- This is used on the development machine during testing. It turns
    on the "Debugging" link and prints the SQL query.

    'DEVEL_TEST' -- This is used on the development machine after testing. It
    suppresses all development information.

    'DEPLOY_TEST' -- This is used on the deployment machine before deployment.
    It shows all development information.

    'DEPLOY' -- This is used on the deployment machine. This is the default.

Constants:

    'ENVIRON_KEY' -- The environment variable to set to one of the values
    above. This is provided mainly for documentation.

    'meta' -- Meta information about the site. It contains these attributes:

        'development' -- A 'bool' indicating whether this is a development
        environment (i.e., whether the 'ATLASSITE_TARGET' environment variable
        is either 'DEVEL', or 'DEPLOY_TEST').

        'version' -- A 'str' version identifier for the site.

        'projects' -- A 'dict' containing the projects' settings. This maps
        "afam" to the 'afam' constant below, and likewise for "lamsas" and
        "lapnw".

    'afam' -- Information about the African-American and Gullah project. It
    contains these attributes:

        'name' -- The name of the project.

        'db' -- The name of the project's database.

        'description' -- A short description of the project.

        'baseimage' -- The file name of the base map graphic.

        'mapheight', 'mapwidth' -- The dimensions of the map graphic.

        'leftmargin', 'topmargin' -- The initial top and left margins for
        writing on the map graphic.

        'infcount', 'comscount' -- The number of informants and communities,
        respectively, in the project.

        'respinf', 'respcom' -- The map location to start writing the number of
        responses for informants and communities.

        'noreinf', 'norecom' -- The map location to start writing the number of
        informants and communities that did not respond to the item.

        'links' -- A 'list' of the side bar links.

    'lamsas' -- Information about the Linguistic Atlas of the Middle and South
    Atlantic States project. It contains these attributes:

        'name' -- The name of the project.

        'db' -- The name of the project's database.

        'description' -- A short description of the project.

        'baseimage' -- The file name of the base map graphic.

        'mapheight', 'mapwidth' -- The dimensions of the map graphic.

        'leftmargin', 'topmargin' -- The initial top and left margins for
        writing on the map graphic.

        'infcount', 'comscount' -- The number of informants and communities,
        respectively, in the project.

        'respinf', 'respcom' -- The map location to start writing the number of
        responses for informants and communities.

        'noreinf', 'norecom' -- The map location to start writing the number of
        informants and communities that did not respond to the item.

        'links' -- A 'list' of the side bar links.

    'lapnw' -- Information about the Linguistic Atlas of the Pacific North West
    project. It contains these attributes:

        'name' -- The name of the project.

        'description' -- A short description of the project.

        'datadir' -- The location of the LAPNW data directory.

        'mapdir' -- The location of the LAPNW map directory.

        'links' -- A 'list' of the side bar links.

    'links' -- Information about the side bar links on various pages. It
    contains these attributes:

        'base' -- The links of projects.

        'info' -- The links of site information.

        'util' -- The links to the utilities pages.

        'exits' -- External links.

    'locale' -- Settings that change according to the location of the site
    (taken from the environment variable 'ATLASSITE_TARGET').

        'baseurl' -- The base URL of the site.

        'baseold' -- The base URL of the old site.

        'basecgi' -- The base URL of the cgi-bin directory.

        'htdocs' -- The base directory for the site on the local file system.

        'cgibin' -- The location of the cgi-bin directory.

        'etc' -- The location of the site's etc directory.

        'old_data' -- The location of the old data directories.

        'connect' -- A 'dict' containing the key word arguments to pass to the
        database module's 'connect' function when connecting to the database.

        'webmaster' -- The webmaster's e-mail address.

        'sessions' -- A 'dict' containin the key word arguments to use when
        initializing the sessions mechanism.

'''


__all__ = [
    'ENVIRON_KEY',
    'UnknownSettingsLocaleError',
    'meta',
    'afam',
    'lamsas',
    'lapnw',
    'links',
    'locale',
    ]


import os, sys
from lap.util import Data


ENVIRON_KEY = 'ATLASSITE_TARGET'
LAPDIR = os.path.abspath(os.path.dirname(__file__))


class UnknownSettingsLocaleError(Exception):
    pass


meta = Data(
    development=os.environ.get(ENVIRON_KEY) in ('DEVEL', 'DEPLOY_TEST'),
    version='0.0.5 alpha',
    projects={},
    db='LAP',
    )

afam = Data(
    name='afam',
    db='AFAM',
    description='Linguistic Atlas of African-American and Gullah Speakers',
    mapheight=675, mapwidth=525,
    leftmargin=305, topmargin=485,
    infcount=62, comscount=44,
    respinf=(417, 521), respcom=(425, 539),
    noreinf=(417, 611), norecom=(425, 629),
    links=['<a href=".">AFAM</a>',
           [('afam/info', 'About'),
            ('afam/browse?clear=1', 'Browse'),
            ]],
    )

lamsas = Data(
    name='lamsas',
    db='LAMSAS',
    description='Linguistic Atlas of the Middle and South Atlas States',
    mapheight=900, mapwidth=510,
    leftmargin=288, topmargin=681,
    infcount=1162, comscount=484,
    respinf=(400, 717), respcom=(408, 735),
    noreinf=(400, 807), norecom=(408, 825),
    links=['<a href=".">LAMSAS</a>',
           [('lamsas/info', 'About'),
            ('lamsas/browse?clear=1', 'Browse'),
            ('lamsas/analyses', 'Analyses'),
            ('lamsas/scrapbook', 'Scrap Book'),
            ]],
    )

lapnw = Data(
    name='lapnw',
    description='Linguistic Atlas of the Pacific North West',
    links=['<a href="./">LAPNW</a>',
           [('lapnw/info', 'About'),
            ('lapnw/db/', 'Database'),
            ('lapnw/data/', 'Data'),
            ('lapnw/maps/', 'Maps'),
            ]],
    )

meta.projects['afam'] = afam
meta.projects['lamsas'] = lamsas
meta.projects['lapnw'] = lapnw

links = Data(
    base=['Projects',
          [('afam', 'AFAM'),
           ('lags', 'LAGS'),
           ('lamsas', 'LAMSAS'),
           ('lancs', 'LANCS'),
           ('lane', 'LANE'),
           ('lao', 'LAO'),
           ('lapnw', 'LAPNW'),
           ('lapw', 'LAPW'),
           ('larms', 'LARMS'),
           ('laum', 'LAUM'),
           ]],
    info=['<a href="index.html">Information</a>',
          [('information/about.html', 'About'),
           ('information/intro.html', 'Introduction'),
           ('information/ling.html', 'Linguistics'),
           ('information/phonetics.html', 'Phonetics'),
           ('information/projects.html', 'Projects'),
           ('information/analyses.html', 'Analyses'),
           ('information/databases.html', 'Databases'),
           ('information/faq.html', 'FAQ'),
           ('information/contacts.html', 'Contacts'),
           ('information/links.html', 'Links'),
           ]],
    util=['<a href="index.html">Utilities</a>',
          [('utils/fonts.html', 'Fonts'),
           ]],
    exits=['Exits',
           [('old/index.html', 'The Old Atlas Site'),
           ]],
    )

target = os.environ.get(ENVIRON_KEY, None)

if target in ('DEVEL', 'DEVEL_TEST', None):
    locale = Data(
        htdocs='/home/eric/projects/atlas/www/htdocs',
        cgibin='/home/eric/projects/atlas/www/cgi-bin',
        etc='/home/eric/projects/atlas/www/etc',
        old_data='/home/eric/projects/atlas/old-data',
        connect={'user': 'w_lap', 'passwd': '********', 'host': 'localhost',
                 'db': 'lap'},
        webmaster='webmaster@us.english.uga.edu',
        cgiurl='http://lap/cgi-bin',
        basecgi='http://lap/cgi-bin',
        baseold='http://lap/old',
        )

elif target in ('DEPLOY_TEST', 'DEPLOY', None):
    locale = Data(
        htdocs='/home/users/lap_www/htdocs',
        cgibin='/home/users/lap_www/cgi-bin',
        old_data='/home/users/lap_www/old-data',
        etc='/home/users/lap_www/etc',
        connect={'user': 'w_lap', 'passwd': '********', 'host': 'localhost',
                 'db': 'lap'},
        webmaster='w_lap@www.lap.uga.edu',
        basecgi='http://www.lap.uga.edu/cgi-bin',
        baseold='http://www.lap.uga.edu/old',
        cgiurl='http://www.lap.uga.edu/cgi-bin',
        )

else:
    raise UnknownSettingsLocaleError, 'Unknown target platform: %s' % target

del target

for project in (afam, lamsas):
    project.baseimage = os.path.join(LAPDIR, 'web', 'site', project.name,
                                     'mapbase.png')

lapnw.datadir = os.path.join(locale.htdocs, 'lapnw', 'data')
lapnw.mapsdir = os.path.join(locale.htdocs, 'lapnw', 'maps')

