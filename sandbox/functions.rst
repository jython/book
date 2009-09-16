XXX Link into the standard docs

XXX ensure PSF license is incorporated in our book, much of the text of this chapter is the description of the builtin functions

Defining Functions and Using Built-Ins
======================================

Introduction
------------

Functions are the fundamental unit of work in Python. In this chapter,
we will start with the basics of functions. Then we look at using the
builtin functions. These are the core functions that are always
available, meaning they don't require an explicit import into your
namespace.

Next we will look at some alternative ways of defining functions, such as
lambdas and classes. We will also look at more advanced types of
functions, namely closures and generator functions.

As you will see, functions are very easy to define and use. Python
encourages an incremental style of development that you can leverage
when writing functions.

So how does this work out in practice? Often when writing a function
it may make sense to start with a sequence of statements and just try
it out in a console. Or maybe just write a short script in an
editor. The idea is to just to prove a path and answer such questions
as, "Does this API work in the way I expect?"  Because top-level code in
a console or script works just like it does in a function, it's easy
to later isolate this code in a function body and then package it as a
function, maybe in a libary, or as a method as part of a class. The
ease of doing this style of development is one aspect that makes
Python such a joy to program in. And of course in the Jython
implementation, it's easy to do that within the context of any Java
library.

.. note:: 

  Perhaps the only tricky part is to keep the whitespace consistent as
  you change the identation level. The key then is to use a good editor
  that supports Python.

And nearly everything else is in terms of functions, even what are
typically declarations in other languages like Java. For example, a
class definition or module import is just syntax around the underlying
functions, which you can call yourself if you need to do
so. (Incidentally, these functions are ``type`` and ``__import__``
respectively, and you will be learning more about them later in the
sections on builtins.)

XXX Functions are first-class objects XXX incorporate



Function Syntax and Basics
--------------------------

Functions are usually defined by using the :keyword:`def` keyword, the name
of the function, its parameters (if any), and the body of code. We
will start by looking at this example function::

  def times2(n):
      return n * 2

Normal usage can treat function definitions as being very simple. But
there's subtle power in every piece of the function definition, due to
the fact that Python is a dynamic language. We look at these pieces
from both a simple (the more typical case) and a more advanced
perspective.

We will also look at some alternative ways of creating functions in a
later section.


The :keyword:`def` Keyword
~~~~~~~~~~~~~~~~~~~

Using :keyword:`def` for *define* seems simple enough, and this keyword
certainly can be used to declare a function just like you would in a
static language. You should write most code that way in fact.

However, the more advanced usage is that a function definition can
occur at any level in your code and be introduced at any time. Unlike
the case in a language like C or Java, function definitions are not
declarations. Instead they are *executable statements*. You can nest
functions, and we'll describe that more when we talk about nested
scopes. And you can do things like conditionally define them.

This means it's perfectly valid to write code like this::

    if variant:
        def f():
            print "One way"
     else:
        def f():
            print "or another"

Please note, regardless of when and where the definition occurs,
including its variants as above, the function definition will be
compiled into a function object at the same time as the rest of the
module or script that the function is defined in.


Naming the Function
~~~~~~~~~~~~~~~~~~~

We will describe this more in a later section, but the ``dir`` builtin
function will tell us abou the names defined in a given namespace,
defaulting to the module, script, or console environment we are
working in. With this new ``times2`` function defined above, we now
see the following (at least) in the console namespace::

  >>> dir()
  ['__doc__', '__name__', 'times2']

We can also just look at what is bound to that name::

  >>> times2
  <function times2 at 0x1>

(This object is further introspectable. Try ``dir(times2)`` and go
from there.)

We can also redefine a function at any time::

  >>> def f(): print "Hello, world"
  ... 
  >>> def f(): print "Hi, world"
  ... 
  >>> f()
  Hi, world

This is true not just of running it from the console, but any module
or script. The original version of the function object will persist
until it's no longer referenced, at which point it will be ultimately
be garbage collected. In this case, the only reference was the name
``f``, so it became available for GC immediately upon rebind.

What's important here is that we simply rebound the name.  First it
pointed to one function object, then another. We can see that in
action by simply setting another name (equivalently, a variable) to
``times2``::

  >>> t2 = times2
  >>> t2(5)
  10

This makes passing a function as a parameter very easy, for a callback
for example. But first, we need to look at function parameters in more
detail.

.. sidebar:: Function Metaprogramming

  A given name can only be associated with one function at a time, so
  can't overload a function with multiple definitions. If you were to
  define two or more functions with the same name, the last one
  defined is used, as we saw.

  However, it is possible to overload a function, or otherwise
  genericize it. You simply need to create a dispatcher function that
  then dispatches to your set of corresponding functions.


Function Parameters and Calling Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When defining a function, you specify the parameters it
takes. Typically you will see something like the following. The syntax
is familar::

  XXX def f(a, b, c)

Often defaults are specified::

  XXXX def f(a, b=1, c=None)

With this being the general form of what it take::

  XXX what's a clear way to describe this? probably from the python tutorial or ref
  def f(param1[=default1], *args, **kwargs)

.. note:: 

  This is not exhaustive. You can also use tuple parameters, but in
  practice, they are not typically used, and were removed in Python
  3. We recommend you don't use them. For one thing, they cannot be
  properly introspected from Jython.

Calling a function is symmetric. 
You can call a function. The parentheses are mandatory. 

Calling functions is also done by with a familiar syntax. For example,
for the function x with parameters ``a,b,c`` that would be
x(a,b,c). Unlike some other dynamic languages like Ruby and Perl, the
use of parentheses is required syntax (due the function name being
just like any other name).

Objects are strongly typed, as we have seen. But function parameters,
like names in general in Python, are not typed.  This means that
any parameter can refer to any type of object.

We see this play out in the ``times2`` function. The ``*`` operator
not only means multiply for numbers, it also means repeat for
sequences (like strings and lists).  So you can use the ``times2``
function as follows::

  >>> times2(4)
  8
  >>> times2('abc')
  'abcabc'
  >>> times2([1,2,3])
  [1, 2, 3, 1, 2, 3]

All parameters in Python are passed by reference. This is identical to
how Java does it with object parameters. However, while Java does
support passing unboxed primitive types by value, there are no such
entities in Python. Everything is an object in Python.

Functions are objects too, and they can be passed as parameters::

  XXX passing a function as a parameter - We can simply pass its name, then in the function using it

If you have more than two or so arguments, it often makes more sense
to call a function by parameter, rather than by the defined
order. This tends to create more robust code. So if you have a
function ``draw_point(x,y)``, you might want to call it as
``draw_point(x=10,y=20)``.

Defaults further simplify calling a function. You use the form of
``param=default_value`` when defining the function. For instance, you
might take our ``times2`` function and generalize it::

  def times_by(n, by=2):
      return n * by

This function is equivalent to ``times2`` when called using that
default value.

There's one point to remember that oftens trips up developers. The
default value is initialized exactly once, when the function is
defined. That's certainly fine for immutable values like numbers,
strings, tuples, frozensets, and similar objects. But you need to
ensure that if the default value is mutable, that it's being used in
this fashion correctly. So a dictionary for a shared cache makes
sense. But this mechanism won't work for but a list where we expect it
is initialized to an empty list upon invocation. If you're doing that,
you need to write that explicitly in your code.

Lastly, a function can take an unspecified number of ordered
arguments, through ``*args``, and keyword args, through
``**kwargs``. These parameter names (``args`` and ``kwargs``) are conventional, so you can use whatever name makes sense for your function. The markers ``*`` and ``**`` are used to to determine that this functionality should be used.

  XXX by factors



Calling Functions - Recursion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The code definition is separate from the name of the function.
This distinction proves to be useful for decorators, as we will see later.

  XXX Recursion. (I think it makes sense to not focus on recursion too
  much; it may be a fundamental aspect of computer science, but it's
  also rarely necessary for most end-user software development. So
  let's keep it in a sidebar.)  Demo Fibonacci, since this requires no
  explanation, and it's a non trivial use of recursion.

  Note that Jython, like CPython, is ultimately stack based [at least
  until we have some tail call optimization support in JVM]. Recursion
  can be useful for expressing an algorithm compactly, but deeply
  recursive solutions on Jython can exhaust the JVM stack.

   Memoization, as we will discuss with decorators, can make a
   recursive solution practical, however.


Function Body
~~~~~~~~~~~~~

Documenting Functions
^^^^^^^^^^^^^^^^^^^^^

First, you should specify a document string for the function. The
docstring, if it exists, is a string that occurs as the first value of
the function body::

   def times2(n):
       """Given n, returns n * 2"""
       return n * 2

By convention, use triple-quoted strings, even if your docstring is
not multiline. If it is multiline, this is how we recommend you format it::

   def fact(n):
       """Returns the factorial of n

       Computes the factorial of n recursively. Does not check its
       arguments if nonnegative integer or if would stack
       overflow. Use with care! 
       """

       if n in (0, 1):
           return 1
       else:
           return n * fact(n - 1)

Any such docstring, but with leading indendetation stripped, becomes
the ``__doc__`` attribute of that function object. Incidentally,
docstrings are also used for modules and classes, and they work
exactly the same way.

You can now use the ``help`` built-in function to get the docstring,
or see them from various IDEs like PyDev for Eclipse and nbPython for
NetBeans as part of the auto-complete::

  XXX help(fact)

Returning Values
^^^^^^^^^^^^^^^^

All functions return some value.

 In
``times2``, we use the ``return`` statement to exit the function with
that value.

Functions can easily return multiple values at once by returning a tuple or
other structure::

  XXX especially show the construct return x, y - this is an elegant way to do multiple values

A function can return at any time::

  XXX

And it can also return any object as its value. So you can have a
function that looks like this::

  XXX think of an interesting, simple function that returns different values based on input

 If a return statement is not used, the value ``None`` is returned. There is no
equivalent to a ``void`` method in Java, because every function in Python
returns a value. However, the Python console will not show the return
value when it's ``None``, so you need to explicitly print it to see
what is returned::

   >>> do_nothing()
   >>> print do_nothing()
   None

A delighter in Python is the ease by which it enables returning multiple values::

  XXX function - return a, b

We can then readily unpack the return value.


Introducing Variables
^^^^^^^^^^^^^^^^^^^^^

XXX local variables - extend this with discussion 
XXX global variables

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
  
  XXX rewrite above, confusing


Functions create scopes for their variables.
Assigning a variable, just like in a simple script, implicitly


Other Statements
^^^^^^^^^^^^^^^^

.. sidebar:: Acceptable Statements
 
  So what can go in a function body? Pretty much any statement,
  including material that we will cover later in this book. So you can
  define functions or classes or use even import, within the scope of
  that function.

  In particular, performing a potentially expensive operation like
  import as last as possible, can reduce the startup time of your
  app. It's even possible it will be never needed too.

  There are a couple of exceptions to this rule. In both cases, these
  statements must go at the beginning of a module, similar to what we
  see in a static language like Java:

    * Compiler directives. Python supports a limited set of compiler
      directives that have the provocative syntax of ``from __future__
      import X``; see :pep:`236`. These are features that will be
      eventually be made available, generally in the next minor
      revision (such as 2.5 to 2.6). In addition, it's a popular place
      to put Easter eggs, such as ``from __future__ import
      braces``. (Try it in the console, which also relaxes what it
      means to be performed at the beginning.)

    * Source encoding declaration. Although technically not a
      statement -- it's in a specially parsed comment -- this must go
      in the first or second line.


Empty Functions
^^^^^^^^^^^^^^^

An empty function still needs something in its body. You can use the
``pass`` statement::

  def do_nothing():
      pass # here's how to specify an empty body of code

Or you can just have a docstring for the function body::

  def empty_callback(*args, **kwargs):
      """Use this function where we need to supply a callback,
         but have nothing further to do.
      """

Why have a function that does nothing? As in math, it's useful to have
an operation that stands for doing nothing, like "add zero" or
"multiply by one". These identity functions eliminate special
cases. Likewise, as see with ``empty_callback``, we may need to
specify a callback function when calling an API, but nothing actually
needs to be done. By passing in an empty function -- or having this be
the default -- we can simplify the API.




Miscellaneous
^^^^^^^^^^^^^

XXX various limits
XXX currently limits of 64K java bytecode instructions when compiled. this will be relaxed in a future version

.. sidebar:: What do functions look like from Java?

  They are instances of PyObject, supporting the ``__call__`` method.

  Additional introspection is available. If a function object is just
  a standard function written in Python, it will be of class
  PyFunction. A builtin function will be of class
  PyBuiltinFunction. But don't assume that in your code, because many
  other objects support the function interface (``__call__``), and
  these potentially could be proxying, perhaps several layers deep, a
  given function. You can only assume it's a PyObject.


Builtin Functions
-----------------

Builtin functions are those functions that are always in the Python
namespace. In other words, these functions -- and builtin exceptions,
boolean values, and some other objects -- are the only truly globally
defined names. If you are familiar with Java, they are somewhat like
the classes from ``java.lang``.

Builtins are rarely sufficient, however; even a simple command line
script generally needs to parse its arguments or read in from its
standard input. So for this case you would need to ``import sys``. And
in the context of Jython, you will need to import the relevant Java
classes you are using, perhaps with ``import java``. But the
builtin functions are really the core function that almost all Python
code uses.

.. include:: builtins.rst

XXX let's just pull in the actual documentation, then modify/augment
as desired. I still prefer the grouping that we are doing here,
especially if we can create an index.

XXX Let's list these by functionality, that is 
Group by functionality; this is the standard docs, augmented by our
perspectives on how to use them.


Alternative Ways to Define Functions
------------------------------------

The :keyword:`def` keyword is not the only way to define a function. Here are
some alternatives:

   * :keyword:`lambda` functions. The :keyword:`lambda` keyword creates an unnamed
     function. Some people like this because it requires minimal
     space, especially when used in a callback::

     XXX lambda in a keyed sort, maybe combine last name, first name?

     XXX gen exp ex

   * Classes. In addition, we can also create objects with classes
     whose instance objects look like ordinary functions.  Objects
     supporting the __call__ protocol. This should be covered in a
     later chapter.  For Java developers, this is familiar. Classes
     implement such single-method interfaces as Callable or Runnable.
     
   * Bound methods. Instead of calling x.a(), I can pass x.a as a
     parameter or bind to another name. Then I can invoke this
     name. The first parameter of the method will be passed the bound
     object, which in OO terms is the receiver of the method. This is
     a simple way of creating callbacks. (In Java you would have just
     passed the object of course, then having the callback invoke the
     appropriate method such as `call` or `run`.)

   * staticmethod, classmethod, descriptors functools, such as for
     partial construction.

   * Other function constructors, including yours?



Lambda Functions
~~~~~~~~~~~~~~~~

Limitations.


Generator Functions
-------------------

Generators are functions that construct objects implementing Python's
iterator protocol.

iter() - obj.__iter__
Call obj.next


Advance to the next point by calling the special method
``next``. Usually that's done implicitly, typically through a loop or
a consuming function that accepts iterators, including generators.


Defining Generators
^^^^^^^^^^^^^^^^^^^

A generator function is written so that it consists of one or more
yield points, which are marked through the use of the keyword
``yield``::

  def g():
      print "before yield point 1"
      yield 1
      print "after 1, before 2"
      yield 2
      yield 3

If the ``yield`` keyword is seen in the scope of a function, it's
compiled as if it's a generator function.

Unlike other functions, you use the ``return`` statement only to say,
"I'm done", that is, to exit the generator::

  XXX code

You can't return an argument::

  def g():
      yield 1
      yield 2
      return None

  for i in g():
      print i
  
  SyntaxError: 'return' with argument inside generator

But it's not necessary to explicitly return. You can think of
``return`` as acting like a ``break`` in a for-loop or while-loop.

Many useful generators actually will have an infinite loop around
their yield expression, instead of ever exiting, explicitly or not::

  XXX while True:
     yield stuff

This works because a generator object can be garbage collected, just
like any other object implementing the iteration protocol. The fact
that it uses the machinery of function objects to implement itself
doesn't matter.



.. sidebar:: How it actually works

  Generators are actually compiled differently from other
  functions. Each yield point saves the state of unnamed local
  variables (Java temporaries) into the frame object, then returns the
  value to the function that had called ``next`` (or ``send`` in the
  case of a coroutine). The generator is then indefinitely suspended,
  just like any other iterator. Upon calling next again, the generator
  is resumed by restoring these local variables, then executing the
  next bytecode instruction following the yield point. This process
  continues until the generator is either garbage collected or it
  exits.

  You can determine if the underlying function is a generator if its
  code object has the ``CO_GENERATOR`` flag set in ``co_flags``.

  Generators can also be resumed from any thread, although some care
  is necessary to ensure that underlying system state is shared (or
  compatible). We will explore how to use effectively use this
  capability in the chapter on concurrency.


Generator Expressions
^^^^^^^^^^^^^^^^^^^^^

This is an alternative way to create the generator object. Please note
this is not a generator function! It's the equivalent to what a
generator function returns when called.

. Creates an unnamed generator. But cover
this later with respect to generators. Note that generators are not callable objects::

  >>> x = (2 * x for x in [1,2,3,4])
  >>> x
  <generator object at 0x1>
  >>> x()
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: 'generator' object is not callable



Using Generators
~~~~~~~~~~~~~~~~

Python iteration protocol. iter, next.


Generator Example
~~~~~~~~~~~~~~~~~

contextlib

Jar scanner

How to use in interesting ways with Java. For example, we wrap
everything in Java that supports ``java.util.Iterator`` so it supports
the Python iteration protocol.

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
~~~~~~~~~~~~~~~~~~~~~

XXX Maybe something simple with Java Mail? Could show how to attach files that meet a certain criteria?


Namespaces, Nested Scopes and Closures
--------------------------------------

Functions can be nested.

Most importantly this allows the construction of closures.


Namespaces
Note that you can introduce other namespaces into your function definition. So::

  def f():
      from NS import A, B


Function Decorators
-------------------

Function decorators are two things:

 * A convenient syntax that describes how to transform a function. You
   might want to *memoize* a given function, so it uses a cache, with
   a desired policy, to remember a result for a given set of
   parameters. Or you may want to create a static method in a class.

 * A powerful, yet simple design where the decorator is a function on
   function that results in the decorated, or transformed, function.

(Class decorators are similar, except they are functions on classes).

XXX example - XXX How about a decorator for Java integration? eg add support of a given interface to facilitate callbacks


Creating Decorators
~~~~~~~~~~~~~~~~~~~

Memoization decorator. For our same Fibonacci example.


Often a function definition is not the simplest way to write the
desired decorator function. Instead, you might want to create a class,
as we described in alternate ways to create function objects.

XXX In addition, ``functools``, specifically the ``wraps`` function.

XXX ref Eckel's article on decorators.


Using Decorators
~~~~~~~~~~~~~~~~







XXX Chopping block


Coroutines
----------

 One thing
to remember: coroutines do not mix with generators, despite being
related in both syntax and implementation. Coroutines use push;
generators use pull.

XXX The PyCon tutorial on coroutines has some useful coroutine
examples - certainly need similar coverage.

XXX Might be nice to show how to use this in
conjunction with parallelism. but that's a later chapter anyway


Advanced Function Usage
-----------------------

Frames
Tracebacks
Profiling and tracing
Introspection on functions - various attributes, etc, not to mention the use of inspect


.. sidebar:: Function Code Bodies

  Jython, like CPython, only has one unit of compilation, the function
  code body. When a module is compiled, every function in it is
  compiled even if it's not ultimately bound to a name. In addition, a
  script or module is itself treated as a function when
  compiled. These function definitions are compiled to Java
  bytecode. (There's experimental support for other formats, namely
  Python bytecode, which we may see be used in later versions of
  Jython.)


.. sidebar:: Partitioning this global namespace with shadowing.



  The inspect module. Determining parameters, etc.
  One thing that is not supported: introspecting on code objects themselves.






.. sidebar::

  Behind the scenes, this function application is compiled to
  x.__call__(*args, **kwargs), and that's how it's called from Java. A
  convenience method is also provided, invoke, that combines method
  lookup and dispatch together. So you can directly call Python
  functions from Java code in this way. We will look at this more in
  the chapter on Java integration.





.. sidebar:: Special syntax support for operators

  x.a
  del x
  x[i]
  etc.

  All operators are also available as functions from the :module:`operator`. 
  It should be noted that operators on built-in types (int, str, dict,
  etc.) will usually execute faster on the JVM because they do not
  require dynamic dispatch. Invokedynamic, part of JDK 7, is exciting
  because it makes that cost go away, but we will have to wait for
  that. 
