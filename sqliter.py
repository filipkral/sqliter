"""Convenient API for Python sqlite3 module.

Recommended import statement: import sqliter as lt

Author: Filip Kral <contact at filipkral.com>, http://filipkral.com

License: LGPL v3
"""

import sqlite3 as lt

def version():
    """Return a 3-tuple indicating version of this module."""
    return (0,1,0)

Connection = lt.Connection

def q(sql, db):
    """Execute sql query on database path or connection db.

    Returns fetchall() result for select statements,
    returns result of cn.execute for anything else.

    Required:
    sql -- statement to execute
    db -- a connection object, or a path to a database

    Example:
    >>> q('CREATE TABLE tbl (ido INT PRIMARY KEY NOT NULL, nm VARCHAR(20));', con)
    >>> q("INSERT INTO tbl VALUES (%s, %s);" % (1,'\'Foo\''), con)
    """
    closeit = False
    cn = None
    cr = None
    if type(db) == lt.Connection:
        cn = db
    else:
        cn = lt.connect(db)
        closeit = True
    cr = cn.cursor()
    cr.execute(sql)
    cn.commit()
    ret = list(cr.fetchall())
    if closeit: cn.close()
    return ret

def sqstr(x, forcestr=False):
    """Return a string insertable in SQL queries from x if x is string/unicode,

    Required:
    retrun 'x' string otherwise.

    Optional:
    forcestr -- explicitly force conversion to string

    Example:
    >>> sqstr(1) # "1"
    >>> sqstr(1, True) # "'1'"
    >>> sqstr("1") # "'1'"
    """
    if forcestr or (type(x) in (str, unicode)):
        return str("'%s'" % (str(x).replace("'", r'\'')))
    else:
        return str(str(x).replace("'", r'\''))

def sqstrs(x, forcestr=False):
    """Convert iterable into an iterable of insertable strings.

    Required:
    x -- list, tuple, or other iterable

    Optional:
    forcestr -- either False, or a list of booleans indicating whether to
        force conversion to string or not for each element of x.

    Example:
    >>> sqrstrs((1,2,3, 'foo'))
    >>> sqrstrs((1,2,3, 'foo'), [False, False, True, True])
    >>> sqrstrs((1,2,3, 'foo'), [0, 0, 1, 1])
    """
    if forcestr == False:
        forcestr = [False] * len(x)
    return map(sqstr, x, forcestr)

def tables(db):
    """Return a list of table names in database or connection db."""
    return [i[0] for i in q("SELECT name FROM sqlite_master WHERE type='table';", db)]

def names(db, table):
    """Return a list of column names of table from database or connection db."""
    closeit = False
    if type(db) == lt.Connection:
        cn = db
        closeit = True
    else:
        cn = lt.connect(db)
    cr = cn.cursor()
    re = cr.execute("SELECT * FROM %s LIMIT 0" % (table))
    ret = [i[0] for i in re.description]
    if closeit: cn.close()
    return ret

def types(db, table):
    """Return a list of column types of table from database or connection db."""
    infos = q("PRAGMA table_info(%s);" % (table), db)
    return list([i[2] for i in infos])

def getRow(db, table, idcol, ido, cols='*'):
    """Return a row as tuple where idcol equals ido.

    Required:
    db -- path or a connection to a database to query
    table -- name of a table to query
    idcol -- column representing identifier (although technically any column)
    ido -- value of idcol for which to retrieve row(s)

    Optional:
    cols -- list of columns to retrieve (default is '*' for all)
    """
    qry = "SELECT %s FROM %s WHERE %s = %s" % (",".join(cols) if cols not in ['*', ['*'], ('*')] else '*', table, idcol, ido)
    ret = q(qry, db)
    return ret

def getRowD(db, table, idcol, ido, cols = '*'):
    """Get row as dictionary. Like getRow but row is returned as a dict."""
    if cols in ['*', ['*'], ('*')]:
        cols = names(db, table)
    rw = getRow(db, table, idcol, ido, cols = cols)[0]
    ret = dict(zip(cols, rw))
    return ret

def updateRow(db, table, idcol, ido, cols, vals, forcestr=False):
    """Update a row where column idcol equals ido with values vals

    Required:
    db -- path or a connection to a database to query
    table -- name of a table to query
    idcol -- column representing identifier (although technically any column)
    ido -- value of idcol for which to retrieve row(s)
    cols -- list of columns to update
    vals -- list of new values for columns cols

    Optional:
    forcestr -- either False, or a list of booleans indicating whether to
        force conversion to string or not for each element of vals.
    """
    wc = "%s = %s" % (idcol, sqstr(ido))
    valstr = sqstrs(vals, forcestr)
    assignments = ",".join([' = '.join(sqstrs(a)) for a in zip(cols, valstr)])
    qry = "UPDATE %s SET %s WHERE %s" % (table, assignments, wc) #FROM %s WHERE %s = %s" % (",".join(cols) if cols not in ['*', ['*']] else '*', table, idcol, ido)
    ret = q(qry, db)
    return ret

def insertRow(db, table, cols, vals, forcestr=False):
    """Insert a row into a table.

    Required:
    db -- path or a connection to a database to query
    table -- name of a table to query
    cols -- list of columns for which values will be inserted
    vals -- list of values for columns cols

    Optional:
    forcestr -- either False, or a list of booleans indicating whether to
        force conversion to string or not for each element of x.
    """
    insertcols = "(" + ",".join(map(str, cols)) + ")"
    insertvals = "(" + ",".join([sqstrs(a, forcestr) for a in vals]) + ")"
    qry = "INSERT INTO %s %s VALUES %s" % (table, insertcols, insertvals, wc)
    ret = q(qry, db)
    return ret


if __name__ == "__main__":

    dbpath = r'c:\temp\testdb.db'

    with lt.connect(dbpath) as con:
        ts = tables(con)
        if "node" in ts:
            q("DROP TABLE node", con)
        if "edge" in ts:
            q("DROP TABLE edge", con)
        q('CREATE TABLE node (IDO INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, XC INT NOT NULL, YC INT NOT NULL, LABEL INT, INS TEXT, OUTS TEXT);', con)
        q('CREATE TABLE edge (IDO INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, LABEL INT, STARTN INT, ENDN INT);', con)

        # insert some nodes and edges the sqlite3 way, faster then liter.q
        data_nodes = [(1, '', 0, 0, 0, '', '1'), (2, '', 0, 0, 0, '', ''), (3, '', 0, 0, 0, '', ''), (4, '', 0, 0, 0, '', ''), (5, '', 0, 0, 0, '', ''), (6, '', 0, 0, 0, '', '')]
        data_edges = [(1, '', 0, 1, 2), (2, '', 0, 1, 2), (3, '', 0, 1, 2), (4, '', 0, 1, 2), (5, '', 0, 1, 2), (6, '', 0, 1, 2)]
        for i in data_nodes:
            con.execute("INSERT INTO node VALUES (?, ?, ?, ?, ?, ?, ?);", i)
        for i in data_edges:
            con.execute('INSERT INTO edge VALUES (?, ?, ?, ?, ?);', i)
        con.commit()

        # insert some more nodes with individual sqliter.q calls
        data_nodes = [(7, '', 0, 0, 0, '', '1'), (8, '', 0, 0, 0, '', ''), (9, '', 0, 0, 0, '', ''), (10, '', 0, 0, 0, '', ''), (11, '', 0, 0, 0, '', ''), (12, '', 0, 0, 0, '', '')]
        data_edges = [(7, '', 0, 1, 2), (8, '', 0, 1, 2), (9, '', 0, 1, 2), (10, '', 0, 1, 2), (11, '', 0, 1, 2), (12, '', 0, 1, 2)]
        for i in data_nodes:
            q("INSERT INTO node VALUES (%s)" % ", ".join(sqstrs(i)), con)
        for i in data_edges:
            q("INSERT INTO edge VALUES (%s)" % ", ".join(sqstrs(i)), con)

    print q("SELECT * FROM edge", dbpath)

    names(dbpath, "node")
    types(dbpath, "node")

