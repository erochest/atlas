
# Linguistic Atlas Projects

Some notes about the structure of the code and the technologies used. More detail to come, if I have time.

## A Little History

The timeline's fuzzy, but I think I started working on this site during the late 1990s, and continued being the primary (sole?) developer until 2004. I was primarily working with Python. This was before Django or Flask, so the libraries and frameworks for web development in Python were very different than they are now. Web development in general was very different. You'll see what I mean.

The site that I took over was a set of Perl scripts that read the data from some CSV files. There were some security issues with this, so I rewrote them in Python. Dr. Kretzschmar wanted to maintain the original version of the site also, so this iteration of the site is still in the code under `www/cgi-bin`.

To update the site, I had several goals:

* Update the design (which now looks dated again);
* Store the data in a RDBMS;
* Recode the library from lamcour (the ad hoc encoding that the data was originally stored in) to Unicode, which had come out in the meantime.

There are three sections to the data:

* [`lamrecode`](#lamrecode): A small codec library to change the encoding from lamcour to Unicode.
* [`lap`](#lap): A library of utilities. This might roughly be the business logic, models, views, controllers, and utility scripts. It's messy.
* [`www`](#www): The static site and CGI scripts for the older version of the site.

## `lamrecode`

This is the codec library and utility scripts for converting strings from the lamcour encoding to Unicode. The core of this is a module written in C, and the data for the conversion itself is in an array in the `lamtable.h` file. It basically just looks up the code point in the table, which contains the string of Unicode characters that the lamcour character should be translated to. Usually this is just an identity function, although there are a few cases where it changes to one or two different characters.

The C module, `_lamcour` is in `_lamcour.c`. It's mainly boilerplate.

Finally, `lamcour.py` is a Python wrapper around `_lamcour`.

## `lap`

This directory contains most of the code. It also contains scripts to load the data from CSV files into a MySQL database.

## `www`

This contains the static parts of the site, the CGI scripts for the original site, and the templates for the Quixote site.

