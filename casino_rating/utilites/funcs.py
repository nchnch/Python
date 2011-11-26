# coding: utf-8
"""
Some small and useful functions
"""
import Image
import hashlib
import os
import re
from os.path import join, abspath, dirname
from settings import MEDIA_ROOT, MEDIA_URL
from uuid import uuid4


def rel(*x):
    """Easy way to set setting paths"""
    return join(abspath(dirname(__file__)), *x)


def remove_html_tags(data):
    """Remove html tags from string"""
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def decimal_ceil(x):
    """math.ceil analog which works"""
    int_x = int(x)
    if x - int_x == 0:
        return int_x
    return int_x + 1


def to_utf8(string):
    """Convert to utf8"""
    return unicode(str(string), 'utf-8').encode('utf-8')


def objects_to_choices(queryset):
    """Get choices list from model queryset"""
    res = []
    for elm in queryset:
        res.append((elm.pk, unicode(elm)))
    return res


def value_from_list(key, values, by_first=False):
    """
    Get 0-index from collection of double tuples/lists by first key value
    print value_from_list(((1, "key1",), (2, "key2",), (3, "key3",),), "key2")
    will output:`2`
    """
    i, j = (1, 0,) if not by_first else (0, 1,)
    for elm in values:
        if elm[i] == key:
            return elm[j]
    return None


def get_md5(text):
    """MD5 function short name"""
    return hashlib.md5(text).hexdigest()


def generate_filename(base_folder, extension=None, filename=None, with_path=True, get_name=False, easy=False):
    """
    Generate unique filename with folder path.
    `with_path` - need folders in new path or no
    `get_name` - get only path or list which contents name and dir_name of new file
    """
    name = get_md5(str(uuid4()))
    if not extension:
        extension = get_file_extension(filename)
    extension = extension.lower()

    if with_path:
        if not easy:
            target = "%s/%s/%s/%s.%s" % (name[0], name[1], name[2], name, extension,)
        else:
            target = "%s/%s.%s" % (name[0], name, extension,)
        path = "%s/%s" % (base_folder.rstrip("/"), target, )
        return path if not get_name else (path, name, )
    else:
        return "%s/%s.%s" % (base_folder.rstrip("/"), name, extension)


def get_file_extension(filename):
    """Get extenstion of file"""
    if not filename:
        return ""
    dotpos = filename.rfind(".")
    return filename[dotpos+1:] if dotpos != -1 else ""


def easy_upload_path(instance, filename):
    """
    Generates easy(small folders) upload path for FileField
    """
    return generate_filename(instance.UPLOAD_DIR, get_file_extension(filename), easy=True) 


def make_upload_path(instance, filename):
    """
    Generates upload path for FileField
    """
    return generate_filename(instance.UPLOAD_DIR, get_file_extension(filename)) 