Chapter 19:  Concurrency
========================

Supporting concurrency is increasingly important. In the past,
mainstream concurrent programming generally meant ensuring that the
code interacting with relatively slow network, disk, database, and
other I/O resources did not unduly slow things down. Exploiting
parallelism was typically only seen in such domains as scientific
computing with the apps running on supercomputers.

But there are new factors at work now. The semiconductor industry
continues to work feverishly to uphold Moore's Law of exponential
increase in chip density. Chip designers used to apply this bounty to
speeding up an individual CPU. But for a variety of reasons, this old
approach no longer works as well. So now chip designers are cramming
chips with more CPUs and hardware threads. Speeding up execution means
harnessing the parallelism of the hardware. And it is now our job as
software developers to do that work.

The Java platform can help out here. The Java platform is arguably the
most robust environment for running concurrent code today, and this
functionality can be readily be used from Jython.  The problem remains
that writing concurrent code is still not easy. This difficulty is
especially true with respect to a concurrency model based on threads,
which is what today's hardware natively exposes.

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

 * Keep the concurrency simple.

 * Use tasks, which can be mapped to a thread pool.

 * Use immutable objects where possible.

 * Avoid unnecessary sharing of mutable objects. 

 * Minimize sharing of mutable objects. Queues and related objects --
   like synchronization barriers -- provide a structured mechanism to
   hand over objects between threads. This can enable a design where
   an object is visible to only one thread when its state changes.

 * Code defensively. Make it possible to cancel or interrupt
   tasks. Use timeouts.


Java or Python APIs?
--------------------

One issue that you will have to consider in writing concurrent code is
how much to make your implementation dependent on the Java
platform. Here are our recommendations:

  * If you are porting an existing Python code base that uses
    concurrency, you can just use the standard Python ``threading``
    module. Such code can still interoperate with Java, because Jython
    threads are always mapped to Java threads. (If you are coming from
    Java, you will recognize this API, since it is substantially based
    on Java's.)

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

Lastly, remember you can always mix and match.


Working with Threads
--------------------

Creating threads is easy, perhaps too easy. This example downloads a
web page concurrently::

  XXX thread creation code

Be careful not to inadvertently invoke the function; ``target`` takes
a reference to the function object (typically a name if a normal
function). Calling the function instead creates an amusing bug where
your target function runs now, so everything looks fine at first. But
no concurrency is happening, because the function call is being
performed within the invoking thread.

The target function can be a regular function, or an object that is
callable (implements ``__call__``). This later example of course makes
it harder to see that the target is a function object::

  XXX sample code with __call__ - 

To wait for a thread to complete, call ``join`` on it. This enables
working with the concurrent result::

  XXX code

Here's a simple test harness we might use. It creates a variation on
``unittest.TestCase`` with a new method ``assertContended``::

  .. literalinclude:: src/chapter19/test_harness.py

The idea is that you want to exercise some structure . So we use this
idea in Jython to test the atomicity of our ``list``
implementation. This is what it looks like for testing that ``append``
and ``remove`` work atomically (more on that later)::

XXX say something about good thead interruption is, compared to just using a while on a variable::

  class DoSomething(Runnable):
      def __init__(self):
          cancelled = False

      def run(self):
          while not self.cancelled:
              do_stuff()

Thread interruption allows for more responsive cancellation. In
particular, if a a thread is waiting on such synchronizers as a
condition variable or on file I/O, this action will cause the
waited-on method to exit with an ``InterruptedException``.
(Unfortunately this excludes most usage of locks.)

Although Python's ``threading`` module does not itself support
interruption, it is available through the standard Java thread
API. First, let's import this class. We will rename it to ``JThread``
so it doesn't conflict with Python's version::

  from java.lang import Thread as JThread

As we have seen, you can use Java threads as if they are Python
threads. So logically you should be able to do the converse: use
Python threads as if they are Jave threads. Therefore it would be nice
to make calls like ``JThread.interrupt(obj)``.

  .. note:
  
  Incidentally, this formulation, instead of ``obj.interrupt()``,
  looks like a static method on a class, as long as we pass in the
  object as the first argument. This adaptation is a good use of
  Python's explicit self.

But there's a problem here. As of Jython 2.5.1, we forgot to include
an appropriate ``__tojava__`` method on the ``Thread`` class! So this
looks like you can't do this trick after all.

Or can you? What if you didn't have to wait until we fix this bug?
Dynamic languages are... dynamic.  You could explore the source code
or look at the class with ``dir``. One possibility would be to use the
nominally private ``_thread`` attribute on the ``Thread``
object. After all ``_thread`` is the attribute for the underlying Java
thread. Yes, this is an implementation detail, but it's probably fine
to use. It's not so likely to change.

But we can do even better. We can *monkey patch* the ``Thread`` class
such that it has an appropriate ``__tojava__`` method, but only if it
doesn't exist. So this patching is likely to work with a future
version of Jython because we are going to fix this missing method
before we change its implementation!

So here's how we can monkey patch, following a recipe of
Guido van Rossum::

  .. literalinclude:: src/chapter19/monkeypatch.py

This ``monkeypatch_method`` decorator allows us to add a method to a
class after the fact. (This is what Ruby developers call *opening* a
class.) Use this power with care. But again, you shouldn't worry too
much when you keep such fixes to a minimum, especially when it's
essentially a bug fix like this one. In our case, we will use a
variant, the ``monkeypatch_method_if_not_set`` decorator.

Putting it all together, we have this code::

  .. literalinclude:: src/chapter19/interrupt.py

Lastly, an easier way to access interruption is through the ``cancel``
method provided by a ``Future``. We will describe this more in the
section on :ref:tasks.

.. sidebar:: Daemon Threads

  Daemon threads present an alluring alternative to managing the
  lifecycle of threads. A thread is set to be a daemon thread before
  it is started::

    # create a thread t
    t.setDaemon(True)
    t.start()

  Daemon status is inherited by any child threads. Upon JVM shutdown,
  any daemon threads are simply terminated, without an opportunity --
  or need -- to perform cleanup or orderly shutdown.

  This lack of cleanup means it's important that daemon threads never
  hold any external resources, such as database connections or file
  handles. Any such resource will not be properly closed upon a JVM
  exit. For similar reasons, a daemon thread should never make an import
  attempt, as this can interfere with Jython's orderly shutdown.

  In production, the only use case for daemon threads is when
  they are strictly used to work with in-memory objects, typically for
  some sort of housekeeping. For example, you might use them to
  maintain a cache or compute an index.

  Having said that, daemon threads are certainly convenient when
  playing around with some ideas. Maybe your lifecycle management of a
  program is to use "Control-C" to terminate. Unlike regular threads,
  running daemon threads won't get in the way and prevent JVM
  shutdown. Likewise, a latter example demonstrating deadlock uses
  daemon threads to enable the code shutdown.

  With that in mind, it's generally best not use daemon threads. At
  the very least, serious thought should be given to their usage.


Thread Locals
-------------

The ``threading.local`` class enables a simple way of associating
objects with a given thread.  Its usage is deceptively simple. Simply
create an instance of ``threading.local``, or a subclass, and assign
it to a variable or other name. This variable could be global, or part
of some other namespace. So far, this is just like working with any
other object in Python.

Threads then can share the variable, but with a twist: each thread
will see a different, thread-specific version of the object.  This
object can have arbitrary attributes added to it, each of which will
not be visible to other threads::

  XXX code

Other options include subclassing ``threading.local``. As usual, this
allows you to define defaults and specify a more nuanced properties
model. But one unique, and potentially useful, aspect is that any
attributes specified in ``__slots__`` will be *shared* across threads.

However, there's a big problem when working with thread
locals. Usually they don't make sense because threads are not the
right scope. An object or a function is, especially through a
closure. If you are using thread locals, you are implicitly adopting a
model where threads are partitioning the work. But then you are
binding the given piece of work to a thread. This makes using a thread
pool problematic, because you have to clean up after the thread.

 .. sidebar:: Jython's ``ThreadState`` Problem

  In fact, we see this very problem in the Jython runtime. A certain
  amount of context needs to be made available to execute Python
  code. In the past, we would look this ``ThreadState`` up from the
  thread. Historically, this may have been in fact faster in the past,
  but it now slows things down, and unnecessarily limits what a given
  thread can do.  A future refactoring of Jython will likely remove
  the use of ``ThreadState`` completely, simultaneously speeding and
  cleaning things up.

Having said they, thread locals might be useful in certain cases. One
common scenario is one where your code is being called by a component
that you didn't write. You may need to access a thread-local
singleton. And of course, if you are using code whose architecture
mandates thread locals, it's just something you will have to work
with.

But often this is unnecessary. Your code may be different, but Python
gives you good tools to avoid action at a distance. You can use
closures, decorators, even sometimes selectively monkey patching
modules. Take advantage of the fact that Python is a dynamic language,
with strong support for metaprogramming. And remember that the Jython
implementation makes these techniques accessible when working with even
recalcitrant Java code.

In the end, thread locals are an interesting aside. They do not work
well in a task-oriented model, because you don't want to associate
context with a worker thread that will be assigned to arbitrary
tasks. Without a lot of care, this can make for a confused mess.


No Global Interpreter Lock
--------------------------

Jython lacks the global interpreter lock (GIL), which is an
implementation detail of CPython. For CPython, the GIL means that only
one thread *at a time* can run Python code. This restriction also
applies to much of the supporting runtime as well as extension modules
that do not release the GIL. (Unfortunately development efforts to
remove the GIL in CPython have so far only had the effect of slowing
down Python execution significantly.)

The impact of the GIL on CPython programming is that threads are not
as useful as they are in Jython. Concurrency will only be seen in
interacting with I/O as well as scenarios where computation is performed
by an extension module on data structures managed outside of CPython's
runtime. Instead, developers typically will use a process-oriented
model to evade the restrictiveness of the GIL.

Again, Jython does not have the straightjacket of the GIL. This is
because all Python threads are mapped to Java threads and use standard
Java garbage collection support (the main reason for the GIL in
CPython is because of the reference counting GC system). The important
ramification here is that you can use threads for compute-intensive
tasks that are written in Python.


Module Import Lock
------------------

Python does, however, define a *module import lock*, which is implemented by
Jython. This lock is acquired whenever an import of any name is
made. This is true whether the import goes through the import
statement, the equivalent ``__import__`` builtin, or related
code. It's important to note that even if the corresponding module has
already been imported, the module import lock will still be acquired,
if only briefly.

So don't write code like this in a hot loop, especially in threaded
code::

  def slow_things_down():
      from foo import bar, baz
      ...

It may still make sense to defer your imports. Such deferral can
decrease the start time of your app. Just keep in mind that thread(s)
performing such imports will be forced to run single threaded because
of this lock. So it might make sense for your code to perform deferred
imports in a background thread::

  .. literalinclude:: src/chapter19/background_import.py

So as you can see, you need to do at least two imports of the a given
module; one in the background thread; the other in the actual place(s)
where the module's namespace is being used.

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

It's usually best to avoid managing the lifecycle of threads
directly. Instead, the task model often provides a better
abstraction. 

*Tasks* describe the asynchronous computation to be
performed. Although there are other options, the object you ``submit``
to be executed should implement Java's ``Callable`` interface (a
``call`` method without arguments), as this best maps into working
with a Python method or function. Tasks move through the states of
being created, submitted (to an executor), started, and
completed. Tasks can also be cancelled or interrupted.

*Executors* run tasks using a set of threads. This might be one thread,
a thread pool, or as many threads as necessary to run all currently
submitted tasks concurrently. The specific choice comprises the
executor policy. But generally you want to use a thread pool so as to
control the degree of concurrency.

*Futures* allow code to access the result of a computation -- or an
exception, if thrown -- in a task only at the point when it's
needed. Up until that point, the using code can run concurrently with
that task. If it's not ready, a wait-on dependency is introduced.

Given this, here's how we can do this with a one-shot async function
call. This sample code let us download a web page in the background::

  XXX code to download web page

In Jython any other task could be done in this fashion, whether it is
a database query or a computationally intensive task written in Python.

Up until the ``get`` method on the returned future, the caller run
concurrently with this task. The ``get`` call then introduces a
wait-on dependency on the task's completion. (So this is like calling
``join`` on the supporting thread.) Upon completion, either the result
is returned, or an exception is thrown into the caller. This exception
will be one of:

  * InterruptedException

  * ExecutionException. Your code can retrieve the underlying
    exception with the ``cause`` attribute.

(This pushing of the exception into the asynchronous caller is thus
similar to how a coroutine works when ``send`` is called on it.)

Now let's multiplex the downloads of several web pages over a thread
pool::

 XXX code

Shutting down a thread pool should be as simple as calling the
``shutdown`` method on the pool. However, you may need to take in
account this shutdown can happen during extraordinary times in your
code. Here's the Jython version of a robust shutdown function, as
provided in the standard Java docs::

  XXX code

The ``CompletionService`` interface provides a nice abstraction to
working with futures. The scenario is that instead of waiting for all the
futures to complete, as our code did with ``invokeAll``, or otherwise
polling them, the completion service will push futures as they are
completed onto a synchronized queue. This queue can then be consumed,
by consumers running in one or more threads::

  XXX code
 
This setup enables a natural flow.

XXX
Although it may be tempting to then schedule everything through the
completion service's queue, there are limits. For example, if you're
writing a scalable web spider, you would want to externalize this work
queue. But for simple manangement, it would certainly suffice.


.. sidebar:: Why Use Tasks Instead of Threads

  A common practice too often seen in production code is the addition
  of threading in a haphazard fashion:

   * Heterogeneous threads. Perhaps you have one thread that queries
     the database. And another that rebuilds an associated index. What
     happens when you need to add another query?

   * Dependencies are managed through a variety of channels, instead
     of being formally structured. This can result in a rats' nest of
     threads synchronizing on a variety of objects, often with timers
     and other event sources thrown in the mix.

  It's certainly possible to make this sort of setup work. Just debug
  away. But using tasks, with explicit wait-on dependencies and time
  scheduling, makes it far simpler to build a simple, scalable system.


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

However, other Java collection objects that your code might use would
typically not have such no-corruption guarantees. If you need to use
``LinkedHashMap``, so as to support an ordered dictionary, you will
need to consider thread safety if it will be both shared and mutated.

Here's a simple test harness you can use to test some aspects of the
thread safety of your code::

  .. literalinclude:: src/chapter19/test_harness.py

The idea is to to apply a sequence of operations that perform an
operation, then reverse it. One step forward, one step back. The net
result should be right where you started, and in the case of a
collection, how it started. Here's how we can test ``append`` and
``remove`` on a ``list``::

  .. literalinclude:: src/chapter19/test_list.py

Of course these concerns do not apply at all to immutable
objects. Commonly used objects like strings, numbers, datetimes,
tuples, and frozen sets are immutable. And you can create your own
immutable objects too.

There are a number of other strategies in solving thread safety issues. We
will look at them as follows:

 * Synchronization

 * Atomicity

 * Thread Confinement

 * Safe Publication


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
~~~~~~~~~

But use synchronizaton carefully. This code will always eventually
deadlock::

  .. literalinclude:: src/chapter19/deadlock.py

Deadlock results from a cycle of any length of wait-on
dependencies. For example, Alice is waiting on Bob, but Bob is waiting
on Alice. Without a timeout or other change in strategy -- Alice just
gets tired of waiting on Bob! -- this deadlock will not be broken.

Avoiding deadlocks can be done by never acquiring locks such that a
cycle like that can be created. Bob always allows Alice to go first,
in the example above. However, this is not always easy to do. Often, a
more robust strategy is to allow for timeouts.


Other Synchronization Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Queue`` module implements a first-in, first-out synchronized
queue. (Synchronized queues are also called blocking queues, and
that's how they are described in ``java.util.concurrent``.) Such
queues represent a thread-safe way to send objects from one or more
producing threads to one or more consuming threads.

For example, here's a standard way to implement a task queue in
Python. This allows you to distribute work to a thread pool.  Rather
than put in a tuple that describes the work to the consuming thread,
it's probably best to encapsulate. The easiest way to do this is to
define a ``__call__`` method. For compatibility with Java, you can
alias that to ``call`` too::

  .. literalinclude:: src/chapter19/worker.py

Often, you will define a poision object to shut down the queue. This
will allow any consuming, but waiting threads to immediately shut
down. (Or use Java's support for executors to get an off-the-shelf
solution.)

If you need to implement another policy, such as last-in, first-out or
based on a priority, you can use the comparable synchronized queues in
``java.util.concurrent`` as appropriate.  (Note these have since been
implemented in Python 2.6, so they will be made available when Jython
2.6 is eventually released.)

``Condition`` objects allow for one thread to ``notify`` another thread
that's waiting on a condition to wake up; ``notifyAll`` is used to
wake up all such threads. Along with ``Queue``, this is probably the
most versatile of the synchronizing objects for real usage.

``Condition`` objects are always associated with a ``Lock``. You use
them like this. Your code needs to bracket waiting and notifying the
condition by acquiring a lock, then finally (as always!) releasing
it. As usual, this is easiest done in the context of the
with-statement::

  .. literalinclude:: src/chapter19/condition.py

For example, here's how we actually implement a ``Queue`` in the
standard library of Jython (just modified here to use the
with-statement). We can't use a standard Java blocking queue, because
the requirement of being able to join on the queue when there's no
more work to be performed requires a third condition variable::

  .. literalinclude:: src/chapter19/Queue.py

There are other mechanisms to synchronize, including exchangers,
barriers, latches, etc. You can use semaphores to describe scenarios
where it's possible for multiple threads to enter. Or use locks that
are set up to distinguish reads from writes. There are many
possibilities.


Atomic Operations
~~~~~~~~~~~~~~~~~

An atomic operation is inherently thread safe. Data races and object
corruption do not occur. And it's not possible for other threads to
see an inconsistent view.

Atomic operations are therefore simpler to use than
synchronization. In addition, atomic operations will often use
underlying support in the CPU, such as a ``compare-and-swap``
instruction. Or they may use locking too. The important thing to know
is that the lock is not directly visible. Also, if synchronization is
used, it's not possible to expand the scope of the synchronization. In
particular, callbacks and iteration are not feasible.

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
builtin ``set`` type.

For CPython, this atomicity emerges from combining its Global
Interpreter Lock (GIL), the Python bytecode virtual machine execution
loop, and the fact that types like ``dict`` and ``list`` are
implemented natively in C and do not release the GIL.

Despite the fact that this is in some sense accidentally emergent, it
is a useful simplification for the developer. And it's what existing
Python code expects. So this is what we have implemented in Jython.

In particular, because ``dict`` is a ``ConcurrentHashMap``, we also
expose the following methods to atomically update dictionaries::

  * ``setifabsent``

  * ``update``

It's important to note that iterations are not atomic::

  .. literalinclude:: src/chapter19/unsafe_iteration.py

And you can't construct an atomic counter this way either::

  .. literalinclude:: src/chapter19/unsafe_counter.py

But you can get an atomic counter by using a Java class like
``AtomicInteger``::

  .. literalinclude:: src/chapter19/atomic_integer.py

Atomic operations are useful, but they are pretty limited too. Often,
you still need to use synchronization to prevent data races. And this
has to be done with care to avoid deadlocks and starvation.


Thread Confinement
~~~~~~~~~~~~~~~~~~

Thread confinement is often the best solution to resolve most of the
problems seen in working with mutable objects. In practice, you
probably don't need to share a large percentage of the mutable objects
used in your code. Very simply put, if you don't share, then thread
safety issues go away.

Not all problems can be reduced to using thread confinement. There are
likely some shared objects in your system, but in practice most can be
eliminated. And often the shared state is someone else's problem:

  * Intermediate objects don't require sharing. For example, if you
    are building up a buffer that is only pointed to by a local
    variable, you don't need to synchronize. It's an easy prescription
    to follow, so long as you are not trying to keep around these
    intermediate objects to avoid allocation overhead. Don't do that.

  * Producer-consumer. Construct an object in one thread, then hand it
    off to another thread. You just need to use an appropriate
    synchronizer object, such as a ``Queue``.

  * Application containers. The typical database-driven web
    applications makes for the classic case. For example, if you are
    using ModJy, then the database connection pools and thread pools
    are the responsibility of the servlet container. And they are not
    directly observable. (But don't do things like share database
    connections across threads.) Caches and databases then are where
    you will see shared state.

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

Lastly, thread confinement is not perfect in Python, because of the
possibility of introspecting on frame objects. This means your code
can see local variables in other threads, and the objects they point
to. But this is really more of an issue for how optimizable Jython is
when run on the JVM. It won't cause thread safety issues if you don't
exploit this loophole. We will discuss this more in the section on the
Python Memory Model.


Python Memory Model
-------------------

Reasoning about concurrency in Python is easier than in Java. This is
because the memory model is not as surprising to our conventional
reasoning about how programs operate. However, this also means that
Python code sacrifices significant performance to keep it simpler.

Here's why. In order to maximize Java performance, it's allowed for a
CPU to arbitrarily re-order the operations performed by Java code,
subject to the constraints imposed by *happens-before* and
*synchronizes-with* relationships. (The published `Java memory model
<http://java.sun.com/docs/books/jls/third_edition/html/memory.html>`_
goes into more details on these constraints.)

Although such reordering is not visible within a given thread, the
problem is that it's visible to other threads. Of course, this
visibility only applies to changes made to non-local objects; thread
confinement still applies.

In particular, this means you cannot rely on the apparent sequential
ordering of Java code when looking at two or more threads.

Python is different. The fundamental thing to know about
Python, and what we have implemented in Jython, is that setting any
attribute in Python is a volatile write; and getting any
attribute is a volatile read. This is because Python attributes are
stored in dictionaries, and in Jython, this follows the semantics of
the backing ``ConcurrentHashMap``. So ``get`` and ``set`` are
volatile.

So this means that Python code has sequential consistency. Execution
follows the ordering of statements in the code. There are no surprises
here.

And this means that *safe publication* is pretty much trivial in
Python, when compared to Java. Safe publication means the thread safe
association of an object with a name. Because this is always a
memory-fenced operation in Python, your code simply needs to ensure
that the object itself is built in a thread-safe fashion; then publish
it all at once by setting the appropriate variable to this object.

If you need to create module-level objects -- singletons -- then you
should do this in the top-level script of the module so that the
module import lock is in effect.


Conclusion
----------

XXX various recommendations
summarize some stuff, especially around safe publication