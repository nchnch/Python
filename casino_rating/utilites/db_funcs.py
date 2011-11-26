#coding: utf-8
from MySQLdb import connect
from MySQLdb.cursors import DictCursor
from settings import DATABASES

db = DATABASES["default"]
conn = connect(user=db["USER"], passwd=db["PASSWORD"], db=db["NAME"], charset="utf8", cursorclass=DictCursor)


def db_select(query, params=None):
    """Do database query. Function for easy query do"""
    c = conn.cursor()
    # c.execute('SET NAMES utf8;')
    # c.execute('SET CHARACTER SET utf8;')
    # c.execute('SET character_set_connection=utf8;')
    result = False
    try:
        if not params:
            c.execute(query)
        else:
            c.execute(query, params)
        result = c.fetchall()
    except Exception, e:
        print "MyDBQuery error: ", e
        print "Query was: ", query % params if params else ""
    # try:
        # conn.close()
    # except Exception:
        # pass
    return result


def db_query(query, params=None, multi=False):
    """
    Function for non-select query
    """
    c = conn.cursor()
    # c.execute('SET NAMES utf8;')
    # c.execute('SET CHARACTER SET utf8;')
    # c.execute('SET character_set_connection=utf8;')
    result = False
    try:
        if params is None:
            result = c.execute(query)
        else:
            if multi:
                result = c.executemany(query, params)
            else:
                result = c.execute(query, params)
        conn.commit()
    except Exception, e:
        print "MyDBQuery error: ", e
        print "Query was: ", query
    # try:
        # conn.close()
    # except Exception:
        # pass
    return result


def tree_delete_node(table, row_id):
    """Delete node from nested sets tree"""
    c = conn.cursor()
    c.execute("""SELECT parent_id, `left`, `right`, tree_id, `level` FROM %s WHERE id=%s""" % (table, row_id))
    row = c.fetchone()
    c.execute("""DELETE FROM %s WHERE id=%s""" % (table, row_id))
    c.execute("""UPDATE %s SET `left`=`left`-2 WHERE `left`>%s AND tree_id=%s""" % (table, row["right"], row["tree_id"]))
    c.execute("""UPDATE %s SET `right`=`right`-2 WHERE `right`>%s AND tree_id=%s""" % (table, row["right"], row["tree_id"]))
    return True



