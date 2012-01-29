#!/usr/bin/python
#coding:utf-8
import os
import sys
import urllib
from os.path import dirname, abspath, join
from settings_local import conn_new, c_new_dict as c

sys.path.append("../casino_rating")
from utilites.funcs import generate_filename, get_file_extension

rel = lambda x: join(abspath(dirname(__file__)), x)    


def main():
    """
    Main function for run all processes
    """
    # _casino_logo()
    _casino_screenshots()
    
    # _slots_logo()


def _casino_logo():
    """
    Copy casino logo images
    """
    c.execute("""SELECT id, logo FROM old_site_casino c WHERE logo<>'' ORDER BY id ASC""")
    for item in c.fetchall():
        filename = copy_file("http://casino-rating.org/images/logos/%s.jpg" % item["logo"], "casino", "jpg")
        c.execute("""UPDATE old_site_casino SET logo=%s WHERE id=%s""", (filename, item["id"]))
    conn_new.commit()


def _casino_screenshots():
    """
    Copy casino screenshots
    """
    c.execute("""SELECT id, casino_id, image FROM old_site_casinoscreenshot WHERE image<>'' ORDER BY id ASC""")
    for item in c.fetchall():
        filename = copy_file("http://casino-rating.org/images/logos/%s" % item["image"], "casino", 
            get_file_extension(item["image"]))
        c.execute("""UPDATE old_site_casinoscreenshot SET image=%s WHERE id=%s""", (filename, item["id"]))
    conn_new.commit()


def _slots_logo():
    """
    Copy slots logo images
    """
    c.execute("""SELECT id, screenshot FROM casino_game WHERE screenshot<>'' ORDER BY id ASC""")
    for item in c.fetchall():
        filename = copy_file("http://casino-rating.org/%s" % item["screenshot"], "slots", 
            get_file_extension(item["screenshot"]))
        c.execute("""UPDATE casino_game SET screenshot=%s WHERE id=%s""", (filename, item["id"]))
    conn_new.commit()


def copy_file(url, folder, ext):
    """
    Copy file to new folder
    `url` - file URL
    dbpath` - needed folder for new file
    """
    f = urllib.urlopen(url)
    filename = generate_filename(folder, ext)
    fullpath = rel("../upload/%s" % filename)

    filedir = os.path.dirname(fullpath)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    nf = open(fullpath, "w+")
    nf.write(f.read())
    nf.close()
    return filename


q = sys.exit
if "__main__" == __name__:
    sys.exit(main())
