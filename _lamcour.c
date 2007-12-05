
#include <stdio.h>
#include <string.h>
#include <Python.h>
#include "lamtable.h"


static PyObject *LamcourError;

/****************************************************/
/* First, some utility functions.                   */
/****************************************************/

/* This is copied from the Python 2.2 distribution, */
/* Modules/_codecsmodule.c                          */
/* See that for copyright information.              */
static
PyObject *codec_tuple(PyObject *unicode,
                      int len)
{
    PyObject *v, *w;

    if (unicode == NULL)
        return NULL;
    v = PyTuple_New(2);
    if (v == NULL) {
        Py_DECREF(unicode);
        return NULL;
    }
    PyTuple_SET_ITEM(v, 0, unicode);
    w = PyInt_FromLong(len);
    if (w == NULL) {
        Py_DECREF(v);
        return NULL;
    }
    PyTuple_SET_ITEM(v, 1, w);
    return v;
}

/*
   This returns the length of a NULL-ended array of Py_UNICODE.
   */

int pyunilen(const Py_UNICODE *unicode) {
    int i;
    for (i = 0; unicode[i] != 0x0; i++);
    return i;
}

/*
   This returns true (1) if the first string begins with the second string.
   */

int pystartswith(const Py_UNICODE *string, const Py_UNICODE *prefix) {
    int i;
    for (i = 0; prefix[i] != 0x0; i++) {
        if ((string[i] != prefix[i]) || (string[i] == 0x0))
            return 0;
    }
    return 1;
}

/*
   This copies src into dest (which is assumed to be already allocated. (This
   might be a bit faster using memcpy or something.)
   */

void pyunicpy(const Py_UNICODE *src, Py_UNICODE *dest) {
    int i;
    for (i = 0; src[i] != 0x0; i++) {
        dest[i] = src[i];
    }
}

/*
   This looks up the beginning of unicode in lamcour_table. If it finds it,
   replacement is the lamcour character that corresponds to unicode, deltai is
   number of characters of unicode that correspond to replacement, and it
   returns 1. Otherwise, it returns 0, and replacement and deltai are left
   alone.
   */

int unicode_lookup(const Py_UNICODE *unicode, char *replacement, int *deltai) {
    int i, l;

    for (i = 0; i < 256; i++) {
        /* test, and if they are the same, assign result and break. */
        l = pyunilen(lamcour_table[i]);
        if ((l > 0) && (pystartswith(unicode, lamcour_table[i]))) {
            *replacement = (char)i;
            *deltai = l;
            return 1;
        }
    }

    return 0;
}

/****************************************************/
/* These are the work-horse functions.              */
/* o decode converts a string into a PyUnicodeObject*/
/*        (LAMCOUR -> Unicode).                     */
/* o encode converts a Py_UNICODE string into a     */
/*        PyString (Unicode -> LAMCOUR).            */
/* See the Python help for PyUnicode_EncodeUTF8 and */
/* PyUnicode_DecodeUTF8 for information about the   */
/* arguments these functions take.                  */
/* o errors can be:
Possible values for errors are 'strict' (raise an exception in case of an
encoding error), 'replace' (replace malformed data with a suitable replacement
marker, such as "?") and 'ignore' (ignore malformed data and continue without
further notice) */
/****************************************************/
static PyObject *decode(const char *data, int size, const char *errors)
{
    Py_UNICODE *unicode;
    PyObject *pyunicode;
    int unisize, i, j;

    /* figure out the length of the resulting string */
    unisize = 0;
    for (i = 0; i < size; i++)
        unisize += pyunilen(lamcour_table[(unsigned char)data[i]]);

    /* allocate memory */
    unicode = malloc(sizeof(Py_UNICODE) * (unisize + 1));
    unicode[unisize] = 0;

    /* copy the translations to the unicode string */
    for (i = 0, j = 0; i < size; i++) {
        pyunicpy(lamcour_table[(unsigned char)data[i]],
                (Py_UNICODE *)(unicode+j));
        j += pyunilen(lamcour_table[(unsigned char)data[i]]);
    }

    /* convert to python, release resources, and return */
    pyunicode = PyUnicode_FromUnicode(unicode, unisize);
    free(unicode);
    return pyunicode;
}

/*
   This takes a unicode string s and coverts size characters to the lamcour
   encoding, handling errors according to the errors argument.
   */

static PyObject *encode(const Py_UNICODE *s, int size, const char *errors)
{
    char *string, replacement=0;
    PyObject *pystring;
    int strsize=0, i, j, deltai=0;

    /* figure out the length of the resulting string */
    for (i = 0; i < size; i++) {
        if (unicode_lookup((const Py_UNICODE *)(s+i),
                    (char *)&replacement, &deltai)) {
            strsize += deltai;
        } else if (errors != NULL && strcmp(errors, IGNORE) == 0) {
            continue;
        } else if (errors != NULL && strcmp(errors, REPLACE) == 0) {
            strsize++;
        } else {
            char msg[256];
            sprintf(msg, "Character has no LAMCOUR equivalent: U+%04X",
                    (int)s[i]);
            PyErr_SetString(PyExc_UnicodeError, msg);
            return NULL;
        }
    }

    /* allocate memory for the result */
    string = malloc(sizeof(char) * (strsize + 1));
    string[strsize] = 0;

    /* i indexes the input string (s)
       j indexes the output string (string) */
    for (i = 0, j = 0; i < size;) {
        if (unicode_lookup((const Py_UNICODE *)(s+i),
                    (char *)&replacement, &deltai)) {
            string[j] = replacement;
            j++;
            i += deltai;
        } else if (errors != NULL && strcmp(errors, IGNORE) == 0) {
            i++;
        } else if (errors != NULL && strcmp(errors, REPLACE) == 0) {
            string[j] = LAMCOUR_REPLACE;
            i++;
            j++;
        }

        /* If an exception needed to be raised, it should have been done
         * before. */

    }

    /* allocate the python string, free resources, and return */
    pystring = PyString_FromStringAndSize(string, strsize);
    free(string);
    return pystring;
}

/****************************************************/
/* These are wrapper Python-interface functions for */
/* decode and encode above.                         */
/* o lamcour_decode wraps decode.                   */
/* o lamcour_encode wraps encode.                   */
/****************************************************/
static PyObject *lamcour_decode(PyObject *self, PyObject *args)
{
    const char *data;
    int size;
    const char *errors = NULL;

    if (!PyArg_ParseTuple(args, "t#|z:lamcour_decode",
                          &data, &size, &errors))
        return NULL;

    return codec_tuple(decode(data, size, errors), size);
}

static PyObject *lamcour_encode(PyObject *self, PyObject *args)
{
    PyObject *str, *v;
    Py_UNICODE *unistring;
    const char *errors = NULL;

    if (!PyArg_ParseTuple(args, "O|z:lamcour_encode",
                          &str, &errors))
        return NULL;

    str = PyUnicode_FromObject(str);
    if (str == NULL)
        return NULL;

    unistring = PyUnicode_AsUnicode(str);
    v = codec_tuple(encode(unistring,
                           PyUnicode_GET_SIZE(str),
                           errors),
                    PyUnicode_GET_SIZE(str));
    /*free(unistring);*/
    Py_DECREF(str);
    return v;
}

/****************************************************/
/* These define the Python inteface.                */
/****************************************************/
static PyMethodDef LamcourMethods[] = {
    {"decode", lamcour_decode, METH_VARARGS,
     "Creates a Unicode object by decoding a LAMCOUR-encoded string."},

    {"encode", lamcour_encode, METH_VARARGS,
     "Creates a string object by converting a Unicode object into\n"
     "a LAMCOUR-encoded string."},

    {NULL, NULL, 0, NULL}
};

void
init_lamcour(void)
{
    PyObject *m, *d;

    m = Py_InitModule("_lamcour", LamcourMethods);
    d = PyModule_GetDict(m);
    LamcourError = PyErr_NewException("lamcour.error", NULL, NULL);
    PyDict_SetItemString(d, "error", LamcourError);
}

