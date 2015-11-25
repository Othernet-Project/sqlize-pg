=========
sqlize-pg
=========

Sqlize-pg is a SQL query builder for Python. It's main goals are:

- speed: because fast is good
- transparency: do not hide the true nature of SQL
- mutability: we should be able to mutate the query

This library is primarily developed for use with Postgresql and no efforts have
been invested into testing or using with other database backends.

Installation
============

Sqlize-pg can be installed using ``pip`` or ``easy_install`` as usual::

    pip install sqlize-pg


Introduction (quick tutorial)
=============================

This section will provide a brief introduction to sqlize-pg. The examples are all
doctested, so rest assured that they work as expected.

The basic concept is to instantiate an object representing some type of query,
optionally manipulate attributes on it to fine-tune the clauses, and finally
convert the query into SQL string by coercing it into string.

Note that the queries are meant to be used with placeholder values, and **no
quoting is performed by sqlize-pg**. The generated SQL strings are intended to be
used with ``psycopg2.extensions.cursor.execute()``, and similar methods.

A basic select looks like this::

    >>> import sqlize_pg as sql
    >>> q = sql.Select('*', sets='foo')

Note that we call tables 'sets' to avoid the clash with Python's ``from``
keyword.

To convert the query to SQL, we simply coerce it into a ``str``::

    >>> str(q)
    'SELECT * FROM foo;'

You can select multiple things::

    >>> str(sql.Select(['foo', 'bar'], sets='foo'))
    'SELECT foo, bar FROM foo;'

You can also select from mutliple tables::

    >>> str(sql.Select('*', sets=['foo', 'bar']))
    'SELECT * FROM foo , bar;'


If you want to restrict your select, all common clauses are available::

    >>> str(sql.Select('*', ['foo', 'bar'], where='a = %s', group='foo',
    ...                order='-bar', limit=10, offset=20))
    'SELECT * FROM foo , bar WHERE a = %s GROUP BY foo ORDER BY bar DESC LIMIT 10 OFFSET 20;'


So far it looks like a rather complicated way of writing SQL. The real power,
though, comes from the fact that every aspect of the query object can be
tweaked.::

    >>> q = sql.Select()
    >>> str(q)
    'SELECT *;'
    >>> q.what = 'foo'
    >>> q.sets = 'this'
    >>> q.sets.join('other', sql.INNER)
    <sqlize_pg.builder.From object at ...>
    >>> q.where = 'bar = %s'
    >>> q.limit = 2
    >>> str(q)
    'SELECT foo FROM this INNER JOIN other WHERE bar = %s LIMIT 2;'

Now let's take a look at individual clauses. 

The ``where`` attribute is represented by a ``sqlize_pg.builder.Where`` object,
which supports a few handy operators for adding conditions::

    >>> q = sql.Select()
    >>> q.where = 'foo = %s'
    >>> q.where &= 'bar = %s'
    >>> q.where |= 'foo = bar'
    >>> str(q)
    'SELECT * WHERE foo = %s AND bar = %s OR foo = bar;'

The ``&=`` and ``|=`` have method aliases. Main advantage is that methods are
chainable. The above example can be rewritten as::

    >>> q = sql.Select()
    >>> q.where = 'foo = %s'
    >>> q.where.and_('bar = %s').or_('foo = bar')
    <sqlize_pg.builder.Where object at ...>
    >>> str(q)
    'SELECT * WHERE foo = %s AND bar = %s OR foo = bar;'

Note the underscore. We can't use method names that look like built-in
operators.

The ``sets`` attribute is represented by a ``sqlize_pg.builder.From`` object. It
has a few utility methods which you can use to add and join other tables::

    >>> q = sql.Select()
    >>> q.sets = 'foo'
    >>> q.sets.append('bar')
    <sqlize_pg.builder.From object at ...>
    >>> str(q)
    'SELECT * FROM foo , bar;'

    >>> q = sql.Select()
    >>> q.sets = 'foo'
    >>> q.sets.join('bar', sql.NATURAL)
    <sqlize_pg.builder.From object at ...>
    >>> str(q)
    'SELECT * FROM foo NATURAL JOIN bar;'

There is no direct support for aggregates. Instead, you write raw SQL.::

    >>> q = sql.Select('COUNT(*) as count', sets='foo', group='bar')
    >>> str(q)
    'SELECT COUNT(*) as count FROM foo GROUP BY bar;'

This is intentional. We wanted sqlize-pg to be as true to SQL as possible, and not
get in your way.

Apart from selecting, sqlize-pg supports inserts, updates, deletion, and
replacement.

Inserts look like this::

    >>> q = sql.Insert('foo', '%s, %s, %s')
    >>> str(q)
    'INSERT INTO foo VALUES (%s, %s, %s);'

You can also specify columns::

    >>> q = sql.Insert('foo', '%s, %s, %s', ('foo', 'bar', 'baz'))
    >>> str(q)
    'INSERT INTO foo (foo, bar, baz) VALUES (%s, %s, %s);'

If you omit the values, the query will contain named placeholders::

    >>> q = sql.Insert('foo', cols=('foo', 'bar', 'baz'))
    >>> str(q)
    'INSERT INTO foo (foo, bar, baz) VALUES (:foo, :bar, :baz);'

Replacing is similar to inserting, but uses ``Replace`` class instead::

    >>> q = sql.Replace('foo', constraints=['id'], cols=['id', 'name'])
    >>> str(q)
    'INSERT INTO foo (id, name) VALUES (%(id)s, %(name)s) ON CONFLICT (id) DO UPDATE SET id = %(id)s, name = %(name)s;'

The update query looks like this::

    >>> q = sql.Update('foo', 'bar = %s', baz='%s')
    >>> str(q)
    'UPDATE foo SET baz = %s WHERE bar = %s;'

The second argument is the same as ``where`` in ``Select()``. It can be
modified after initialization::

    >>> q = sql.Update('foo', baz='%s')
    >>> q.where &= 'foo = %s'
    >>> q.where |= 'bar = %s'
    >>> str(q)
    'UPDATE foo SET baz = %s WHERE foo = %s OR bar = %s;'

Any keyword arguments passed to ``Update()`` will be converted to ``SET``
clauses.

Deleting rows can be accomplished using the ``Delete()`` class.::

    >>> q = sql.Delete('foo', 'bar = %s')
    >>> str(q)
    'DELETE FROM foo WHERE bar = %s;'

As with ``Update()``, the second argument is a ``where`` clause, and can be
manipulated.

More docs, please!
==================

Unfortunately, there are currently no docs apart from this introduction. I hope
that codebase is not too difficult to follow, though, so if you can't wait, you
can peek into the source files.

Comparison to other libraries
=============================

TODO

Reporting bugs
==============

Report all bugs and feature requests to our `issue tracker`_.


_issue tracker: https://github.com/Outernet-Project/sqlize-pg/issues
