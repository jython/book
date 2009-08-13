.. -*- mode: rst -*-

Resources
http://www.jython.org/archive/21/docs/zxjdbc.html
http://www.informit.com/articles/article.aspx?p=26143&seqNum=3
http://www.ibm.com/developerworks/data/library/techarticle/dm-0404yang/

Document this as well for some major databases:
PostgreSQL driver connection - http://jdbc.postgresql.org/documentation/head/connect.html
Oracle - 
MySQL
DB2?
SQLServer?

That should suffice... there may even be a repository out there that
lists standard URLs. Certainly it's a function of good containers to
do this...


Meta - Stuff to cover:

transactions - never use autocommit of course (but perhaps there's an
exception for doing so); more importantly things like the isolation of
the transaction, also perhaps its durability

preparing a statement
existence query - return one row
paged queries
scrolling
bulk inserts/updates


exception mgmt - especially diagnosing various errors (maybe enhance too?)

what improvements can we make to zxJDBC in less than one month?
decimal, datetime, etc. should all translate
we need to have a protocol level
minimum - support jdbc 3, ideally optionally jdbc 4


Add this caveat to the chapter introducing zxJDBC at the beginning of ch 12:

Finally we will look at zxJDBC package, which is a standard part of
Jython since version 2.1 and complies with the Python 2.0 DBI
standard. zxJDBC can be an appropriate choice for simple one-off
scripts where database portabibility is not a concern. In addition,
it's (generally) necessary to use zxJDBC when writing a new dialect
for SQLAlchemy or Django. [But not strictly true: you can use pg8000,
a pure Python DBI driver, and of course write your own DBI
drivers. But please don't do that.] So knowing how zxJDBC works can
useful when working with these packages. However, it's too low level
for us to recommend for more general usage. Use SQLAlchemy or Django
if at all possible.

Finally, JDBC itself is also directly accessible, like any other Java
package from Jython. Simply use the java.sql package. In practice this
should be rarely necessary. [XXX But perhaps something about how we
can still look at the underlying JDBC connection and result sets, if
necessary?  and if so, how?] [XXX there was also an article on doing
this on IBM developer works if I'm not mistaken]

zxJDBC – Using Python’s DB API via JDBC
=======================================

Introduction to zxJDBC
----------------------

The zxJDBC package provides an easy-to-use Python wrapper around
JDBC. zxJDBC bridges two standards:

 * JDBC is the standard platform for database access in Java.
 * DBI is the standard database API for Python apps.

zxJDBC, part of Jython, provides a DBI 2.0 standard compliant
interface to JDBC. Over 200 drivers are available for JDBC [XXX
http://developers.sun.com/product/jdbc/drivers], and they all work
with zxJDBC. High performance drivers are available for all major
relational databases, including DB2, Derby, MySQL, Oracle, PostgreSQL,
SQLite, SQLServer, and Sybase. And drivers are also available for
non-relational and specialized databases too.

However, unlike JDBC, zxJDBC when used in the simplest way possible,
blocks SQL injection attacks, minimizes overhead, and avoids resource
exhaustion. In addition, zxJDBC defaults to using a transactional
model (when available), instead of autocommit.

First we will look at connections and cursors, which are the key
resources in working with zxJDBC, just like any other DBI
package. Then we will look at what you can do them with them, in terms
of typical queries and data manipulating transactions.

------

Note: examples in this section are for Jython 2.5.1 and later. Jython
2.5.1 introduced some simplifications for working with connections and
cursors. In addition, we assume PostgreSQL for most examples, using the world sample database (also available for MySQL). [XXX link that in]

XXX setup, including the specific jar and world database

We also look at Oracle, because there has been some additional support
for some of the functionality supported by Oracle, including reference
cursors.

XXX setup, including the specific jar and hr database

XXX setups for other systems?


Connections
-----------

A database connection is simply a resource object that manages access to the
database system. Because database resources are generally expensive
objects to allocate, and can be readily exhausted, it is important to
close them as soon as you're finished using them. Here's the best way
to create a database connection outside of a managed container::

  from __future__ import with_statement
  from com.ziclix.python.sql import zxJDBC

  # for example
  jdbc_url =  "jdbc:postgresql:test"
  username = "postgres"
  password = "jython25"
  driver = "org.postgresql.Driver"

  with zxJDBC.connect(jdbc_url, username, password, driver) as conn:
      do_something(conn)

If you're just doing from the command line, you still to connect as
before, but we will forego ensuring the connection is closed::

  XXX >>> code

Inside a container, like an app server, you should use JDNI to allocate the
resource. Generally the connection will be managed by a connection
pool:

  XXX code

(We will assume these two imports in the remaining code examples in this section.)

In both cases the ``with`` statement ensures that the connection is
immediately closed. The alternative is to use ``finally``::

  XXX code

.. sidebar::

  Connection pools help ensure for more robust operation, by providing
  for reuse of connections while ensuring the connections are in fact
  valid. Often naive code will hold a connection for a very long time,
  to avoid the overhead of creating a connection, and then go to the
  trouble of managing reconnecting in the event of a network or server
  failure. It's better to let that be managed by the connection pool
  infrastructure instead of reinventing it.

  All transactions, if supported, are done within the context of a
  connection. We will be discussing transactions further in the
  subsection on data modification, but this is the basic recipe:

More details
------------

XXX maybe move to the end of the section? yes, i think that will break
up the flow much less. So let's do that.

There are two ways to create database connections:

  * Direct creation. Standalone code, such as a script, will directly
    create a connection.

  * JNDI. Code managed by a container should use JNDI for connection
    creation. Such containers include GlassFish, JBoss, Tomcat,
    WebLogic, and WebSphere. Normally connections are pooled when run
    in this context and are associated with a given security context.

As with regular Java JDBC, t

Let's look at these in turn.

zxJDBC.connect


zxJDBC.lookup


In a managed container, you would use ``zxJDBC.locate`` instead of
``zxJDBC.connect``. If you have code that needs to run both inside and
outside containers, we recommend you use a factory to abstact this.

XXX sample code for factory

This lookup process does not require knowing the JDBC URL or the
driver factory class. These aspects, as well as possibly the user name
and password, are configured by the adminstrator of the container
using tools specific to that container.

XXX - say something about the naming convention here, specifically
java:/comp/env/jdbc/NAME; in a container the jndi name is jdbc/NAME,
where jdbc is a convention

Transaction isolation levels

[XXX - see http://java.sun.com/docs/books/tutorial/jdbc/basics/transactions.html]


Cursors
-------

Once you have a connection, you probably want to do something with
it. Because you can do multiple things within a transaction - query
one table, update another - you need one more resource, which is a
cursor. Creating a cursor is easy::

  with conn.cursor() as c:
      do_some_work(c)

Like connections, you want to ensure the resource is appropriately
closed. Of course if you are using Jython from the shell, there's
generally no need to worry about resource allocations. So you can just
do this to follow the shorter examples we will look at:

.. example::

   >>> c = conn.cursor()

Cursors represent a unit of work. The easiest way is to use the execute method::

   >>> XXX code select from the world database

If the statement is a database query - uses the select statement - then it will return a result set. The best way to work with that result set is to iterate over it::

   XXX code

Binding variables

XXX cursors also support prepare


The unit of work is a cursor. Let's now look at how to create and then use cursors.


Create a cursor with the cursor method on the connection:


(zxJDBC maps a cursor to a JDBC ResultSet.)




Resource Management
+++++++++++++++++++

You should always close connections. This is not only good practice
but absolutely essential in a managed container so as to avoid
exhausting the corresponding connection pool, which needs the
connections returned as soon as they are no longer in use. The
``with`` statement makes it easy:

.. example::

from __future__ import with_statement
from itertools import islice
from com.ziclix.python.sql import zxJDBC

# externalize
jdbc_url =  "jdbc:oracle:thin:@host:port:sid" [XXX generalize]
username = "world"
password = "world"
driver = "oracle.jdbc.driver.OracleDriver"

with zxJDBC.connect(jdbc_url, username, password, driver) as conn:
    with conn.cursor() as c:
        c.execute("select * from emp")
        for row in islice(c, 20):
            print row # let's redo this w/ namedtuple momentarily...



(Jython 2.5.0 requires using contextlib.closing; here's how that looks)

The older alternative is available. It's more verbose, and similar to
the Java code that would normally have to be written to ensure that
the resource is closed. Note that for backwards compatibility, certain
defaults have changed.

.. example:



Creating and Executing Queries
==============================

Here's how to write a query using zxJDBC::

  XXX code

Usually you will want to use binding variables in query statements::

  XXX code

Note that the qmark is always ``?`` in zxJDBC::

>>> XXX

What else?

.. sidebar::

   Ideally, never construct a query statement directly from user data. SQL
   injection attacks employ such construction as their attack vector.
   Even when not malicious, user data will often contain characters,
   such as quotation marks, that can cause the query to fail if not
   properly escaped. In all cases, it's important to scrub and
   then escape the user data before it's used in the query.

   XXX is there an escape or quoting function that can be used here? 


   One other consideration is that such queries will generally consume
   more resources unless the database statement cache is able to match
   it (if at all). 

   But there are two important exceptions to our recommendation:

   * SQL statement requirements. Bind variables cannot be used
     everywhere. However, specifics will depend on the database.

   * Ad hoc or unrepresentative queries. In databases like Oracle, the
     statement cache will cache the execution plan, without taking in
     account lopsided distributions of values that are indexed - but
     are known to the database if presented literally. In those cases,
     a more efficient execution plan will result if the value is put
     in the statement directly.

   However, even in these exceptional cases, it's imperative that any
   user data is fully scrubbed. A good solution is to use some sort of
   mapping table, either an internal dictionary or driven from the
   database itself. In certain cases, a carefully constructed regular
   expression may also work. Be careful.

Statement Templates

.. example::

   # include example from paper


In the past, building one-off SQL query template engines was common in
Python. It might still be popular, but rarely necessary - it's much
better to use tools like SQLAlchemy or, if it's specifically for
object-relational usage, Django. We will discuss both later.

due to unescaped usage.

Retrieving Data
===============





Iteration
=========

.. example::

   # exporting data as a CSV file

Older code often used `fetchall`. In addition, so-called static
cursors were used by default. This practice is not
recommended. Iteration will generally perform much better, and it does
not produce fragile code when used with large data sets.

Metadata about the Query
========================

c.description

Compare with cx_Oracle or pgsql - it would be nice if the datatype
that was provided (the constructor), instead of the numeric type -
make it so

name, type, display_size, internal_size, precision, scale, null_ok).

Also make certain isNullable is a boolean



Named Tuples
============


Data Modification Language
=================


Bulk Inserts, Updates, and Merges
---------------------------------
(what is best practice here)


=======================
 Data Type Integration
=======================

Unicode
Numbers
Dates and Times
XML
BLOBs

Reference Cursors

Databases like Oracle support reference cursors [XXX we may only
support Oracle, check zxJDBC source - of course we can also use
customization to support]. Such reference cursors can be created a
number of ways, but perhaps most easily with cursor expressions:


what about input/output variables?

DDL
===


Extensions
=========

Metadata, lots of metadata!
See PyExtendedCursor
(so how do I make one of these from jython source?)


Scrollable cursors

Cursors can support a more complex interaction than simple iteration,
through scrolling, and this is exposed by zxJDBC. For web
applications, this functionality is not at all useful. In others, it
is rarely seen. One possible use case is for modestly-scaled
applications with a Swing GUI.

[XXX describe more]

Customization


preExecute/postExecute
getRowId


And even more; see http://www.jython.org/archive/21/docs/zxjdbc.html which documents the range of this quite extensively.


History
+++++++

zxJDBC was contributed by Brian Zimmer, one-time lead committer for
Jython.
