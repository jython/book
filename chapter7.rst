Chapter 7: Modules and Packages
+++++++++++++++++++++++++++++++

Up until this chapter we have been looking at code at the level of the
interactive console and simple scripts. This works well for small examples, but
when your program gets larger, it becomes necessary to break programs up into
smaller units.  In Python, the basic building block for these units in larger
programs is the module. 

Imports For Re-Use
==================

Breaking code up into modules helps to organize large code bases. Modules can
be used to logically separate code that belongs together, making programs
easier to understand. Modules are helpful for creating libraries that can be
imported and used in different applications that share some functionality.
Jython's standard library comes with a large number of modules that can be used
in your programs right away.

Import Basics
=============

We'll start with a couple of definitions.  A *namespace* is a logical grouping of
unique identifiers.  In other words, a namespace is that set of names that can
be accessed from a given bit of code in your program.  For example, if you open
up a Jython prompt and type dir(), the names in the interpreters namespace will
be displayed.  ::

    >>> dir()
    ['__doc__', '__name__']

The interpreter namespace contains __doc__ and __name__.  __doc__ is empty in
this case, and __name__ contains the string '__main__'.  The __name__ property
contains the name of the module the code is running in or '__main__' if it is
running outside of a module. ::

    >>> __doc__
    >>> __name__
    '__main__'

Here is a silly file called breakfast.py: ::

    class Spam(object):

        def order(self, number):
            print "spam " * number

    def order_eggs(): 
        print " and eggs!"

    s = Spam()
    s.order(3)
    order_eggs()

Let's see what happens when we import breakfast: ::
    >>> import breakfast
    spam spam spam 
     and eggs!
    >>> dir()
    ['__doc__', '__name__', 'breakfast']

Checking the doc() after the import shows that breakfast has been added to the
top level namespace.  Notice that the act of importing actually executed the
code in breakfast.py.  In languages like Java, the import statement is strictly
a compiler directive that must occur at the top of the source file. In Jython,
the import statement is an expression that can occur anywhere in the source
file, and can even be conditionally executed.

As an example, a common idiom is to attempt to import something that may not be
there in a try block, and in the except block import a module that is known to
be there. ::

    >>> try:
    ...     from blah import foo
    ... except ImportError:
    ...     def foo():
    ...         return "hello from backup foo"
    ...
    >>> foo()
    'hello from backup foo'
    >>>

If a module named blah had existed, the definition of foo would have been taken
from there. Since no such module existed, foo was defined in the except block,
and when we called foo, the 'hello from backup foo' string was returned.

I should point out that dir() does not actually print out the entire namespace
for the top level of the interpreter.  There are a large number of names that
are ommitted since the dir() output would not be as useful.  The special
__builtin__ module can be imported to see the rest: ::

    >>> import __builtin__
    >>> dir(__builtin__)
    ['ArithmeticError', 'AssertionError', 'AttributeError', ...

Definitions
-----------

Here are some basic concepts that are needed to discuss imports in Jython.

Python Module
	A file containing Python definitions and statements which in turn define a namespace. The module
        name is the same as the file name with the suffix .py removed, so for example the Python file
        “foo.py” defines the module “foo”. 

Python Package
	A directory containing an __init__.py file and usually some Python modules which are said
        to be contained in the package. The __init__.py file is executed before any contained modules
        are imported.

Java Package
	Java packages organize Java classes into a namespace using nested directories. Java packages
        do not require an __init__.py file. Also unlike Python packages, Java packages are explicitly
        referenced in each Java file with a package directive at the top.

The Import Statement
--------------------

An Example Program
------------------

To have a reasonable discussion about modules and packages, it helps to have a
motivating example that is complex enough for discussion, but simple enough to
describe in a short space. I have chosen to show an application that takes
command line input that will then be used to search through the files in a
given directory for a given bit of text and list the files that match the input
in a swing window. ::

	chapter7/
		searchdir.py
		search/
			__init__.py
			walker.py
			scanner.py

The example contains one package: search, which is a package because it is a
directory containing the special __init__.py file.  In this case __init__.py is
empty and so only serves as a marker that search is a package . If __init__.py
contained code, it would be executed before any of its containing modules could
be imported.  Note that the directory chapter7 itself is not a package because
it does not contain an __init__.py. There are three modules in the example
program: searchdir, search.input and search.scanner. The code for this program
can be downloaded at XXX.

searchdir.py
~~~~~~~~~~~~ ::

    import search.scanner as scanner
    import sys

    help = """
    Usage: search.py directory terms...
    """

    args = sys.argv

    if args == None or len(args) < 2:
        print help
        exit()

    dir = args[1]
    terms = args[2:]
    scan = scanner.scan(dir, terms)
    scan.display()
    
    
scanner.py
----------::

    from search.walker import DirectoryWalker
    from javax.swing import JFrame, JTable, WindowConstants

    class ScanResults(object):
        def __init__(self):
            self.results = []

        def add(self, file, line):
            self.results.append((file, line))

        def display(self):
            colnames = ['file', 'line']
            table = JTable(self.results, colnames)
            frame = JFrame("%i Results" % len(self.results))
            frame.getContentPane().add(table)
            frame.size = 400, 300
            frame.defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE
            frame.visible = True

        def scan(dir, terms):
            results = ScanResults()
            for filename in DirectoryWalker(dir):
                for line in open(filename):
                    for term in terms:
                        if term in line:
                            results.add(filename,line)
            return results
            
walker.py
---------::

    import os

    class DirectoryWalker:
        # A forward iterator that traverses a directory tree. Adapted from an
        # example in the eff-bot library guide: os-path-walk-example-3.py

        def __init__(self, directory):
            self.stack = [directory]
            self.files = []
            self.index = 0

        def __getitem__(self, index):
            while 1:
                try:
                    file = self.files[self.index]
                    self.index = self.index + 1
                except IndexError:
                    # pop next directory from stack
                    self.directory = self.stack.pop()
                    self.files = os.listdir(self.directory)
                    self.index = 0
                else:
                    # got a filename
                    fullname = os.path.join(self.directory, file)
                    if (os.path.isdir(fullname) and not
                        os.path.islink(fullname)):
                            self.stack.append(fullname)
                    else:
                        return fullname


If you run searchdir.py on it's own directory like this:

Trying out the Example Code
---------------------------::

    $ jython scanner.py . terms


You  will get a swing table titled “5 Results” (possibly more if .class files
are matched).  Let's examine the import statements used in this program.  The
module searchdir contains two import statements:::

    import search.scanner as scanner
    import sys

The first imports the module “search.scannar” and renames the module “scannar”.
The second imports the builtin module “sys” and leaves the name as “sys”. The
module “search.scannar” has two import statements: ::

    from search.walker import DirectoryWalker
    from javax.swing import JFrame, JTable, WindowConstants

The first imports DirectoryWalker from the “search.walker” module.  Note that
we had to do this even though search.walker is in the same package as
search.scanner. The last import is interesting because it imports the java
classes like JFrame from the java package javax.swing. Jython makes this sort
of import look the same as other imports.  This simple example shows how you
can import code from different modules and packages to modularize your
programs.

Types of import statements
==========================

The import statement comes in a variety of forms that allow much finer control
over how importing brings named values into your current module.

Basic import Statements
----------------------- ::

    import module
    from module import submodule
    from . import submodule

I will discuss each of the import statement forms in turn starting with: ::

    import module

This most basic type of import imports a module directly. Unlike Java, this
form of import binds the leftmost module name, so If you import a nested module
like: ::

	import javax.swing.JFrame

You would need to refer to it as “javax.swing.JFrame” in your code.  In Java
this would have imported “JFrame”.


from import Statements
---------------------- ::

    from module import name

This form of import allows you to import modules, classes or functions nested
in other modules. This allows you to achieve the result that a typical Java
import gives. To get a JFrame in your Jython code you issue: ::

    from javax.swing import JFrame

You can also use the from style of import to import all of the names in a
module directly into your current module using a '*'. This form of import is
discouraged in the Python community, and is particularly troublesome when
importing from Java packages (in some cases it does not work, see chapter 10
for details) so you should avoid its use. It looks like this: ::

    from module import *

Relative import Statements
--------------------------

A new kind of import introduced in Python 2.5 is the explicit relative import.
These import statements use dots to indicate how far back you will walk from
the current nesting of modules, with one dot meaning the current module. ::

    from . import module
    from .. import module
    from .module import submodule
    from ..module import submodule

Even though this style of importing has just been introduced, its use is
discouraged. Explicit relative imports are a reaction to the demand for
implicit relative imports. If you look at the search.scanner package, you will
see the import statement: ::
 
    from search.walker import DirectoryWalker

Because search.walker sits in the same package as search.scanner, the import
statement could have been: ::

    from walker import DirectoryWalker

Some programmers like to use relative imports like this so that imports will
survive module restructuring, but these relative imports can be error prone
because of the possibility of name clashes. The new syntax provides an explicit
way to use relative imports, though they too are still discouraged. The import
statement above would look like this: ::

    from .walker import DirectoryWalker


Aliasing import Statements
--------------------------

Any of the above imports can add an "as" clause to change import a module but
give it a new name. ::

    import module as alias
    from module import submodule as alias
    from . import submodule as alias


This gives you enormous flexibility in your imports, so to go back to the
Jframe example, you could issue: ::

    import javax.swing.JFrame as Foo

And instantiate a JFrame object with a call to Foo(), something that would
surprise most Java developers coming to Jython.

Hiding Module Names
-------------------

Typically when a module is imported, all of the names in the module are
available to the importing module. There are a couple of ways to hide these
names from importing modules. Starting any name with an underscore (_) which is
the Python convention for marking names as private is the first way.  The
second way to hide module names is to define a list named __all__, which should
contain only those names that you wish to have your module to expose.  As an
example here is the value of __all__ at the top of Jython's os module: ::

    __all__ = ["altsep", "curdir", "pardir", "sep", "pathsep",
               "linesep", "defpath", "name", "path",
               "SEEK_SET", "SEEK_CUR", "SEEK_END"]
           
Note that you can add to __all__ inside of a module to expand the exposed names
of that module.  In fact, the os module in Jython does just this to
conditionally expose names based on the operating system that Jython is running
on.


Module Search Path, Compilation, and Loading
============================================

Compilation
-----------

Despite the popular belief that Jython is an “interpreted, not compiled”, in
reality all Jython code is turned into Java bytecodes before execution.  These
bytecodes are not always saved to disk, but when you see Jython execute any
code, even in an eval or an exec, you can be sure that bytecodes are getting
fed to the JVM. The sole exception to this that I know of is the experimental
pycimport module that I will describe in the section on sys.meta_path below,
which interprets CPython bytecodes instead of producing Java bytecodes.



Module search Path and Loading
------------------------------

Understanding the process of module search and loading is more complicated in
Jython than in either CPython or Java because Jython can search both Java's
CLASSPATH and Python's path. We'll start by looking at Python's path and
sys.path. When you issue an import, sys.path defines the path that Jython will
use to search for the name you are trying to import. The objects within the
sys.path list tell Jython where to search for modules. Most of these objects
point to directories, but there are a few special items that can be in sys.path
for Jython that are not just pointers to directories. Trying to import a file
that does not reside anywhere in the sys.path (and also cannot be found in the
CLASSPATH) raises an ImportError exception. Let's fire up a command line and
look at sys.path. ::

    >>> import sys
    >>> sys.path
    ['', '/Users/frank/jython/Lib', '__classpath__', '__pyclasspath__/',
    '/Users/frank/jython/Lib/site-packages']



The first blank entry ('') tells Jython to look in the current directory for
modules. The second entry points to Jython's Lib directory that contains the
core Jython modules. The third and forth entries are special markers that we
will discuss later, and the last points to the site-packages directory where
new libraries can be installed when you issue setuptools directives from Jython
(see Chapter XXX for more about setuptools).

Import Hooks
------------

To understand the way that Jython imports Java classes we have to understand a
bit about the Python import protocol.  I won't get into every detail, for that
you would want to look at PEP 302 .

Briefly, we first try any custom importers registered on sys.meta_path. If one
of them is capable of importing the requested module, allow that importer to
handle it. Next, we try each of the entries on sys.path. For each of these, we
find the first hook registered on sys.path_hooks that can handle the path
entry. If we find an import hook and it successfully imports the module, we
stop. If this did not work, we try the builtin import logic. If that also
fails, an ImportError is thrown. So let's look at Jython's path_hooks.


sys.path_hooks 
-------------- ::
  
    >>> import sys
    >>> sys.path_hooks
    [<type 'org.python.core.JavaImporter'>, <type 'zipimport.zipimporter'>,
    <type 'ClasspathPyImporter'>]

Each of these path_hooks entries specifies a path_hook that will attempt to
import special fies. JavaImporter, as it's name implies, allows the dynamic
loading of Java packages and classes that are specified at runtime.  For
example, if you want to include a jar at runtime you can execute the following
code, which will then get picked up by the JavaImporter hook the next time that
an import is attempted: ::

    >>> import sys
    >>> sys.path.append("/Users/frank/lib/mysql-connector-java-5.1.6.jar")
    >>> import com.mysql
    *sys-package-mgr*: processing new jar, '/Users/frank/lib/mysql-connector-java-5.1.6.jar'
    >>> dir(com.mysql)
    ['__name__', 'jdbc']

sys.meta_path
-------------

Adding entries to sys.meta_path allows you to add import behaviors that will
occur before any other import is attempted, even the default builtin importing
behavior.  This can be a very powerful tool, allowing you to do all sorts of
interesting things.  As an example, I will talk about an experimental module
that ships with Jython 2.5.  That module is pycimport.  If you start up jython
and issue: ::

    >>> import pycimport


Jython will start scanning for .pyc files in your path and if it finds one,
will use the .pyc file to load you module. .pyc files are the files that
CPython produces when it compiles Python source code. So, if you after you have
imported pycimport (which adds a hook to sys.meta_path) then issue: ::

    >>> import foo

Jython will scan your path for a file named foo.pyc, and if it finds one it
will import the foo module using the CPython bytecodes.  Here the code at the
bottom of pycimport.py that makes defines the MetaImporter and adds it to
sys.meta_path: ::

    class __MetaImporter(object):
        def __init__(self):
            self.__importers = {}
        def find_module(self, fullname, path):
            if __debugging__: print "MetaImporter.find_module(%s, %s)" % (
                repr(fullname), repr(path))
            for _path in sys.path:
                if _path not in self.__importers:
                    try:
                        self.__importers[_path] = __Importer(_path)
                    except:
                        self.__importers[_path] = None
                importer = self.__importers[_path]
                if importer is not None:
                    loader = importer.find_module(fullname, path)
                    if loader is not None:
                        return loader
            else:
                return None
    
    sys.meta_path.insert(0, __MetaImporter())
    
The find_module method calls into other parts of pycimport and looks for .pyc
files. If it finds one, it knows how to parse and execute those files and adds
the corresponding module to the runtime. Pretty cool eh?

Java Package Scanning
=====================

Although you can ask the Java SDK to give you a list of all of the packages
known to a ClassLoader using: ::

    java.lang.ClassLoader#getPackages()

there is no corresponding ::

    java.lang.Package#getClasses()

This is unfortunate for Jython, because Jython users expect to be able to
introspect they code they use in powerful ways. For example, users expect to be
able to call dir() on Java objects and packages to see what names they contain:
::

    >>> import java.util.zip
    >>> dir(java.util.zip)
    ['Adler32', 'CRC32', 'CheckedInputStream', 'CheckedOutputStream', 'Checksum', 'DataFormatException', 'Deflater', 'DeflaterOutputStream', 'GZIPInputStream', 'GZIPOutputStream', 'Inflater', 'InflaterInputStream', 'ZipEntry', 'ZipException', 'ZipFile', 'ZipInputStream', 'ZipOutputStream', '__name__']
    >>> dir(java.util.zip.ZipInputStream)
    ['__class__', '__delattr__', '__doc__', '__eq__', '__getattribute__', '__hash__', '__init__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__', 'available', 'class', 'close', 'closeEntry', 'equals', 'getClass', 'getNextEntry', 'hashCode', 'mark', 'markSupported', 'nextEntry', 'notify', 'notifyAll', 'read', 'reset', 'skip', 'toString', 'wait']


To make this sort of introspection possible in the face of merged namespaces
requires some major effort the first time that Jython is started (and when jars
or classes are added to Jython's path at runtime). If you have ever run a new
install of Jython before, you will recognize the evidence of this system at
work: ::

    *sys-package-mgr*: processing new jar, '/Users/frank/jython/jython.jar'
    *sys-package-mgr*: processing new jar, '/System/Library/Frameworks/JavaVM.framework/Versions/1.5.0/Classes/classes.jar'
    *sys-package-mgr*: processing new jar, '/System/Library/Frameworks/JavaVM.framework/Versions/1.5.0/Classes/ui.jar'
    *sys-package-mgr*: processing new jar, '/System/Library/Frameworks/JavaVM.framework/Versions/1.5.0/Classes/laf.jar'
    ...
    *sys-package-mgr*: processing new jar, '/System/Library/Frameworks/JavaVM.framework/Versions/1.5.0/Home/lib/ext/sunjce_provider.jar'
    *sys-package-mgr*: processing new jar, '/System/Library/Frameworks/JavaVM.framework/Versions/1.5.0/Home/lib/ext/sunpkcs11.jar'

This is Jython scanning all of the jar files that it can find to build an
internal representation of the package and classes available on your  JVM. This
has the unfortunate side effect of making the first startup on a new Jython
installation painfully slow.

How Jython Finds the Jars and Classes to scan
---------------------------------------------

There are two properties that Jython uses to find jars and classes. These
settings can be given to Jython using commandline settings or the registry (see
Chapter XXX). The two properties are: ::

    python.packages.paths
    python.packagse.directories

These properties are comma separated lists of further registry entries that
actually contain the values the scanner will use to build its listing. You
probably should not change these properties. The properties that get pointed to
by these properties are more interesting. The two that potentially make sense
to manipulate are: ::

    java.class.path
    java.ext.dirs


For the java.class.path property, entries are separated as the classpath is
separated on the operating system you are on (that is, ";" on Windows and ":"
on most other systems).  Each of these paths are checked for a .jar or .zip and
if they have these suffixes they will be scanned.

For the java.ext.dirs property, entries are separated in the same manner as
java.class.path, but these entries represent directories.  These directories
are searched for any files that end with .jar or .zip, and if any are found
they are scanned.

To control the jars that are scanned, you need to set the values for these
properties. There are a number of ways to set these property values, see
Chapter XXX for more.

If you only use full class imports, you can skip the package scanning
altogether. Set the system property python.cachedir.skip to true or(again) pass
in your own postProperties to turn it off. 

Python Modules and Packages vs. Java Packages
=============================================

The basic semantics of importing Python modules and packages versus the
semantics of importing Java packages into Jython differ in some important
respects that need to be kept carefully in mind.

sys.path
--------

When Jython tries to import a module, it will look in its sys.path in the
manner described in the previous section until it finds one. If the module it
finds represents a Python module or package, this import will display a “winner
take all” semantic. That is, the first python module or package that gets
imported blocks any other module or package that might subsequently get found
on any lookups. This means that if you have a module foo that contains only a
name bar early in the sys.path, and then another module also called foo that
only contains a name baz, then executing “import foo” will only give you
foo.bar and not foo.baz.

This differs from the case when Jython is importing Java packages. If you have
a Java package org.foo containing bar, and a Java package org.foo containing
baz later in the path, executing “import org.foo” will merge the two namespaces
so that you will get both org.foo.bar and org.foo.baz.

Just as important to keep in mind, if there is a Python module or package of a
particular name in your path that conflicts with a Java package in your path
this will also have a winner take all effect.  If the Java package is first in
the path, then that name will be bound to the merged Java packages.  If the
Python module or package wins, no further searching will take place, so the
Java packages with the clashing names will never be found.


Naming Python Modules and Packages ----------------------------------

Developers coming from Java will often make the mistake of modeling their
Jython package structure the same way that they model Java packages. Do not do
this. The reverse url convention of Java is a great, I would even say a
brilliant convention for Java. It works very well indeed in the world of Java
where these namespaces are merged. In the Python world however, where modules
and packages display the winner take all semantic, this is a disastrous way to
organize your code.

If you adopt this style for Python, say you are coming from “acme.com” so you
would set up a package structure like “com.acme”. If you try to use a library
from your vendor xyz that is set up as “com.xyz”, then the first of these on
your path will take the “com” namespace, and you will not be able to see the
other set of packages.


Proper Python Naming --------------------

The Python convention is to keep namespaces as shallow as you can, and make
your top level namespace reasonably unique, whether it be a module or a
package. In the case of acme and company xyz above, you might start you package
structures with “acme” and “xyz” if you wanted to have these entire codebases
under one namespace (not necessarily the right way to go – better to organize
by product instead of by organization, as a general rule).

Note: There are at least two sets of names that are particularly bad choices
for naming modules or packages in Jython. The first is any top level domain
like org, com, net, us, name. The second is any of the domains that Java the
language has reserved for its top level namespaces: java, javax.

Java Import Example
-------------------

We'll start with a Java class which is on the CLASSPATH when Jython is started: ::

    package com.foo;
    public class HelloWorld {
        public void hello() {
            System.out.println("Hello World!");
        }
        public void hello(String name) {
            System.out.printf("Hello %s!", name);
        }
    }

Here we manipulate that class from the Jython interactive interpreter: ::

    >>> from com.foo import HelloWorld
    >>> h = HelloWorld()
    >>> h.hello()
    Hello World!
    >>> h.hello("frank")
    Hello frank!

It's important to note that, because the HelloWorld program is located on the
Java CLASSPATH, it did not go through the sys.path process we talked about
before. In this case the Java class gets loaded directly by the ClassLoader.
Discussions of Java ClassLoaders are beyond the scope of this book.  To read
more about ClassLoader see (citation? Perhaps point to the Java Language
Specification section)

Conclusion
==========

In this chapter we have learned how to divide code up into modules to for the
purpose of organization and re-use.  We have learned how to write modules and
packages, and how the Jython system interacts with Java classes and packages.
This ends Part I.  We have now covered the basics of the Jython language and
are now ready to learn how to use Jython.


