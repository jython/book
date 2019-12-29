Chapter 6:  Object Oriented Jython
==================================

This chapter is going to cover the basics of object oriented
programming.  If you're familiar with the concepts.  I'll start with
covering the basic reasons for why you would want to write object
oriented code in the first place, then cover all the basic syntax, and
finally I'll show you a non-trivial example.

Object oriented programming is a method of programming where you
package your code up into bundles of data and behaviour.  In Jython,
you can define a template for this bundle with a class definition
With this first class written, you can then instantiate copies of your
object and have them act upon each other.  This helps you organize
your code into smaller more manageable bundles 

Throughout this chapter, I interchangably use Python and Jython - for
regular object oriented programming - the two dialects of Python are
so similar that there are no meaningful differences between the two
languages.  Enough introduction text though - let's take a look at
some basic syntax to see what this is all about.

Basic Syntax
------------

Writing a class is really simple.  It is fundamentally about managing
some kind of 'state' and exposing some functions to manipulate that
state.  In object jargon - we just call those functions 'methods'.

Let's start by creating a car class.  The goal is to create an object
that will manage it's own location on a two dimensional plane.  We
want to be able to tell it to turn, move forward, and we want to be
able to interrogate the object to find out where it's current location
is. ::

    class Car(object):

        NORTH = 0 
        EAST = 1
        SOUTH = 2 
        WEST = 3

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y
            self.direction = 0

        def turn_right(self):
            self.direction += 1
            self.direction = self.direction % 4

        def turn_left(self):
            self.direction -= 1
            self.direction = self.direction % 4

        def move(self, distance):
            if self.direction == self.NORTH: 
                self.y += distance
            elif self.direction == self.SOUTH:
                self.y -= distance
            elif self.direction == self.EAST:
                self.x += distance
            else:
                self.x -= distance

        def position(self):
            return (self.x, self.y)

We'll go over that class definition in detail but right now, let's
just see how to create a car, move it around and ask the car where it
is. ::

    from car import Car

    def test_car():
        c = Car()
        c.turn_right()
        c.move(5)
        assert (5, 0) ==  c.position()

        c.turn_left()
        c.move(3)

        assert (5, 3) == c.position()

    if __name__ == '__main__':
        test_car()

The best way to think of a class is to think of it like a special kind of
function that acts like a factory that generates object instances. For
each call to the class - you are creating a new discrete copy of your
object.

Once we've created the car instance, we can simply call functions that
are attached to the car class and the object will manage it's own
location.  From the point of view of our test code - we do not need to
manage the location of the car - nor do we need to manage the
direction that the car is pointing in.  We just tell it to move - and
it does the right thing.

Let's go over the syntax in detail to see exactly what's going on
here.

In Line 1, we declare that our Car object is a subclass of the root
"object" class.  Python, like many object oriented languages has a
'root' object that all other objects are based off of.  This 'object'
class defines basic behavior that all classes can reuse.

Python actually has two kinds of classes - 'newstyle' and old style.
The old way of declaring classes didn't require you to type 'object' -
you'll occassionally see the old-style class usage in some Python
code, but it's not consider a good practice   Just subclass 'object'
for any of your base classes and your life will be simpler [1]_.

Lines 3 to 6 declare class attributes for the direction that any car
can point  to.  These are *class* attributes so they can be shared
across all object instances of the car object.

Now for the good stuff.

Line 8-11 declares the object initializer.  In some languages, you
might be familiar with a constructor - in Jython, we have an
initializer which lets us pass values into an object at the time of
creation.  

In our initializer, we are setting the initial position of the car to
(0, 0) on a 2 dimensional plane and then the direction of the car is
initialized to pointing north.  Fairly straight forward so far.

The function signature uses Python's default argument list feature so
we don't have to explicitly set the initial location to (0,0), but
there's a new argument introduced called 'self'. This is a reference
to the current object.

Remember - your class definition is creating instances of objects.
Once your object is created, it has it's own set of internal variables
to manage.  Your object will inevitably need to access these as well
as any of the classes internal methods.  Python will pass a reference
to the current object as the first argument to all your instance
methods.

If you're coming from some other object oriented language, you're
probably familiar with the 'this' variable. Unlike C++ or Java, Python
doesn't magically introduce the reference into the namespace of
accessible variables, but this is consistent with Python's philosophy
of making things explicit for clarity.

When we want to assign the initial x,y position, we just need to
assign values on to the name 'x', and 'y' on the object.  Binding
the values of x and y to self makes the position values accessible to
any code that has access to self - namely the other methods of the
object. One minor detail here - in Python, you can technically
name the arguments however you want.  There's nothing stopping you
from calling the first argument 'this' instead of 'self', but the
community standard is to use 'self' [2]_.

Line 13 to 19 declare two methods to turn the vehicle in different
directions.  Notice how the direction is never directly manipulated by
the caller of the Car object.  We just asked the car to turn, and the
car changed it's own internal 'direction' state.

Line 21 to 29 define where the car should move to when we move the car
forward.  The internal direction variable informs the car how it
should manipulate the x and y position.  Notice how the caller of the
car object never needs to know precisely what direction the car is
pointing in.  The caller only needs to tell the object to turn and
move forward.  The particular details of how that message is used is
abstracted away.

That's not too bad for a couple dozen lines of code.

This concept of hiding internal details is called encapsulation.  This
is a core concept in object oriented programming.  As you can see from
even this simple example - it allows you to structure your code so
that you can provide a simplified interface to the users of your code.

Having a simplified interface means that we could have all kinds of
behaviour happening behind the function calls to turn and move - but
the caller can ignore all those details and concentrate on *using* the
car instead of managing the car. 

As long as the method signatures don't change, the caller really
doesn't need to care about any of that.  We can easily add
persistence to this class - so we can save and load the car's state 
to disk.

First, pull in the pickle module - pickle will let us convert python
objects into byte strings that can be restored to full objects later.

    import pickle

Now, just add two new methods to load and save the state of the object. ::

    def save(self):
        state = (self.direction, self.x, self.y)
        pickle.dump(state, open('mycar.pickle','wb'))

    def load(self):
        state = pickle.load(open('mycar.pickle','rb'))
        (self.direction, self.x, self.y) = state

Simply add calls to save() at the end of the turn and move methods,
and the object will automatically save all the relevant internal
values to disk.

People who use the car object don't even need to know that it's saving
to disk, because the Car object handles it behind the scenes. ::

        def turn_right(self):
            self.direction += 1
            self.direction = self.direction % 4
            self.save()

        def turn_left(self):
            self.direction -= 1
            self.direction = self.direction % 4
            self.save()

        def move(self, distance):
            if self.direction == self.NORTH: 
                self.y += distance
            elif self.direction == self.SOUTH:
                self.y -= distance
            elif self.direction == self.EAST:
                self.x += distance
            else:
                self.x -= distance
            self.save()

Now, when you call the turn, or move methods, the car will
automatically save itself to disk.  If you want to reconstruct the car
object's state from a previously saved pickle file, you can simply
call the load() method.

Object Attribute Lookups
------------------------

If you've beeen paying attention, you're probably wondering how the
NORTH, SOUTH, EAST and WEST variables got bound to self.  We never
actually assigned them to the self variable during object
initialization - so what's going on when we call move()?  How is
Jythpon actually resolving the value of those four variables?

Now seems like a good time to show how Jython resolves name lookups.

The direction names actually got bound to the Car class.  The Jython
object system does a little bit of magic when you try accessing any
*name* against an object, it first searches for anything that was
bound to 'self'.  If python can't resolve any attribute on self with
that name, it goes up the object graph to the class definition.  The
direction attributes NORTH, SOUTH, EAST, WEST were bound to the class
definition - so the name resolution succeeds and we get the value of
the class attribute.

An very short example will help clarify this  ::

    >>> class Foobar(object):
    ...   def __init__(self):
    ...     self.somevar = 42
    ...   class_attr = 99
    ... 
    >>> 
    >>> obj = Foobar()
    >>> obj.somevar
    42
    >>> obj.class_attr
    99
    >>> obj.not_there
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Foobar' object has no attribute 'not_there'
    >>> 

So the key difference here is *what* you bind a value to.  The values
you bind to self are available only to a single object.  Values you
bind to the class definition are available to all instances of the
class.  The sharing of class attributes among all instances is a
critical distinction because mutating a class attribute will affect
all instances.  This may cause unintended side effects if you're not
paying attention as a variable may change value on you when you aren't
expecting it to. ::

    >>> other = Foobar()
    >>> other.somevar
    42
    >>> other.class_attr
    99
    >>> # obj and other will have different values for somevar
    >>> obj.somevar = 77
    >>> obj.somevar         
    77
    >>> other.somevar
    42
    >>> # Now show that we have the same copy of class_attr
    >>> other.class_attr = 66
    >>> other.class_attr
    66
    >>> obj.class_attr
    66

I think it's important to stress just how transparent Python's object
system really is.  Object attributes are just stored in a plain python
dictionary.  You can directly access this dictionary by looking at the
__dict__ attribute. ::

    >>> obj = Foobar()
    >>> obj.__dict__
    {'somevar': 42}

Notice that there are no references to the methods of the class, or
the class attribute.  I'll reiterate it again - Python is going to
just go up your inheritance graph - and go to the class definition to
look for the methods of Foobar and the class attributes of foobar.

The same trick can be used to inspect all the attributes of the class,
just look into the __dict__ attribute of the class definition and
you'll find your class attributes and all the methods that are
attached to your class definition ::

    >>> Foobar.__dict__
    {'__module__': '__main__', 
        'class_attr': 99, 
        '__dict__': <attribute '__dict__' of 'Foobar' objects>, 
        '__init__': <function __init__ at 1>}

This transparency can be leveraged with dynamic programming techniques
using closures and binding new functions into your class definition at
runtime.  We'll revisit this later in the chapter when we look at
generating function dynamically and finally with a short introduction
to metaprogramming.

Inheritance and Overloading
---------------------------

In the car example, we subclass from the root object type.  You can
also subclass your own classes to specialize the behaviour of your
objects.  You may want to do this if you notice that your code
naturally has a structure where you have many different classes that
all share some common behaviour.

With objects, you can write one class, and then reuse it using
inheritance to automatically gain access to the pre-existing behavior
and attributes of the parent class.  Your 'base' objects will inherit
behaviour from the root 'object' class, but any subsequent subclasses
will inherit from your own classes.

Let's take a simple example of using some animal classes to see how
this works. Define a module "animals.py" with the following code:

    class Animal(object):
        def sound(self):
            return "I don't make any sounds"

    class Goat(Animal):
        def sound(self):
            return "Bleeattt!"

    class Rabbit(Animal):
        def jump(self):
            return "hippity hop hippity hop"

    class Jackalope(Goat, Rabbit):
        pass

Now you should be able to explore that module with the jython
interpreter:

    >>> from animals import *
    >>> animal = Animal()
    >>> goat = Goat()
    >>> rabbit = Rabbit()
    >>> jack = Jackalope()

    >>> animal.sound()
    "I don't make any sounds"
    >>> animal.jump()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Animal' object has no attribute 'jump'

    >>> rabbit.sound()
    "I don't make any sounds"
    >>> rabbit.jump()
    'hippity hop hippity hop'

    >>> goat.sound()
    'Bleeattt!'
    >>> goat.jump()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Goat' object has no attribute 'jump'

    >>> jack.jump()
    'hippity hop hippity hop'
    >>> jack.sound()
    'Bleeattt!'

Inheritance is a very simple concept, when you declare your class, you
simply specify which parent classes you would like to reuse.  Your new
class can then automatically access all the methods and attributes of
the super class.  Notice how the goat couldn't jump and the rabbit
couldn't make any sound, but the Jackalope had access to methods from
both the rabbit and the goat.

With single inheritance - when your class simply inherits from one
parent class - the rules for resolving where to find an attribute or a
method are very straight forward.  Jython just looks up to the parent if
the current object doesn't have a matching attribute.  

It's important to point out now that the Rabbit class is a type of
Animal - the Python runtime can tell you that programmatically by
using the isinstance function ::

    >>> isinstance(bunny, Rabbit)
    True
    >>> isinstance(bunny, Animal)
    True
    >>> isinstance(bunny, Goat)
    False

For many classes, you may want to extend the behavior of the parent
class instead of just completley overriding it.  For this, you'll want
to use the super().  Let's specialize the Rabbit class like this. ::

    class EasterBunny(Rabbit): 
        def sound(self): 
            orig = super(EasterBunny, self).sound() 
            return "%s - but I have eggs!" % orig 

If you now try making this rabbit speak, it will extend the original
sound() method from the base Rabbit class ::

    >>> bunny = EasterBunny() 
    >>> bunny.sound()
    "I don't make any sounds - but I have eggs!"

That wasn't so bad.  For these examples, I only demonstrated that
inherited methods can be invoked, but you can do exactly the same
thing with attributes that are bound to the self.

For multiple inheritance, things get very tricky.  In fact, the rules
for resolving how attributes are looked up would easily fill an entire
chapter (look up "The Python 2.3 Method Resolution Order" on Google if
you don't believe me). There's not enough space in this chapter to
properly cover the topic which should be a good indication to you that
you really don't want to use multiple inheritance.

More advanced abstraction
-------------------------

Abstraction using plain classes is wonderful and all, but it's even
better if your code seems to naturally fit into the syntax of the
language.  Python supports a variety of underscore methods - methods
that start and end with double "_" signs that let you overload the
behaviour of your objects.  This means that your objects will seem to
integrate more tightly with the language itself.

With the underscore methods, you can give you objects behaviour for
logical and mathematical operations.  You can even make your objects
behave more like standard builtin types like lists, sets or
dictionaries.

    from __future__ import with_statement
    from contextlib import closing

    with closing(open('simplefile','w')) as fout:
        fout.writelines(["blah"])

    with closing(open('simplefile','r')) as fin:
        print fin.readlines()

The above snippet of code just opens a file, writes a little bit of
text and then we just read the contents out.  Not terriblly exciting.
Most objects in Python are serializable to strings using the pickle
module.  We can leverage pickle to write out full blown objects to
disk.  Let's see the functional version of this: ::

    from __future__ import with_statement
    from contextlib import closing
    from pickle import dumps, loads

    def write_object(fout, obj):
        data = dumps(obj)
        fout.write("%020d" % len(data))
        fout.write(data)

    def read_object(fin):
        length = int(fin.read(20))
        obj = loads(fin.read(length))
        return obj

    class Simple(object):
        def __init__(self, value):
            self.value = value
        def __unicode__(self):
            return "Simple[%s]" % self.value

    with closing(open('simplefile','wb')) as fout:
        for i in range(10):
            obj = Simple(i)
            write_object(fout, obj)

    print "Loading objects from disk!"
    print '=' * 20

    with closing(open('simplefile','rb')) as fin:
        for i in range(10):
            print read_object(fin)

This should output something like this: ::

    Loading objects from disk!
    ====================
    Simple[0]
    Simple[1]
    Simple[2]
    Simple[3]
    Simple[4]
    Simple[5]
    Simple[6]
    Simple[7]
    Simple[8]
    Simple[9]

So now we're doing something interesting.  Let's look at exactly what
happening here.

First, you'll notice that the Simple object is rendering a nice - the
Simple object can render itself using the __unicode__ method.  This is
clearly an improvement over the earlier rendering of the object with angle
brackets and a hex code.

The write_object function is fairly straight forward, we're just
converting our objects into strings using the pickle module, computing
the length of the string and then writing the length and the actual
serialized object to disk.

This is fine, but the read side is a bit clunky. We don't really know
when to stop reading.  We can fix this using the iteration protocol.
Which bring us to one of my favourite reasons to use objects at all in
Python.  

Protocols
---------

In Python, we have 'duck typing'.  If it sounds like a duck, quacks
like a duck and looks like a duck - well - it's a duck. This is in
stark contrast to more rigid languagse like C# or Java which have
formal interface definitions.  One of the nice benefits of having duck
typing is that Python has the notion of object 'protocols'.

If you happen to implement the right methods - python will recognize
your object as a certain type of 'thing'.

Iterators are objects that look like lists that let you read the next
object.  Implementing an iterator protocol is straight forward - just
implement a next() method and a __iter__ method and you're ready to
rock and roll.  Let's see this in action: ::

    class PickleStream(object):
        """
        This stream can be used to stream objects off of a raw file stream
        """
        def __init__(self, file):
            self.file = file

        def write(self, obj):
            data = dumps(obj)
            length = len(data)
            self.file.write("%020d" % length)
            self.file.write(data)

        def __iter__(self):
            return self

        def next(self):
            data = self.file.read(20)
            if len(data) == 0:
                raise StopIteration
            length = int(data)well
            return loads(self.file.read(length))

        def close(self):
            self.file.close()

The above class will let you wrap a simple file object and you can now
send it raw python objects to write to a file, or you can read objects
out as if the stream was just a list of objects.  Writing and reading
becomes much simpler ::

    with closing(PickleStream(open('simplefile','wb'))) as stream:
        for i in range(10):
            obj = Simple(i)
            stream.write(obj)

    with closing(PickleStream(open('simplefile','rb'))) as stream:
        for obj in stream:
            print obj

Abstracting out the details of serialization into the PickleStream
lets us 'forget' about the details of how we are writing to disk.  All
we care about is that the object will do the right thing when we call
the write() method.

The iteration protocol can be used for much more advanced uses, but
even with this example, it should be obvious how useful it is.  While
you could implement the reading behaviour with a read() mo loethod, just
using the stream as something you can loop over makes the code much
easier to understand.

An aside a common problem that everyone seems to have
-----------------------------------------------------

One particular snag that seems to catch every python programmer is
when you use default values in a method signature. ::

    >>> class Tricky(object):
    ...   def mutate(self, x=[]):
    ...     x.append(1)
    ...     return x
    ... 
    >>> obj = Tricky()
    >>> obj.mutate()
    [1]
    >>> obj.mutate()
    [1, 1]
    >>> obj.mutate()
    [1, 1, 1]

What's happening here is that the instance method 'mutate' is an
object.  The method object stores the default value for 'x' in an
attribute *inside* the method object.  So when you go and mutate the
list, you're actually changing the value of an attribute of the method
itself.   Remember - this happens because when you invoke the mutate
method, you're just accessing a callable attribute on the Tricky
object.

Runtime binding of methods
--------------------------

One interesting feature in Python is that instance methods are
actually just attributes hanging off of the class defintion - the
functions are just attributes like any other variable, except that
they happen to be 'callable'.

It's even possible to create and bind in functions to a class
definition at runtime using the new module to create instance methods.
In the following example, you can see that it's possible to define a
class with nothing in it, and then bind methods to the class
definition at runtime. ::

    >>> def some_func(self, x, y):
    ...   print "I'm in object: %s" % self
    ...   return x * y
    ... 
    >>> import new
    >>> class Foo(object): pass
    ... 
    >>> f = Foo()
    >>> f
    <__main__.Foo object at 0x1>
    >>> Foo.mymethod = new.instancemethod(some_func, f, Foo)
    >>> f.mymethod(6,3)
    I'm in object: <__main__.Foo object at 0x1>
    18

When you invoke the 'mymethod' method, the same attribute lookup
machinery is being invoked.  Python looks up the name against the
'self' object.  When it can't find anything there, it goes to the
class definition.  When it finds it there, the instancemethod object
is returned.  The function is then caled with two arguments and you
get to see the final result. 

This kind of dynamism in Jython is extremely powerful.  You can write
code that generates functions at program runtime and then bind those
functions to objects. You can do all of this because in Jython,
classes are what are known as 'first class objects'.  The class
definition itself is an actual object  - just like any other object.
Manipulating classes is as easy as manipulating any other object.

Closures and Passing Objects
----------------------------

Python supports the notion of nested scopes - this can be used by to
preserve some state information inside of another function.  This
technique isn't all that common outside of dynamic languages, so you
may have never seen this before.  Let's look at a simple example ::

    def adder(x):
        def inner(y):
            return x + y
        return inner

    >>> func = adder(5)
    >>> func
    <function inner at 0x7adf0>
    >>> func(8)
    13

This is pretty cool - we can actually create functions from templates of other
functions.  If you can think of a way to parameterize the behavior of a
function, it becomes possible to create new functions dynamically.
You can think of currying as yet another way of creating templates -
this time you are creating a template for new functions.

This is a tremendously powerful tool once you gain some experience
with it.  Remember - everything in python is an object - even
functions are first class objects in Python so you can pass those in
as arguments as well.  A practical use of this is to partially
construct new functions from 'base' functions with some basic known
behavior.

Let's take the previous adder closure and convert it to a more general
form ::

    def arith(math_func, x):
        def inner(y):
            return math_func(x, y)
        return inner

    def adder(x, y):
        return x + y

    >>> func = arith(adder, 91)
    >>> func(5)
    96

This technique is called currying - you're now creating new function
objects based on previous functions. The most common use for this is
to create decorators.  In Python, you can define special kinds of
objects that wrap up your methods and add extra behavior.  Some
decorators are builtin already like 'property', 'classmethod' and
'staticmethod'.  Once you have a decorator, you can sprinkle it on to
of another function to add new behavior.

Decorator syntax looks something like this ::

    @decorator_func_name(arg1, arg2, arg3, ...)
    def some_functions(x, y, z, ...):
        # Do something useful here
        pass

Suppose we have some method that requires intensive computational
resoures to run, but the results do not vary much over time.  Wouldn't
it be nice if we could cache the results so that the computation
wouldn't have to run each and every time? 

Here's our class with a slow computation method ::

    import time
    class Foobar(object): 
        def slow_compute(self, *args, **kwargs): 
            time.sleep(1) 
            return args, kwargs, 42 

Now let's cache the value using a decorator function.  Our strategy
is that for any function named X with some argument list, we want to
create a unique name and save the final computed value to that name.
We want our cached value to have a human readable name, we we want to
reuse the original function name, as well as the arguments that were
passed in the first time.

Let's get to some code! ::

    import hashlib
    def cache(func):
        """ 
        This decorator will add a _cache_functionName_HEXDIGEST
        attribute after the first invocation of an instance method to
        store cached values.
        """
        # Obtain the function's name
        func_name = func.func_name 
        # Compute a unique value for the unnamed and named arguments
        arghash = hashlib.sha1(str(args) + str(kwargs)).hexdigest()
        cache_name = '_cache_%s_%s' % (func_name, arghash)
        def inner(self, *args, **kwargs):
            if hasattr(self, cache_name):
                # If we have a cached value, just use it
                print "Fetching cached value from : %s" % cache_name
                return getattr(self, cache_name)
            result = func(self, *args, **kwargs)
            setattr(self, cache_name, result)
            return result
        return inner

There are only two new tricks that are in this code.

1) I'm using the hashlib module to convert the arguments to the
   function into a unique single string.
2) The use of getattr, hasattr and setattr to manipulate the cached
   value on the instance object.

Now, if we want to cache the slow method, we just throw on a @cache
line above the method declaration. ::

    @cache
    def slow_compute(self, *args, **kwargs): 
        time.sleep(1) 
        return args, kwargs, 42 

Fantastic - we can reuse this cache decorator for any method we want
now.  Let's suppose now that we want our cache to invalidate itself after
every 3 calls.  This practical use of currying is only a slight
modification to the original caching code. ::

    import hashlib
    def cache(loop_iter):
        def function_closure(func):
            func_name = func.func_name
            def closure(self, loop_iter, *args, **kwargs):
                arghash = hashlib.sha1(str(args) + str(kwargs)).hexdigest()
                cache_name = '_cache_%s_%s' % (func_name, arghash)
                counter_name = '_counter_%s_%s' % (func_name, arghash)
                if hasattr(self, cache_name):
                    # If we have a cached value, just use it
                    print "Fetching cached value from : %s" % cache_name
                    loop_iter -= 1
                    setattr(self, counter_name, loop_iter)
                    result = getattr(self, cache_name)
                    if loop_iter == 0:
                        delattr(self, counter_name)
                        delattr(self, cache_name)
                        print "Cleared cached value"
                    return result
                result = func(self, *args, **kwargs)
                setattr(self, cache_name, result)
                setattr(self, counter_name, loop_iter)
                return result
            return closure
        return function_closure

Now we're free to use @cache for any slow method and caching will
come in for free - including automatic invalidation of the cached
value.  Just use it like this ::

    @cache(10)
    def slow_compute(self, *args, **kwargs): 
        # TODO: stuff goes here...
        pass

Review - and a taste of how we could fit all of this together
-------------------------------------------------------------

Now - I'm going to ask you to use your imagination a litte.  We've
covered quite a bit of ground really quickly.  

We can :

 * look up attributes in an object (use the __dict__ attribute).  
 * check if an object belongs to a particular class hierarchy (use the isinstance function).  
 * build functions out of other functions using currying.and even bind those functions to arbitrary names

This is fantastic - we now have all the basic building blocks we need
to generate complex methods based on the attributes of our class.
Imagine a simplified addressbook application with a simple contact. ::

    class Contact(object):
        first_name = str
        last_name = str
        date_of_birth = datetime.Date

Assuming we know how to save and load to a database, we can use the
function generation techniques to automatically generate load() and
save() methods and bind them into our Contact class.  We can use our
introspection techniques to determine what attributes need to be saved
to our database.  We could even grow special methods onto our Contact
class so that we could iterate over all of the class attributes and
magically grow 'searchby_first_name' and 'searchby_last_name' methods.

See how powerful this can be?  We can write extremly minimal code, and
we could code generate all of our required specialized behavior for
saving, loading and searching for records in a database.  Since we do
all of that programmatically - we can dramatically reduce the amount
of code that we have to write by hand and by doing so - we can redue
the chance that we introduce bugs into our system.

We're going to do exactly that in a later chapter. Build a simple
database abstraction layer to demonstrate how to create your own
object system that will automatically know how to read and write to a
database. 

.. Footnotes

.. [1] New style classes provide a large number of useful features that simply aren't available to old-style classes.  If you end up mixing old and new style classes together, you'll usually get unexpected behaviour that will surprise you - and not in the good way.  It'll surprise you in the kind of way that will keep you up late at night wondering why your code doesn't work and you'll curse the fact that both styles of classes exist at all.

.. [2] One of Python's strengths is legibility - of your code and other code.  Community standards help the legibility of code tremendously.
