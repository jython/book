.. -*- mode: rst -*-

.. meta::

   XXX thoughts on what should go in here
   
   it would be nice to consider mapping generators against threads,
   although the fork-join section certainly covers one interesting case

   fix section references to use standard RST/Sphinx

   would it be possible to create custom references such that
   threading.Lock -> http://docs.python.org/library/threading.html#lock-objects and java.util.concurrent.FutureTask -> http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/FutureTask.html ?

   directly incorporate references to functions

   Java 6 is generally preferrable for concurrent ops


   biblio:
    
     Cite *Java Concurrency in Practice* as a go-to guide.

     http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/package-summary.html
     -- I believe the JSR 166 group has some excellent docs somewhere
     around there too, but internally it's well documented too.

     http://www.ibm.com/developerworks/library/j-jtp03304/ - Fixing
     the Java Memory Model

     http://effbot.org/zone/thread-synchronization.htm - Python thread
     safety discussion, including summary of the various issues


    possible entries in the Cookbook: Hadoop (Happy), Scala actors,
    memcached, Terracotta



Concurrency
===========

Often you won't need to work directly with concurrency, although it's important to understand its implications. Code run in a servlet context will be run by a thread allocated from a thread pool. However, even then, the For example, if your code is run as a servlet, then the app server will allocate a thread from a thread pool to run your code. If the code is thread confined, or more realistically, using shared objects like a connection pool that expose a thread safe interface, you may 

And as we will see 

through modjy or another wrapper, you will often not need to submit tasks to a thread pool or spawn threads because However, once you have shared, mutable state, you will need to ensure that your code is safely 

working with that shgenerally not be creating tasks or spawning threads

Servlets, run in an app container
But this doesn't apply to you

XXX intro - basics, threading, how you should use higher level primitives if possible

Python memory model
Then mention two more advanced areas - fork-join

XXX Terracotta, Quartz and others will go in the cookbook
Also JMS and its successors


Portability Concerns
~~~~~~~~~~~~~~~~~~~~

One issue that you will have to consider is to much to make your
concurrent code dependent on the Java platform. Here are our
recommendations:

  * If you are porting an existing Python code base that uses
    concurrency, you can use the standard Python ``threading`` module,
    and any code that relies on this. You can also interoperate since
    Jython threads are always mapped to Java threads. We will actually
    this this last.

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
    ``threading.Lock``. In particular, they have been optimized to
    work in the context of a with-statement, as we will discuss.

The Java platform is arguably the most robust environment for running
concurrent code, so we do believe it makes sense for Python developers
to use these facilities. In practice, this should not impact the
portability so much - using tasks in particular tends to keep this
well isolated in your code. And such considerations as thread
confinement and safe publication remain the same.

XXX This chapter is structured to follow these recommendations.


Concurrency Basics
------------------

Threads vs Tasks
~~~~~~~~~~~~~~~~

A common practice is to add threading in a haphazard fashion:

 * Threads are heterogeneous.

 * Dependencies are managed through a variety of channels, instead of
   being formally structured.

And what happens when the work performed by a thread depends on each
other? Perhaps you have one thread that updates from the database. And
another that rebuilds an index. And so forth. You want to avoid a
rats' nest of timers and threads synchronizing on each other.

XXX a diagram here would be nice - in general we might want to use
sequence diagrams here! MF tweeted on some nice tool for this a while
back, let's see if applicable.

This is a very bad habit, because it limits scalability.

Instead use tasks, with explicit wait-on dependencies and time scheduling.

XXX introduce simple test harness for running a number of threads - we
will explain more about how it works in the section on :ref:``threading``.

XXX shouldn't this be in the context of a thread pool instead?
creating threads is a bad idea. Let's get people out of this
habit. (Even if it's good for simple testing.)

XXX can we make it so that a pure Python thread pool (to be described
later) or one based on Java can be used exactly the same way -
basically make it pluggable. Yes, that would be ideal. Especiall if we
can show how to write a threaded style test harness too.

XXX yes, I think this makes the most sense - it will significantly
improve the quality of the presentation. And it can be simplified by
simply requiring a callable, as well as any desired
dependencies. Basically support a simple wrapper around futures seems
to be the best idea. Then we can also get dependencies. And have timed
submits too.


Thread safety
~~~~~~~~~~~~~

Question addressed to : without external locking, can code corrupt an object - like a list?

Closely related to atomic operations

Move from a consistent state to another consistent state.

Full ACID properties? Well certainly not durability here; nor
composition together as we see in a transaction.


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

XXX discuss lock ordering and the problems presented by cycles in our acquistion.

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


XXX push threading module discussion to end of the chapter

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
perform cleanup or orderly shutdown. Therefore it's important that
daemon threads only be used for certain types of housekeeping tasks,
such as maintaining a cache.

Even better would be to avoid their use and write your code as
cancellable tasks. This requires understanding thread cancellation and
interruption.

Thread Interruption
~~~~~~~~~~~~~~~~~~~

Standard Python thread semantics do not directly support thread
interruption. Instead you would code something like the following::

  class DoSomething(Runnable):
      def __init__(self):
          cancelled = False

      def run(self):
          while not self.cancelled:
              do_stuff()

As you may recall, the instance variable ``cancelled`` is guaranteed
to be volatile by the Python memory model. So setting ``cancelled`` to
``True`` will reliably terminate this loop on its next
iteration. However, this does assume ``do_stuff`` is not holding a
lock or some other resource. (It certainly says nothing about being in
an infinite loop or similar unresponsive state.)

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
  
  while not JThread.currentThread().isInterrupted():
  # or alternatively, JThread.isInterrupted(threading.Thread.currentThread())
      do_stuff()

The ``isInterrupted`` method helps ensure cancellation is responsive
as possible, in the case that ``do_stuff`` is not actually waiting on
a synchronizer. Think belts and suspenders.

With this in place, interrupting an arbitrary Jython -- or Java --
thread is also easy. Simply do the following::

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

  The JVM can often eliminate locking so long as the lock/unlock pair
  occurs in the same unit of code, and this unit of code is
  sufficiently small. Using the with-statement form helps make that
  possible.

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


.. _tasks:

Higher-Level Java Concurency Services
-------------------------------------

Better yet, use higher-level services.

Task model
Executors
ExecutorService and supporting factories in java.util.concurrent.executors

In particular, CompletionService executors offer very nice functionality:
http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/ExecutorCompletionService.html

Futures, in particular you will normally want to derive from FutureTask
http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/FutureTask.html

.. example::

  XXX a nice example to show is probably some sort of spidering,
  possibly in conjunction with BeautifulSoup (hopefully that works
  with Jython) - yes that works just fine - retrieve data, analyze it,
  then make some sort of decision

  maybe some sort of opendata service, such as retrieving USGS
  streamflow data

  use a CompletionService, etc.

  http://bret.appspot.com/entry/we-need-a-wikipedia-for-data - useful
  links to potential data

  actually let's just do something like blogs - going through
  comments, finding other blogs -- pretty standard, but interesting
  enough - or perhaps doing some analysis with NLP

  not certain how much of this is captured by Atom client code

  build an in-memory representation - or serialize to terracotta or
  neo4j or whatever

  or do the same w/ twitter

Other things to look at:

  * various types of queues

  * Exchangers

  * Barriers. A ``CyclicBarrier`` is useful for phased computations.



Pure Python Thread Pool Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
details on a possible sizing model. But in general, it's best to
measure. Vary the thread pool size to experimentally determine what
works best for your problem for a given machine setup, and balance
that against other criteria. For example, it may not be acceptable to
attempt to saturate the CPUs for your target!

Regardless, the number of CPUs is a critical parameter. Determining
the number of available CPUs is simple. On my laptop, here's what I
have::

  >>> from java.lang import Runtime 
  >>> Runtime.getRuntime().availableProcessors()
  2

Maybe I should upgrade.

Concurrency and Collection Types
--------------------------------

XXX write a test harness for showing concurrency - maybe extract from
test_list_jy (if I recall correctly), then plug in the below
functions.

Immutable collection types like frozenset and tuple -- not to mention
unicode and str -- are simple. They have no thread safety
issues. This is even true of ``unicode`` objects: while they do have
internal mutable state to determine if the string contents are in the
basic multilingual plane (by far, the most common case), this is not
visible to the user and is used only to select if a slower method must
be used.

This is not true of mutable collection types, including:

  * list (as well as collections.Deque)
  * dict (as well as collections.defaultdict)
  * set


``dict`` and ``set`` are concurrent collections; both are internally
implemented such that they use a ``ConcurrentHashMap``.

Weakly consistent iteration
No synchronization! No synchronization overhead!

setifabsent
remove
replace


Example to demonstrate this::

  XXX

What about ``__missing__`` on ``defaultdict``? Unfortunately, it's not
atomic and subject to races if not synchronized. In a future release
of Jython, we may want to base it on a ``SynchronizedMap`` instead of
inheriting from the implementation of ``dict``. However, because the
underlying implementation is a ``CHM``, at least it will not corrupt
the underlying data structure. Maybe that's OK for your
purposes. Otherwise, you will need to do something like the
following::

  XXX code showing a dict used with setifabsent and an AtomicInteger
  for a counter - hmm, must think this one through (as usual)!


Behavior of builtin data structures

.. sidebar:: Not Paying for Python Thread Safety Semantics

  You can use HashMap or ArrayList directly.
  What's the overhead of doing that?
  Let's do some simple testing.

  This probably will become less costly in the future - local variables.


  For thread confined code, this make sense.

  But take care. The standard implementation of ``HashMap`` must be
  thread confined or synchronized. Otherwise, you might observe its
  internal bucket structure corrupted in such a way that a thred
  traversing it will get trapped in an infinite loop.
 
  [XXX refer to "A Beautiful Race Condition" by Paul Tyma ... http://mailinator.blogspot.com/2009/06/beautiful-race-condition.html ]


Thread Local Storage with ``threading.local``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create any number of instances of ``threading.local``, or even
derive a class from it. You can freely pass references to this object,
but each thread that uses that reference will see actually see a
different instance, with different attributes::
 
  XXX code

You can also derive from the ``threading.local`` class::

  XXX code

Interestingly, any attributes that are stored in slots are shared
across threads::

  XXX code

Of course, you will need to safely publish as names any such
objects. Safe publication is guaranteed by creating these objects in a
module, then importing them.

However, there's a substantial problem in using thread local
storage. By its nature, it interacts poorly with thread pools because
any work is strongly coupled to the thread. However, you might find
useful in solving problems where the use of global state is
interfering with working with threads.

``threading.local`` is implemented as a wrapper of
``java.lang.ThreadLocal``.

Other Resources
~~~~~~~~~~~~~~~

Python also implements a number of other synchronization constructs:

XXX link to relevant docs

  * ``Event``. For general signaling. Use futures instead.

  * ``Semaphore`` and ``BoundedSemaphore``. For bounding resources,
    such as a connection pool.

  * ``Timer``. For executing on a regular basis, such as refreshing a
    cache. Used timed execution services instead.

These classes are more useful if you have an existing Python codebase
that utilizes them, otherwise, we recommend the higher-level Java
variants.

XXX a quick perusal of Google Code suggests that Semaphore is rarely used in practice.



Fork-Join
---------

.. sidebar:: JSR 166

  XXX explain this work, part of Java 7; how to obtain the jar

Work Stealing and fork-join 
map to 

Recursive generators
~~~~~~~~~~~~~~~~~~~~

Recursive generators are simply generators that call themselves
recursively. The general form goes something like this::

  def gen(X):
      if base_case(X):
          yield some_extract(X)
      else:
          for x in gen(X):
              yield some_other_extract(x)

So the base case must either yield something, or optionally, use
return to stop the iteration at that level.

The non-base case needs to pass through results in the generators it
is called back to its caller.

.. sidebar:: ``yield from``

  Note that Python 2.7 (which is under active development as of the
  writing of this book and not yet supported by Jython) supports an
  alternative form, ``yield from``, that among other things, avoids
  the need to loop over the generator being called recursively, and
  yield results back up.

XXX example of doing a traversal of a tree

Like recursion in general, recursive generators cannot always be
applied because of stack size limits. However, if the depth of the
exploration is known to be bounded in advance, it can provide for a
simpler solution than one where the recursion has been eliminated.

A standard representation of a graph in Python is a dictionary
structured as follows:

  * Key are nodes

  * Values are sequences (list/tuple) representing the adjacency
    list. Or this could be a set if unordered.

XXX show the correspondence between a simple graph and this representation


Note that in the case of graph algorithms, it is important do
dynamically balance the workloads; it's not simply sufficient to use a
hierarchical partitioining workstealing

.. comment::

  Python lists cannot be partitioned for sorting in this fashion


Show how they map to Jython very nicely.

Tobias' forkjoin annotation is very nice, see if it can actually be
implemented.

@forkjoin # fork on call, join on iter - 

XXX simple wrapper class that wraps __call__, __iter__ on the underlying generator

XXX alternatively - may want to control when to fork or not by size;
in which case do the fork explicitly


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





