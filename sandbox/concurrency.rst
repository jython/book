.. -*- mode: rst -*-

.. meta::

   XXX thoughts on what should go in here
   
   it would be nice to consider mapping generators against threads,
   although the fork-join section certainly covers one interesting case

   fix section references to use standard RST/Sphinx

   biblio:
    
     Cite *Java Concurrency in Practice* as a go-to guide.

     http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/package-summary.html
     -- I believe the JSR 166 group has some excellent docs somewhere
     around there too, but internally it's well documentede too.

     http://www.ibm.com/developerworks/library/j-jtp03304/ - Fixing
     the Java Memory Model

     http://effbot.org/zone/thread-synchronization.htm - Python thread
     safety discussion, including summary of the various issues


    possible entries in the Cookbook: Hadoop (Happy), Scala actors, memcached



Concurrency
===========

XXX intro - basics, threading, how you should use higher level primitives if possible

Python memory model
Then mention two more advanced areas - fork-join, Terracotta



Portability Concerns
~~~~~~~~~~~~~~~~~~~~

One issue that you will have to consider is to much to make your
concurrent code dependent on the Java platform. Here are our
recommendations:

  * If you're are porting an existing Python code base that uses
    concurrency, you can use the standard Python ``threading`` module,
    and any code that relies on this.

  * Jython implements ``dict`` and ``set`` by using
    ``ConcurrentHashMap``; you can just use these collections for high
    performance concurrency, as we will describe. You can also any use
    of the collections from ``java.util.concurrent``. So if it fits
    your app's needs, you may want to consider using such collections
    as ``CopyOnWriteArrayList`` and ``ConcurrentSkipListMap`` (new in
    Java 6). The `Google Collections Library
    <http://code.google.com/p/google-collections/>`_ is another good
    choice that works well with Jython.
   
  * Use higher-level primitives from Java instead of creating your
    own. This is particular true of the executor services for running
    and managing tasks against thread pools. So for example, avoid
    using ``threading.Timer``, because you can use timed execution
    services in its place. But still use ``threading.Condition`` and
    ``threading.Lock``. In particular, ``Lock`` has been optimized to
    work in the context of a with-statement, as we will discuss.

The Java platform is arguably the most robust environment for running
concurrent code, so we do believe it makes sense for Python developers
to use these facilities. In practice, this should not impact the
portability so much - using tasks in particular tends to keep this
isolated in your code.


Concurrency Basics
------------------

Threads
~~~~~~~


XXX introduce simple test harness for running a number of threads - we
will explain more about how it works in the section on :ref:``threading``.


Thread safety
~~~~~~~~~~~~~

Without external locking, can code corrupt an object - like a list?
Closely related to atomic operations


Atomic Operations
~~~~~~~~~~~~~~~~~

Python guarantees the atomicity of certain operations, although it's
only informally documented. Fredrik Lundh's article on "Thread
Synchronization Methods in Python" summarizes the mailing list
dicussions, the state of the code, and what we inJython have
implemented. Quoting his article, the following are atomic operations:

  * Reading or replacing a single instance attribute

  * Reading or replacing a single global variable

  * Fetching an item from a list

  * Modifying a list in place (e.g. adding an item using append)

  * Fetching an item from a dictionary

  * Modifying a dictionary in place (e.g. adding an item, or calling
    the clear method)

In addition:

  * set ops

  * what else?

Iterations are not atomic.
XXX maybe show this with iterating over basic data types

Note this does not apply to 

But atomicity Canonical example - a counter

Code::

  XXX code demonstrating unsafe counter

You can get an atomic counter by using a Java class like ``AtomicInteger``::

  XXX code

Alternatively, use synchronization.

Synchronization
~~~~~~~~~~~~~~~

Ensure entry by only one thread

Example code using the with-statement::

  XXX code

There are other mechainsms to synchronize, including condition
variables, exchangers, etc.

Use synchronizaton carefully. This code will always deadlock::

  XXX code demonstrating locks take in different orders, using the with-statement

XXX discuss lock ordering

There are numerous workarounds. For example, you might use a timeout::
  
  XXX code

Thread Confinement
~~~~~~~~~~~~~~~~~~





Safe publication
~~~~~~~~~~~~~~~~
create, initialize an object within a thread before publishing it
which means, is it visible before hand

In practice, this is not seen so much in Python code, because most
such references would usually be to variables (attributes) at a module
scope. But Python specifies that there's a module import lock [XXX
reference the specific docs on this] - all module imports are single
threaded!  (Note this only applies to the actual first-time loading of
a module, if you are simply importing a name in, a lock is not
entered.)

XXX check how that applies to different instances of ``PySystemState``
-- could be potentially relaxed for that.




No global interpreter lock.


.. sidebar:: ``from __future__ import GIL``
   
  XXX what is the GIL (Jython actually supports Python bytecode
  evalutation, but even for that, we don't have the GIL.)

  The JVM supports 

  Native threads

  No reference counting. Instead use only garbage collection.

  Ref counting requires that a counter for each reference is
  incremented or decremented. Lock-free counters are potentially one
  solution to that... however, there's also other sensitivity in terms
  of cache interactions.

  XXX rewrite

  So performance suffers when attempts at eliminating the GIL have
  been attempted in CPython.

  At the 2008 Python Conference, it was decided over the course of a
  nice dinner that we needed a Jython-specific easter egg. There's a
  history of this, as seen here::

    >>> from __future__ import braces

  Because there was confusion over whether Jython had the GIL or not,
  we decided to make it very clear that it didn't, and never would::

    >>> from __future__ import GIL

.. _threading:

``threading`` Module
--------------------

The ``threading`` module implements the standard Python API for
working with threads and related resources, such as locks, condition
variables, and queues. The Jython implementation is a thin wrapper of
the corresponding Java classes, something that is facilitated by the
fact that the Python threading API was directly inspired by Java.

Threads
~~~~~~~

In general, you will want to use a task model, instead of directly
assigning work to a thread. With that said, here are the basics of
Python ``Thread`` objects.

XXX various things, including lifecycle


A thread can also set to be a daemon thread before it is started::

  XXX code
  # create a thread t
  t.setDaemon(True)
  t.start()

Daemon status is inherited by any child threads. Upon JVM shutdown,
any daemon threads are simply terminated, without an opportunity to
perform cleanup or orderly shutdown. Consequently daemon threads
should just be used for housekeeping tasks, such as maintaining a
cache.

Thread Interruption
~~~~~~~~~~~~~~~~~~~

XXX say something about good thead interruption is, compared to just using a while on a variable::

  class DoSomething(Runnable):
      def __init__(self):
          cancelled = False

      def run(self):
          while not self.cancelled:
              do_stuff()


Thread interruption allows for more responsive cancellation. In
particular, if a a thread is waiting on any synchronizers, like a
lock, or on file I/O, this action will cause the waited-on method to
exit with an ``InterruptedException``. Although Python's ``threading``
module does not itself support interruption, it's available through
the standard Java API, and it works with any thread created by
``threading`` -- again, Python threads are simply Java threads in the
Jython implementation.

This is how it works::

  from java.lang import Thread as JThread # so as to not confuse with threading.Thread
  
  while not JThread.currentThread().isInterrupted(): # or alternatively, JThread.isInterrupted(threading.Thread.currentThread())
      do_stuff()

Interrupting an arbitrary Jython -- or Java -- thread is also
easy. Simply do the following::

  >>> JThread.interrupt(a_thread)

An easier way to access interruption is through the cancel method
provided by a ``Future``. We will describe this more in the section on
:ref:tasks.

Locks
~~~~~

XXX with-statement support

You will want to use the with-statement form, because it's actually
more efficient than using a ``finally`` block::

  XXX microbenchmark - with-statement vs finally

.. sidebar:: Lock Elimination ("eliding")

  The JVM elides locking if it can determine the pairing of lock and
  unlock is done in the same unit of code. The key is to make this
  unit small enough.

  XXX show this effect

Note: Jython's implementation of ``threading.Lock`` only uses
reentrant locks -- there's no difference between ``threading.Lock``
and ``threading.RLock`` at all in Jython. A non-reentrant lock is a
compromise where safety is sacrificed for performance. However, since
non-reentrant locks are not implemented in Java, we chose not to do so
in Jython. Any implementation we could have written for Jython would
simply have been of lower performance.


Conditions
~~~~~~~~~~

It is important to 

signal/notify


FIFO Synchronized Queues
~~~~~~~~~~~~~~~~~~~~~~~~

XXX blocking vs non-blocking

XXX Compare with using the Java versions - pretty much identical usage, except can choose other policies like prioritized, LIFO


Thread Local Storage with ``threading.local``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create any number of instances of ``threading.local``, or even
derive a class from it. You can freely pass references to this object,
but each thread that uses that reference will see actually see a different
instance, with different attributes::
 
  XXX code

You can also derive from the ``threading.local`` class::

  XXX code

Interestingly, any attributes that are stored in slots are shared
across threads::

  XXX code

Of course, you will need to safely publish as names any such
objects. By creating these objects in a module -- the normal way --
safe publication is guaranteed.

One caveat of using thread local storage is that it tends to interacts
poorly with thread pools. And in general, TLS is best used sparingly
in order to solve problems where the use of global state is
interfering with working with threads.

Under the covers, ``threading.local`` is implemented using
``java.lang.ThreadLocal``.

Other Resources
~~~~~~~~~~~~~~~

Timers, semaphores.
XXX look through some Python codebases, see if these are actually used in practice.



.. _tasks:

Higher-Level Java Concurency Services
-------------------------------------

Better yet, use higher-level services.

Task model
Executors
ExecutorService and supporting factories in java.util.concurrent.executors
Futures
various types of queues
Exchangers

An alternative is to use a pure Python thread pool, such as this
`ActiveState Python Cookbook recipe (203871)
<http://code.activestate.com/recipes/203871/>`_.

XXX referenced by http://blogs.warwick.ac.uk/dwatkins/entry/benchmarking_parallel_python_1_2/

XXX maybe an aside on using this from say a servlet (of course not in GAE)

Thread Pool Sizing
~~~~~~~~~~~~~~~~~~

You will need to perform some analysis on what works best. For
CPU-bound computations, the rule of thumb is the number of CPUs + 1,
or more frequently in our experience, a small constant. I/O
complicates the picture; refer to [JCIP], pp. 170-171, for more
details on a possible sizing model. But in general, it's just best to
vary the thread pool size to determine what works best for your
problem, on a given machine setup.

Regardless, the number of CPUs is a critical parameter. Determining
the number of available CPUs is simple. On my laptop, here's what I
have::

  >>> from java.lang import Runtime 
  >>> Runtime.getRuntime().availableProcessors()
  2


Concurrency and Collection Types
--------------------------------

XXX write a test harness for showing concurrency - maybe extract from
test_list_jy (if I recall correctly), then plug in the below
functions.

Mutable collection types:

list
dict
set

``dict`` and ``set`` are concurrent collections; both are internally
implemented such that use a ``ConcurrentHashMap``.

Weakly consistent iteration
No synchronization! No synchronization overhead!

setifabsent
remove
replace


Example to demonstrate this::

  XXX

list

Immutable collection types:
frozenset
tuple

Behavior of builtin data structures

.. sidebar:: Not Paying for Python Thread Safety Semantics

  You can use HashMap or ArrayList directly.
  What's the overhead of doing that?
  Let's do some simple testing.

  This probably will go down in the future - local variables.

  For thread confined code - 


Fork-Join
---------

.. sidebar:: JSR 166

  XXX explain this work, part of Java 7; how to obtain the jar

Work Stealing and fork-join 
map to 
Recursive generators


Show how they map to Jython very nicely.

Tobias' forkjoin annotation is very nice, see if it can actually be
implemented.


Java Memory Model and Jython
----------------------------

What about other objects in Jython?

XXX put this in a more advanced section
XXX look at the proposed PEP that was written by Jeff Yasskin, not certain if it was circulated to python-dev or not

happens-before relation introduces a partial ordering;
in particular, you cannot rely on the apparent sequential ordering of code

Ordinarily this should not be an issue in Python code executed by
Jython. A Python object that has a ``__dict__`` for its attributes is,
in Jython, represented such that its backed by a
ConcurrentHashMap. CHMs introduce a happens-before relationship to any
code reading .

But there are wa

Local variables are susceptible to reordering. Internally in Jython,
they are stored by indexing into a PyObject[] array, and such accesses
can be reordered. However, this will not usually be visible to user
code -- local variables are *almost* thread confined, and the Java
memory model ensures that any code within that thread will always see
changes that are sequentially consistent.

However, in Python, it is possible for a local variable to *escape*
through the frame object, because locals (and their containing frames)
are introspectable. You can do this via the ``locals`` function. But
even then it requires a fairly convoluted path. Once again, we need to
use a mutable object that does not introduce a fence. Arrays work well
for this purpose::

  A_locals = None

  # thread A
  def f():
      global A_locals
      A_locals = locals()
      x = zeros('L', 1) # must be a mutable object, a Java array works well
      y = zeros('L', 1)
      # write against these variables in some interesting way; maybe y should always be greater than x
      # in this thread, it will - but not in thread B

  # thread B
  def g():
      global A_locals
      A_x = A_locals['x']
      A_y = A_locals['y']
      # now see if we can observe an ordering inconsistent to being sequential

Let's try that again, but not derefencing the local::
   
   XXX code
  
(Perhaps you can find a shorter path?)

 since locals() : you would need to assign
the reference to thread ``A``'s local variable to thread ``B``

(In addition, if you were to access the frame's locals through Java,
using the public methods and fields of ``org.python.core.PyFrame``,
you can also see out-of-order writes.)

(Note that unnamed local variables are truly thread confined, such as
the target of a for loop; only when a generator is paused are they in
any way accessible, and not easily.)


 By far the most common case will

The other is



Safe publication
Immutability


Not final, not volatile. But endowed 

Terracotta
----------

.. notes::

  Terracotta. We should be able to do something meaningful w/o slowing
  down the rest of PyObject - need to figure out the specifics of how
  to mark that certain such objects should be shared. One possibility:
  we could use the proxy mechanisms for exposing Map objects so that
  they support the dict interface. That seems to be the most workable
  solution.

  Probably what makes most sense is to use TC with something like
  Beaker for caching. Dog-pile prevention should be good strategy,
  regardless of how the cache is backed, since it's about populating
  the cache when necessary. (Presumably through some sort of
  interesting protocol that could also benefit from being shared.)


