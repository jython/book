Chapter 19:  Concurrency
========================

Supporting concurrency is increasingly important. In the past,
mainstream concurrent programming generally meant ensuring that code
interacting with relatively slow network, disk, database, and other
I/O did not unduly slow things down. Exploiting parallelism was
typically only seen in such domains as scientific computing with apps
running on supercomputers.

But there are new factors at work now. The semiconductor industry
continues to work feverishly to uphold Moore's Law of exponential
increase in chip density. Chip designers used to apply this bounty to
speeding up an individual CPU. But for a variety of reasons, this old
approach no longer works as well. So now chip designers are cramming
chips with more CPUs and hardware threads. Speeding up execution now
means harnessing the parallelism of the hardware, and it's our job as
software developers to do that work.

The Java platform is arguably the most robust environment for running
concurrent code today, and it can be readily be used from Jython.  The
problem remains that writing concurrent code is not easy. This
difficulty is especially true with respect to a concurrency model
based on threads, which is what today's hardware natively exposes.

This means we have to be concerned with thread safety, which arises as
an issue because of the existence of mutable objects that are shared
between threads. (Mutable state might be avoidable in functional
programming, but it would be hard to avoid in any but the most trivial
Python code.) And if you attempt to solve concurrency issues
through synchronization, you run into other problems. Besides the
potential performance hit, there are opportunities for deadlock and
livelock.

.. note::

  Implementations of the JVM, like HotSpot, can often avoid the
  overhead of synchronization. We will discuss what's necessary for
  this scenario to happen later in this chapter.

Given all of these issues, it has been argued that threading is just
too difficult to get right. We're not convinced by that
argument. Useful concurrent systems have been written on the JVM, and
that includes apps written in Jython. Key success factors in writing
such code include:

XXX i don't like this prescription, we need to rework

 * Keep the concurrency simple. Avoid heterogeneity by using tasks,
   which then are mapped to threads.

 * Avoid unnecessary sharing of mutable objects.

 * Simplify sharing. Queues and related objects -- like
   synchronization barriers -- provide a structured mechanism to hand
   over objects between threads.

Generally you will want to use Python's standard threading support,
through the ``threading`` module. If you are coming from Java, you
will recognize this API, since it is substantially based on
Java's. Alternatively you can go directly against the
``java.util.concurrent`` package.

You can also mix and match. Because of the support of tasks in
``java.util.concurrent``, this is probably the best option.



How to Choose?
--------------

One issue that you will have to consider in writing concurrent code is
how much to make your implementation dependent on the Java
platform. Here are our recommendations:

  * If you are porting an existing Python code base that uses
    concurrency, you can just use the standard Python ``threading``
    module. Such code can still interoperate with Java, because Jython threads
    are always mapped to Java threads.

  * Jython implements ``dict`` and ``set`` by using Java's
    ``ConcurrentHashMap``. This means you can just use these standard
    Python types, and still get high performance concurrency. (They
    are also atomic like in CPython, as we will describe.) 

  * You can also any use of the collections from
    ``java.util.concurrent``. So if it fits your app's needs, you may
    want to consider using such collections as
    ``CopyOnWriteArrayList`` and ``ConcurrentSkipListMap`` (new in
    Java 6). The `Google Collections Library
    <http://code.google.com/p/google-collections/>`_ is another good
    choice that works well with Jython.
   
  * Use higher-level primitives from Java instead of creating your
    own. This is particular true of the executor services for running
    and managing tasks against thread pools. So for example, avoid
    using ``threading.Timer``, because you can use timed execution
    services in its place. But still use ``threading.Condition`` and
    ``threading.Lock``. In particular, these constructs have been
    optimized to work in the context of a with-statement, as we will
    discuss.

In practice, using Java's support for higher level primitives should
not impact the portability of your code so much. Using tasks in
particular tends to keep all of this well-isolated. And such thread
safety considerations as thread confinement and safe publication
remain the same.


Working with Threads
--------------------

Creating threads is easy, perhaps too easy::

  XXX thread creation code

The runnable function can be a regular function, or an object that is
callable (implements ``__call__``)::

  XXX sample code with __call__

To wait for a thread to complete, call ``join`` on it::

  XXX code

Here's a simple test harness we might use::

  XXX a test harness


Thread Lifecycle
----------------


XXX Cancellation, joining, interruption



.. sidebar:: Daemon Threads

  Daemon threads present an alluring alternative to managing the
  lifecycle of threads. A thread is set to be a daemon thread before
  it is started::

    XXX code
    # create a thread t
    t.setDaemon(True)
    t.start()

  Daemon status is inherited by any child threads. Upon JVM shutdown,
  any daemon threads are simply terminated, without an opportunity --
  or need -- to perform cleanup or orderly shutdown.

  Our advice is to not use daemon threads, at least not without
  serious thought given to their usage. In particular, it's important
  to never have daemon threads hold any external resources, like
  database connections or file handles. Such resources will not be
  properly closed. Additionally, a daemon thread should never make an
  import attempt.

  In practice, the only use case for daemon threads is when they are
  strictly used to work with in-memory objects, typically for some
  sort of housekeeping. For example, you might use them to maintain a
  cache or compute an index.


Thread Locals
-------------

The ``threading.local`` class enables a simple way of associating
objects with any given thread.

Its usage is deceptively simple. Simply instantiate this class -- or a
subclass, and assign it to a name. (So that part is just like working
with any other object in Python.) Threads then can share the name, but
with a twist: each thread will see a different, thread-specific
version of the object.  This object can have arbitrary attributes
added to it, and it will not be visible to other threads::

  XXX code

In addition, you can subclass ``threading.local``
And __slots__ 

In the end, thread locals are an interesting aside. They do not work
really at all in a task-oriented model, because you don't want to
associate context with a worker thread that will be assigned to
arbitrary tasks. This really would just make for a confused mess.


No Global Interpreter Lock
--------------------------

Jython lacks the global interpreter lock (GIL), which is an
implementation detail of CPython. For CPython, the GIL means that only
one thread *at a time* can run Python code. This restriction also
applies to much of the supporting runtime as well as extension modules
that do not release the GIL. Unfortunately development efforts to
remove the GIL in CPython have so far only had the effect of slowing
down Python execution significantly.

The impact of the GIL on CPython programming is that threads are not
as useful as they are in Jython. Concurrency will only be seen in
interacting with I/O as well as scenarios where computation is managed
by an extension module on data structures outside of the CPython's
runtime. Instead, developers typically will use a process-oriented
model to evade the restrictiveness of the GIL.

Again, Jython does not have the straightjacket of the GIL. This is
because all Python threads are mapped to Java threads and use standard
Java garbage collection support (the main reason for the GIL in
CPython is that it uses a reference counting GC system). The important
ramification here is that you can use threads for compute-intensive
tasks that are written in Python.


Module Import Lock
------------------

Python does define a *module import lock*, which is implemented by
Jython. This lock is acquired whenever an import of any name is
made. This is true whether the import goes through the import
statement, the equivalent ``__import__`` builtin, or related
code. It's important to note that even if the corresponding module has
already been imported, the module import lock will still be acquired,
if only briefly.

So don't write code like this in a hot loop, especially in threaded
code::

  def slow_things_down():
      from foo import a, b
      ...

It may still make sense to defer your imports. Such deferral can
decrease the start time of your app. Just keep in mind that thread(s)
performing such imports will be forced to run single threaded because
of this lock. So it might make sense for your code to perform deferred
imports in a background thread::

  XXX code demoing this

It may be somewhat contrived, but you could even have these imports be
scheduled as tasks::

  XXX code

Here's why we need the module import lock. Upon the first import, the
import procedure runs the (implicit) top-level function of the
module. Even though many modules are often declarative in nature, in
Python all definitions are done at runtime. Such definitions
potentially include further imports (recursive imports). And the
top-level function can certainly perform much more complex tasks. The
module import lock simplifies this setup so that it's safely
published. We will discuss this concept further later in this chapter.

Note that in the current implementation, the module import lock is
global for the entire Jython runtime. This may change in the future.


Working with Tasks
------------------

It's often best to avoid managing the lifecycle of threads
directly. Tasks provide a better abstraction: units of work that move
in turn through being created, submitted, started, and
completed. Tasks can also be cancelled or even interrupted.

Normally you will be using ``FutureTask``, which implements the
``Future`` interface.

What's nice about this approach is that a ``FutureTask`` is the
concurrent equivalent of a method or function call. So here's how we
can do this with a one-shot async function call. This sample code let
us download a web page in the background::

  XXX code to download web page

In Jython any other task could be done in this fashion, whether it is
a database query or a computationally intensive task written in Python.

Up until the ``get`` method on the returned future, the caller run
concurrently with this task. The ``get`` call then introduces a
wait-on dependency on the task's completion. (So this is like calling
``join`` on a thread.) Upon completion, either the result is returned,
or an exception is thrown into the caller. This exception will be one
of:

  * InterruptedException
  * ExecutionException

(This pushing of the exception into the asynchronous caller is thus
similar to how a coroutine works.)

Actually mapping tasks against underlying threads is done through a
Java execution service. Generally you want to use a thread pool to
control the degree of concurrency.

So this results in the following:

  * Use a thread pool through a Java execution service. There are a
    number of execution services available, each specialized for a
    given purpose.

  * Work with ``FutureTask`` objects, which provide a more useful
    abstraction of both joining on a thread and getting the result.


  XXX code with Futures - problem is taking them in the order of completion

XXX rework below

As usual with the ``java.util`` package, and perhaps even more so in
``java.util.concurrent``, there are an abundance of options. But
``ExecutorCompletionService`` is probably the most useful. Here's how
to concurrently download a set of web pages::

  XXX code demonstrating with ExecutorCompletionService - maximize concurrency


.. sidebar:: Why Use Tasks Instead of Threads

  A common practice we see in code in the wild is the addition of
  threading in a haphazard fashion:

   * Heterogeneous threads. Perhaps you have one thread that updates
     from the database. And another that rebuilds an index. What
     happens when you have multiple tables you're reading?

   * Dependencies are managed through a variety of channels, instead
     of being formally structured.

  You want to avoid a rats' nest of timers and threads synchronizing
  on each other. This is a very bad habit, because it limits
  scalability.

  Instead use tasks, with explicit wait-on dependencies and time
  scheduling. 

(Alternatively you might want to wrap such execution service. There is
some early work on this that's worth tracking, XXX Python futures.)


Thread Safety
-------------

Thread safety addresses such questions as:

  * Can the (unintended) interaction of two or more threads corrupt a
    mutable object? This is especially dangerous for a collection like
    a list or a dictionary, because such corruption could potentially
    render the underlying data structure unusable or even produce
    infinite loops when traversing it.

  * Can an update get lost? Perhaps the canonical example is
    incrementing a counter. In this case, there can be a data race with
    another thread in the time between retrieving the current value,
    and then updating with the incremented value.

Jython ensures that its underlying mutable collection types --
``dict``, ``list``, and ``set`` -- cannot be be corrupted by using
code. But updates still might get lost in a data race.

However, other Java collection objects your code may use may not have
such no-corruption guarantees. If you need to use ``LinkedHashMap``,
so as to support an ordered dictionary, you will need to consider
thread safety if it will be both shared and mutated.

Of course these concerns do not apply to immutable objects. Commonly
used objects like strings, numbers, datetimes, tuples, and frozen sets
are immutable. And you can also create your own immutable objects. (Of
course, this is Python, so it's restricted to either using convention
or perhaps throwing exceptions, which can be subverted in any event.)

There are a number of other strategies in solving thread safety issues. We
will look at them as follows:

 * Synchronization

 * Atomicity

 * Thread Confinement


Synchronization
~~~~~~~~~~~~~~~

We use synchronization to control the entry of threads into code
blocks corresponding to synchronizable resources. Through this control
we can prevent data races, assuming a correct synchronization
protocol. (This can be a big assumption!)

A ``threading.Lock`` ensures entry by only one thread. (In Jython, but
unlike CPython, such locks are always reentrant; there's no
distinction between ``threading.Lock`` and ``threading.RLock``.) Other
threads have to wait until that thread exits the lock. Such explicit
locks are the simplest and perhaps most portable synchronization to
perform.

You should generally manage the entry and exit of such locks through a
with-statement; failing that, you must use a try-finally to ensure
that the lock is always released when exiting a block of code.

Here's some example code using the with-statement. The code allocates
a lock, then shares it amongst some tasks::

  XXX use task harness

  from threading import Lock

  counter_lock = Lock()
  with counter_lock:
      # XXX contended counter
    
Alternatively, you can do this with try-finally::

  XXX try-finally version

But don't do this. It's actually slower than the with-statement. And using the
with-statement version also results in more idiomatic Python code.

Another possibility is to use the ``synchronize`` module, which is specific to
Jython. This module provides a``make_synchronized`` decorator
function, which wraps any callable in Jython in a ``synchronized``
block::

  from synchronize import make_synchronized

  counter = 0

  @make_synchronized
  def increment_counter():
      global counter
      counter += 1
  
  # use threading test harness

  # XXX verify this works with decorating methods too, but it should; perhaps
  # rewrite to use just that and avoid the above global

In this case, you don't need to explicitly release anything. Even in
the the case of an exception, the synchronization lock is always
released upon exit from the function. If you want to synchronize a
smaller block of code, you can do it like this, through a nested
function that is synchronized::

  XXX code with an inner synchronized function

Howver, you probably want to use an explicit ``Lock`` instead of the
``make_synchronized`` decorator. Jython's current runtime (as of
2.5.1) executes code using the with-statement to a form
that the JVM can execute more efficiently::

  XXX demo two versions with timeit

(But this may change in a later release of Jython.) In addition,
explicit locks give greater flexibility in terms of controlling
execution.

The ``threading`` module offers portablity, but it's also
minimalist. You may want to use the synchronizers in
``Java.util.concurrent``, instead of their wrapped versions in
``threading``. In particular, this approach is necessary if you want
to wait on a lock with a timeout::

  XXX code demoing timeout

You can always use factories like ``Collections.synchronizedMap``,
when applicable, to ensure the underlying object has the desired
synchronization::

  XXX code

Deadlocks
^^^^^^^^^

But use synchronizaton carefully. This code will always eventually
deadlock::

  XXX code demonstrating locks take in different orders, using the
  with-statement

Deadlock results from a cycle of any length of wait-on
dependencies. For example, Alice is waiting on Bob, but Bob is waiting
on Alice. Without a timeout or other change in strategy -- Alice just
gets tired of waiting on Bob! -- this deadlock will not be broken.

Avoiding deadlocks can be done by never acquiring locks such that a
cycle like that can be created. Bob always allows Alice to go first,
in the example above. However, this is not always easy to do. Often, a
more robust strategy is to allow for timeouts.


Other Synchronization Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 

Synchronized Queues

Queue
First-in, first-out

A number of methods, including join

If you need to implement another policy, such as last-in, first-out or based on a priority, you can use ``java.util.concurrent`` for the appropriate

(These have since been implemented in Python 2.6.)


Condition variables

It's important that you carefully consider 
In particular, there's no guarantee that only one thread will be woken

There are other mechanisms to synchronize, including exchangers,
barriers, latches, etc. You can use semaphores to describe scenarios
where it's possible for multiple threads to enter. Or use locks that
are set up to distinguish reads from writes. There are many
possibilities.


Atomic Operations
~~~~~~~~~~~~~~~~~

XXX what is an atomic operation

An atomic operation is inherently thread safe, because it ensures 

Atomic operations are simpler to use than synchronization. And atomic
operations will often use underlying support in the CPU, such as
``compare-and-swap``. Or they may use locking too. The important thing
to know is that the lock is not directly visible and it's not possible
to expand the scope of the synchronization. In particular, callbacks
and iteration are not feasible.

  .. sidebar:: Transactions

  Transactions do allow for multiple operations to be combined into an
  atomic entity. Clojure implements a form of this, software
  transactional memory. In the future we should expect similar
  developments like this in other languages, including Python and
  specifically the Jython implementation.

  XXX reference Nicholas' work?

Python guarantees the atomicity of certain operations, although at
best it's only informally documented. Fredrik Lundh's article on
"Thread Synchronization Methods in Python" summarizes the mailing list
dicussions and the state of the CPython implementation. Quoting his
article, the following are atomic operations for Python code:

  * Reading or replacing a single instance attribute

  * Reading or replacing a single global variable

  * Fetching an item from a list

  * Modifying a list in place (e.g. adding an item using append)

  * Fetching an item from a dictionary

  * Modifying a dictionary in place (e.g. adding an item, or calling
    the clear method)

Although unstated, this also applies to equivalent ops on the
builtin set type.

For CPython, this atomicity emerges from combining its Global
Interpreter Lock (GIL), the Python bytecode virtual machine execution
loop, and the fact that types like ``dict`` and ``list`` are
implemented natively in C and do not release the GIL.

Despite the fact that this is in some sense accidentally emergent,
it's a useful simplification for the developer. And it's what existing
Python code expects. So this is what we have implemented in Jython.

In particular, because ``dict`` is a ``ConcurrentHashMap``, we also
expose the following methods to atomically update dictionaries::

  * ``setifabsent``

  * ``update``

So for example, you can implement a concurrent spanning tree::

  XXX code

It's important to note that iterations are not atomic::

  XXX maybe show this with iterating over basic data types

And you can't construct an atomic counter this way either::

  XXX code demonstrating unsafe counter

But you can get an atomic counter by using a Java class like
``AtomicInteger``::

  XXX code

Atomic operations are not a panacea. You still may have to use
synchronization to prevent data races. And this has to be done with
care to avoid deadlocks and starvation.


Thread Confinement
~~~~~~~~~~~~~~~~~~

Thread confinement is often the best solution to resolve most of the
problems seen in working with mutable objects. In practice, you
probably don't need to share a large percentage of the mutable objects
used in your code. Very simply put, if you don't share -- if you use
thread confinement -- thread safety issues go away.

Not all problems can be reduced to using thread confinement. There are
likely some shared objects in your system, but in practice most can be
eliminated. And often the shared state is someone else's problem.

  * Intermediate objects. If you are building up a buffer that is only
    pointed to by a local variable, you don't need to synchronize.

  * Producer-consumer. Handoff through safe publication, such as
    through some type of blocking queue. (XXX CompletionExecutionService,
    Queue, etc.) This is
    generally easy to ensure in Jython.

  * Containers. The typical database-driven web applications makes for
    a classic example. With Jython, specifically through ModJy,
    database connection pools and thread pools are the responsibility
    of the servlet container, they are not directly
    observable. (Although you may run into problems if you attempt to
    share database connections across threads. That is not advisable.)

    Caches and databases then are where you will see shared state.

  * Actors. The actor model is another good example. Send and receive
    messages to an actor (effectively an independent thread) and let
    it manipulate any objects it owns on your behalf. Effectively this
    reduces the problem to sharing one mutable object, the message
    queue. The message queue can then ensure any accesses are
    appropriately serialized, so there are no thread safety issues.


Unfortunately thread confinement is not without issues in Jython. For
example, if you use ``StringIO``, you have to pay the cost that this
class uses ``list``, which is synchronized. Although it's possible to
further optimize the Jython implementation of the Python standard
library, if a section of code is hot enough, you may want to consider
rewriting that in Java to ensure no additional synchronization
overhead.

.. sidebar:: Introspection and Thread Confinement

  Thread confinement is not perfect in Python, because of the
  possibility of introspecting on frame objects.

  XXX insert from concurrency.rst

  In the end, this is not really an issue from a Pythonic
  perspective.

  XXX similar considerations apply to any manipulation of an object,
  the lack of public-private distinctions, etc.

  If you change an object's class, or directly modify its
  underlying attributes (through ``__dict__``), you have violated that
  object's contract. Don't do that, at least without understanding the
  consequences.


Timeouts and Cancellations
--------------------------

XXX cover this topic

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

Task Cancellation
~~~~~~~~~~~~~~~~~

XXX


Python Memory Model
~~~~~~~~~~~~~~~~~~~

Reasoning about concurrency in Python is easier than in Java. This is
because the memory model is not as surprising to our conventional
reasoning about how programs operate.

Here's why. In order to maximize performance, it's allowed for a CPU
to arbitrarily re-order the operations performed by Java code, subject
to two constraints:

happens-before
synchronizes-with

http://java.sun.com/docs/books/jls/third_edition/html/memory.html


Although such reordering is not visible within a given thread, it is
certainly visible to other threads. Of course, this only applies to
changes made to non-local objects.

Java developers can 

In particular, the volatile keyword is used to control happens-before.

And thereby construct a memory fence - no reordering is possible around this fence.




The fundamental thing to know about Python is that setting any
attribute in Python introduces a volatile write; and getting any
attribute is a volatile read. This is because Python attributes are
stored in dictionaries, and in Jython, this follows the semantics of a
``ConcurrentHashMap``; ``get`` and ``set`` (``put`` in Java) are volatile.

Python code sacrifices some performance to keep it
simpler. We will further discuss the ramifications of this [XXX
deoptimization].

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



Safe publication
~~~~~~~~~~~~~~~~

Related to thread confinement. Construction.

Note this is not perfect.

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


Executors
~~~~~~~~~

fixed thread pool
timed execution
etc.

XXX What about something that dynamically adjusts based on load?

Futures
~~~~~~~

Putting it together
~~~~~~~~~~~~~~~~~~~




Other Concurrency APIs
----------------------

This chapter only represents some of what you can do with concurrency
in Jython.

Other current possibilities include:

  * The ``futures`` module (http://code.google.com/p/pythonfutures/). 

  * Generalized coroutine support. Work is ongoing on the da Vinci
    machine, an experimental branch of the Hotspot JVM, to directly
    support coroutines. Unlike standard Python coroutines, this will
    enable direct control of the scheduling (supports nested
    coroutines), instead of yielding to a *trampoline*.

  * Actors. Very closely related to coroutine support.

  * In addition, other concurrent programming APIs can also be used,
    such as Terracotta. 

XXX maybe look at the new TC API support

.. sidebar::
  
  Note there are other models of concurrency that don't directly
  expose threads to users, or make them easier to use. 

  

  X10

  In particular,
  the Lisp dialect Clojure, a JVM language provides some exciting
  options.

  XXX Transactional memory, agents, etc.


