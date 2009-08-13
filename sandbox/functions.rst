XXX Link into the standard docs

Defining Functions and Using Built-Ins
======================================

Introduction
------------

Functions are the fundamental unit of work in Python. They're also
very easy to define and use. We will start with the basics of
functions. Then we will look at some other ways of defining
them. Lastly we look at using the builtin functions, which are the
core functions that don't require an explicit import.  importing them
into your namespace.

.. sidebar:: Function Code Bodies

  Jython, like CPython, only has one unit of compilation, the function
  code body. When a module is compiled, every function in it is
  compiled even if it's not ultimately bound to a name. In addition, a
  script or module is itself treated as a function when
  compiled. Almost always, these function definitions are compiled to
  Java bytecode, although future versions of Jython will support
  compilation to other formats.


Function Syntax and Basics
--------------------------

Functions are defined by using with ``def`` keyword, the name of the
function, its parameters (if any), and the body of code::

  def times2(n):
      return n * 2

Parameters, like variables in general in Python, are not typed. The
objects, which are passed by reference, are instead typed. Because the
``*`` operator means repeat for sequences (like strings and lists),
you can use the ``times2`` function as follows::

  >>> times2(4)
  8
  >>> times2('abc')
  'abcabc'
  >>> times2([1,2,3])
  [1, 2, 3, 1, 2, 3]

In addition, a given name can only be associated with one function at
a time, so function overloading is not possible just with using
``def``. If you were to define two (or more) functions with the same
name, the last one defined is used.

.. sidebar:: Function Metaprogramming

  However, it is possible to overload a function, or otherwise
  genericize it. You simply need to create a dispatcher function to do
  this on your behalf.

  XXX TurboGears uses this for it routing functionality (but they no
  longer use Peak-Rules as of 2.1 [which is hard to port to
  Jython]). Need to find out more!

An empty function -  can be written by using the ``pass`` statement::

  def do_nothing():
      pass

A function introduces a scope for new names, such as variables. Any
names that are created in the function are only visible within that
scope::

  XXX scope

(Example showing a syntax error...)

.. sidebar:: Global Variables

  global keyword - [Useful for certain circumstances, certainly not
  core/essential, much like nonlocal in Py3K, so let's not put too
  much focus on it.]

  The `global` keyword is used to declare that a variable name is from
  the module scope (or script) containing this function. Using
  `global` is rarely necessary in practice, since it is not necessary
  if the name is called as a function or an attribute is accessed
  (through dotted notation).

  This is a good example of where Python is providing a complex
  balancing between a complex idea - the lexical scoping of names, and
  the operations on them - and the fact that in practice it is doing
  the right thing.


.. sidebar:: Functions are Everywhere

  And nearly everything else is in terms of functions, even what are
  typically declarations in other languages like Java. For example, a
  class definition or module import is just syntax around the
  underlying functions, which you can call yourself if you need to do
  so. (They are type and __import__ respectively, you will be learning
  more about them later.)  ======


.. sidebar:: Recursion

  XXX Recursion. (I think it makes sense to not focus on recursion too
  much; it may be a fundamental of CS, but it's also rarely necessary
  for most end-user software development. So let's keep it in a
  sidebar.)  Demo Fibonacci, since this requires no explanation, and
  it's a non trivial use of recursion.

  Note that Jython, like CPython, is ultimately stack based [at least
  until we have some tail call optimization support in JVM]. Recursion
  can be useful for expressing an algorithm compactly, but deeply
  recursive solutions on Jython can exhaust the JVM stack.

   Memoization, as we will discuss with decorators, can make a
   recursive solution practical, however.

.. sidebar::

   The keyword def is not the only way to define a function
   lambda. Creates an unnamed function that does not require the use
   of whitespace.  generator expressions. Creates an unnamed
   generator. But cover this later with respect to generators.

   In addition, we can also create objects with classes whose instance
   objects look like ordinary functions.  Objects supporting the
   __call__ protocol. This should be covered in a later chapter.  For
   Java developers, this is familiar. Classes implement such
   single-method interfaces as Callable or Runnable.  Bound
   methods. Instead of calling x.a(), I can pass x.a as a parameter or
   bind to another name. Then I can invoke this name. The first
   parameter of the method will be passed the bound object, which in
   OO terms is the receiver of the method. This is a simple way of
   creating callbacks. (In Java you would have just passed the object
   of course, then having the callback invoke the appropriate method
   such as `call` or `run`.)  staticmethod, classmethod, descriptors
   functools, such as for partial construction Other function
   constructors, including yours?  =====

Calling functions is generally done by the familiar syntax. (But see
the sidebar for operators.) For example, for the function x with
parameters a,b,c that would be x(a,b,c). Unlike some other dynamic
languages like Ruby and Perl, the use of parentheses is required
syntax.

.. sidebar::

  Behind the scenes, this function application is compiled to
  x.__call__(a,b,c), and that's how it's called from Java. A
  convenience method is also provided, invoke, that combines method
  lookup and dispatch together. So you can directly call Python
  functions from Java code in this way. We will look at this more in
  the chapter on Java integration.

.. sidebar:: Special syntax support for operators

  x.a
  del x
  x[i]
  etc.

  All operators are available as functions from the operator module.
  It should be noted that operators on built-in types (int, str, dict,
  etc.) will usually execute faster on the JVM because they do not
  require dynamic dispatch. Invokedynamic, part of JDK 7, is exciting
  because it makes that cost go away, but we will have to wait for
  that. 

The code definition is separate from the name of the function.
This distinction proves to be useful for decorators, as we will see later.

Scoping
~~~~~~~

Functions create scopes for their variables.
Assigning a variable, just like in a simple script, implicitly

Note that you can introduce other namespaces into your function definition. So::

  def f():
      from NS import A, B

Functions can be nested.

Most importantly this allows the construction of closures.
Closures.

.. sidebar::

  Note that the function declarations are executable statements. So
  it's perfectly valid to write code like this::

    # write more interesting code
    if variant:
        def f():
            ###
     else:
        def f():
            ###

.. sidebar:: What do functions look like from Java?

  They are instances of PyObject, supporting the __call__ method.

  Additional introspection is available. If a function object is just
  a standard function written in Python, it will be of class
  PyFunction. A builtin function will be of class
  PyBuiltinFunction. But you can't assume that in your code, because
  many other objects support the function interface (__call__), and
  these potentially could be proxying, perhaps several layers deep, a
  given function. You can only assume it's a PyObject.

.. sidebar:: Functions are first-class objects

  The inspect module. Determining parameters, etc.
  One thing that is not supported: introspecting on code objects themselves.

.. sidebar:: Partitioning this global namespace with shadowing.

Decorators
----------

Functions on functions

Using Decorators
~~~~~~~~~~~~~~~~

Memoization decorator. For our same Fibonacci example.
How about a decorator for Java integration? eg add support of a given interface to facilitate callbacks

Creating Decorators
~~~~~~~~~~~~~~~~~~~

Using __future__
with_statement

Generators
----------

Generators are functions that implement Python's iterator protocol.

iter() - obj.__iter__
Call obj.next


Advance to the next point by calling the special method
``next``. Usually that's done implicitly, typically through a loop or
a consuming function that accepts iterators, including generators.

Defining Generators
~~~~~~~~~~~~~~~~~~~

A generator function consists of one or more yield points, which are
marked through the use of the keyword ``yield``. Unlike other
functions, you use the ``return`` statement only to say, "I'm done",
that is, to exit the generator.

Example code::

  XXX code

But it's not necessary to return. Many useful generators actually will
have an infinite loop around their yield expression::

  XXX while True:
     yield stuff


.. sidebar:: How it actually works

  Generators are actually compiled differently from other
  functions. Each yield point saves the state of unnamed local
  variables (Java temporaries) into the frame object, then returns the
  value to the function that had called ``next`` (or ``send`` in the
  case of a coroutine). The generator is then indefinitely suspended,
  just like any other iterator. Upon calling next again, the generator
  is resumed by restoring these variables, then executing the next
  bytecode instruction. This process continues until the generator is
  either garbage collected or it exits.

  You can determine if the underlying function is a generator if its
  code object has the CO_GENERATOR flag set in co_flags.

  Generators can also be resumed from any thread, although some care
  is necessary to ensure that underlying system state is shared (or
  compatible). We will explore how to use effectively use this
  capability in the chapter on concurrency.


Using Generators
~~~~~~~~~~~~~~~~

Python iteration protocol. iter, next.

Generator Example
~~~~~~~~~~~~~~~~~

How to use in interesting ways with Java. For example, we wrap everything in Java that supports Iterator so it supports the Python iteration protocol.

Maybe something simple like walking a directory tree?
In conjunction with glob type functionality? And possibly other analysis.
Maybe process every single file, etc.
That could be sort of cool, and something I don't think is so easy from Java (no, it's not).
Also we will want to wrap it up with RAII semantics too, to ensure closing.

Lastly - what sort of Java client code would want such an iterator? That's the other part of the equation to be solved here.
Maybe some sort of plugin?
Don't want to make the example too contrived.
Some relevant discussion here in a Java tutorial: http://java.sun.com/docs/books/tutorial/essential/io/walk.html

What about a simple Jar scanner? That's sort of handy... and feeds into other functionality too.
Could be the subject of Ant integration too. (Or Maven or Ivy, but perhaps this is going beyond my knowledge here.)

One common usage of a generator is to watch a log file for changes (tail -f). We can create something similar with the NIO package, although this does require the use of a thread for the watcher (but this of course can be multiplexed across multiple directories).

Watching a directory for changes. In CPython, this requires fcntl on Unix/Linux systems, and the use of a completely different Win32 API on Windows systems. http://stackoverflow.com/questions/182197/how-do-i-watch-a-file-for-changes-using-python Java provides a simple approach:
http://java.sun.com/docs/books/tutorial/essential/io/notification.html  - how to do it in Java


Generator Expressions
---------------------


Coroutines
----------

The PyCon tutorial on coroutines has some useful concepts. One thing to remember: coroutines do not mix with generators, despite being related in both syntax and implementation. Coroutines use push; generators use pull.
Might be nice to show how to use this in conjunction with parallelism.


Special Functions
[this is no doubt __XXX__ methods and corresponding generics like len, iter, etc]

Frames
Tracebacks
Profiling and tracing




Builtin Functions
-----------------

Builtin functions are those functions that are always in the Python
namespace. In other words, they are the only truly globally defined
names. As a result, they're somewhat like the classes from
``java.lang``. They 

Please refer to the documentation of the Python standard library [XXX
link to the Jython.org version] for the formal documentation of these
builtin functions.

Let's list these by functionality, that is

Constructor Functions
~~~~~~~~~~~~~~~~~~~~~

Constructor functions are used to create objects of a given type.

.. note:: 

  In Python, the type is a constructor function; there's no difference
  at all in Python. So you can use the ``type`` function, which we
  discuss momentarily, to look up the type of an object, then make
  instances of that same type.

First we will look at the constructor functions, which are more
typically used for conversion. This is because there is generally a
convenient literal syntax available, or in the case of ``bool``, there
are only two such constants, ``True`` and ``False``.

bool
chr
complex
dict
float
list
int
str
tuple
unichr
unicode 

.. note:: 

  So you should use ``42`` in your code instead of ``int('42')`` - and
  even then you still need to a string literal!

.. note:: 

  The function ``long`` is no longer necessary to use. This is because
  int has no restriction on its size.

Although there is a convenient literal for creating ``dict`` objects::

  a_dict = { 'alpha' : 1, 'beta' : 2, 'gamma' : 3 }

It can be more convenient to create them using the ``dict`` function::

  a_dict = dict(alpha=1, beta=2, gamma=3)

Of course in this latter case, the keys of the entries being created
must be valid Python keywords.

frozenset, set
object - use to create a unique object

Constructing iterators: iter, xrange

.. function:: iter(o[, sentinel])


list, long (*), object, open, property, set, slice,  super, tuple, type, - note, no buffer (but string is usually a reasonable sub)

file, open




Use as decorators:
classmethod, staticmethod, property

``slice`` is rarely used directly.

super
type - 3 arg form
compile


Math Builtin Functions
~~~~~~~~~~~~~~~~~~~~~~

Most math functions are defined in ``math`` (or ``cmath`` for complex math). These are functions that are builtin:

abs, cmp, divmod, pow, round

You may need to use named functions 

Functions on Iterables
~~~~~~~~~~~~~~~~~~~~~~

The next group of builtin functions operate on iterables, which in
Jython also includes all Java objects that implement the
``java.util.Interface``. (This extends to the related functions in the
functools and itertools modules.)

In particular,

.. function:: enumerate(iterable)

.. function:: zip([,iterable, ...])

The ``zip`` function creates a list of tuples by stepping through each
*iterable*. One very common idiom is to use ``zip`` to create a
``dict`` where one iterable has the keys, and the other the
values. This is often seen in working with CSV files (from a header
row) or database cursors (from the ``description``
attribute). However, you might want to consider using
``collections.namedtuple`` instead::

  XXX example code - read from CSV, zip together

 
.. function:: sorted(iterable[, cmp[, key[, reverse]]])

The ``sorted`` function returns a sorted list. Use the optional *key*
argument to specify a key function to control how it's sorted. So for
example, this will sort the list by the length of the elements in it::
  
  >>> sorted(['Massachusetts', 'Colorado', 'New York', 'California', 'Utah'], key=len)
  ['Utah', 'Colorado', 'New York', 'California', 'Massachusetts']

And this one will sort a list of Unicode strings without regard to it
whether the characters are upper or lowercase::

  >>> sorted(['apple', 'Cherry', 'banana'])
  ['Cherry', 'apple', 'banana']

  >>> sorted(['apple', 'Cherry', 'banana'], key=str.upper)
  ['apple', 'banana', 'Cherry']

Although using a *key* function requires building a decorated version
of the list to be sorted, in practice this uses substantially less
overhead than calling a *cmp* function on every comparison.

.. function:: all(iterable), any(iterable)

``all`` and ``any`` will also short cut, if possible.


and sum(iterable[, start=0]) are functions that you
will find frequent use for. 

.. function:: max(iterable[, key]) or max([, arg, ...][, key]); min(iterable[, key]) or min([, arg, ...][, key])

The ``max`` and ``min`` functions
take a *key* function as an optional argument.


Although ``filter``, ``map``, and ``reduce`` are still useful, their
use is largely superseded by using other functions, in conjunction
with generator expressions. The ``range`` function is still useful for
creating a list of a given sequence, but for portability eventualy to
Python 3.x, using ``list(xrange())`` instead is better.

Some advice:

 * Generator expressions (or list comprehensions) are easier to use than ``filter``.
 * Most interesting uses of ``reduce`` can be done with ``sum``. Anything more complex should likely be written as a generator.


XXX some extra stuff here:

.. function:: all(iterable)

Returns True if all of the elements in the iterable are true,
otherwise False and stop the iteration. (If the iterable is empty,
this function returns True).

.. function:: any(iterable)

Returns True if any of the elements in the iterable are true, stopping the iteration.
Otherwise returns False and stop the iteration. (If the iterable is empty,
this function returns True).

Returns True if any of the 

.. function:: enumerate(iterable)

.. function:: filter(function, iterable)


.. function:: sum(iterable[, start=0])

   XXX maybe show how to construct a count using bool


Namespace Functions
~~~~~~~~~~~~~~~~~~~
namespace - __import__, delattr, dir, getattr, locals, globals, hasattr, reload, setattr, vars

getattr

.. sidebar::
  
  Java dynamic integration. the supporting special method for getattr
  is __getattr__. When Jython code is compiled, it actually uses
  __getattr__ for implementing attribute lookup. So x.y.z is actually
  compiled to the equivalent chain of
  x.__getattr__('y').__getattr__('z'). Alternatively for more
  efficient Java integration, __findattr__ is supported. It returns
  null instead of throwing an AttributeError if the attribute is not
  part of a given object. But use __getattr__ if you are going to be
  chaining method calls together so as to maintain Python exception
  handling semantics.

  If the given Jython class implements a Java interface (or extends a
  Java class, but this is the less preferrable case in Jython as it is
  in Java in general), then Java code that uses such instances can
  statically bind method lookup.

  XXX [The Clamp project supports an alternate way of exposing Java
  interfaces, such that the interfaces are created from Jython
  code. I'm not so certain about this approach as a best practice
  however. Java interfaces in Java are quite precise with respect to
  interoperability. Other parts are useful, such as AOT compilation of
  Java proxies for Jython classes.]


compile, eval, exec
Creating code objects.

evaluation - eval, execfile, 
predicates - callable, isinstance, issubclass 
hex, oct, id, hash, ord, repr
len
input, rawinput

Just refer to the documentation on these:
deprecated functions - apply, buffer, coerce, intern ...

Operators





