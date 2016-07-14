# coding: utf-8
import os
import gc
import shutil
import logging
from tempfile import mkdtemp
from hashlib import sha1
from normality import slugify

from aleph.text import string_value

log = logging.getLogger(__name__)


def checksum(filename):
    """Generate a hash for a given file name."""
    hash = sha1()
    with open(filename, 'rb') as fh:
        while True:
            block = fh.read(2 ** 10)
            if not block:
                break
            hash.update(block)
    return hash.hexdigest()


def make_filename(file_name, sep='-'):
    if file_name is not None:
        file_name = os.path.basename(file_name)
        slugs = [slugify(s, sep=sep) for s in file_name.rsplit('.', 1)]
        slugs = [s[:200] for s in slugs if s is not None]
        file_name = '.'.join(slugs)
        file_name = file_name.strip('.').strip(sep)
    return file_name


def make_tempdir(name=None):
    name = string_value(name) or 'data'
    path = os.path.join(mkdtemp(), name)
    os.makedirs(path)
    return path


def remove_tempdir(path):
    if path is not None and os.path.exists(path):
        shutil.rmtree(os.path.join(path, '..'))


def make_tempfile(name=None, suffix=None):
    name = string_value(name) or 'data'
    suffix = string_value(suffix)
    if suffix is not None:
        name = '%s.%s' % (name, suffix.strip('.'))
    return os.path.join(make_tempdir(), name)


def remove_tempfile(path):
    if path is None:
        return
    remove_tempdir(os.path.dirname(path))


def find_subclasses(cls):
    # https://stackoverflow.com/questions/8956928
    all_refs = gc.get_referrers(cls)
    results = []
    for o in all_refs:
        if (isinstance(o, tuple) and getattr(o[0], "__mro__", None) is o):
            results.append(o[0])
    return results
