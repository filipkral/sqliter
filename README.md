sqliter
=======
Convenient API for sqlite3 - wrapper functions, helper functions, and aliases that make basic access to SQLite databases even easier than it is with sqlite3 module.

How to use?
-----------

    import sqliter as lt
    lt.version()


Installation
------------
Download this repository, put its contents somewhere into python path, then:

    import sqliter as lt

If you do not want to put it into your python path, then:

    sqliterpath = "c:\\path\\to\directory\\contating_sqliter_py"
    import sys
    sys.path.insert(0, sqliterpath)
    import sqliterpath as lt

Resources
---------
- Each function in arcapi has a decent docstring.
- Examples are in the body of sqliter.py below line `if __name__ == "__main__":`
- List all functions and their documentation: `help(lt)`


Dependencies
------------
[sqlite3](http://docs.python.org/2/library/sqlite3.html) - normally installed with Python


Tests
-----
Please write any tests into the body of sqliter.py below line  `if __name__ == "__main__":`


Issues
------
Feel free to submit issues and enhancement requests.


Contributing
------------
We welcome contributions from anyone and everyone.
If you feel you have made significant contribution anywhere in sqliter files,
please add yourself to the authors at the top of sqliter.


License
-------
[LGPL v3](https://github.com/filipkral/sqliter/blob/master/LICENSE)
