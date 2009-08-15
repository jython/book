Chapter 19:  Testing and Continuous Integration
+++++++++++++++++++++++++++++++++++++++++++++++

Nowadays, automated testing is a fundamental activity in software
development. In this chapter you will see a survey of the tools available for
Jython is this field, from common tools used in the Python world to aid with
unit testing to more complex tools available in the Java world which can be
extended or driven using Jython.

Python Testing Tools
====================

UnitTest (PyUnit)
-----------------

First we will take a look at the most classic test tool available in Python:
PyUnit. It follows the conventions of most "xUnit" incarnations: You subclass
from ``TestCase`` class, then optionally override the methods ``setup()`` and
``tearDown()`` which are executed around the test methods, which are all the
methods you define with a name starting with "test". And you can use the
multiple ``assert*()`` methods provided by ``TestCase``. Here is an very simple
test case for the some functions of the built-in math module::

    import math
    import unittest
    
    class TestMath(unittest.TestCase):
        def testFloor(self):
            self.assertEqual(1, math.floor(1.01))
            self.assertEqual(0, math.floor(0.5))
            self.assertEqual(-1, math.floor(-0.5))
            self.assertEqual(-2, math.floor(-1.1))
    
        def testCeil(self):
            self.assertEqual(2, math.ceil(1.01))
            self.assertEqual(1, math.ceil(0.5))
            self.assertEqual(0, math.ceil(-0.5))
            self.assertEqual(-1, math.ceil(-1.1))
    
There are many other assertion methods besides ``assertEqual()``, of
course. Here is a list with the rest of the available assertion methods:

* ``assertNotEqual(a, b)``: The opposite of ``assertEqual()``

* ``assertAlmostEqual(a, b)``: Only used for numeric comparison. It adds a sort
  of tolerance for insignificant differences, by subtracting its first two
  arguments after rounding them to the seventh decimal place, and later
  comparing the result to zero. You can specify a different number of decimal
  places in the third argument. This is useful for comparison of floating point
  numbers.

* ``assertNotAlmostEqual(a, b)``: The opposite of ``assertAlmostEqual()``

* ``assert_(x)``: Accepts a boolean argument expecting it to be ``True``. You can
  use it to write other checks like "greater than", or to check boolean
  functions/attributes (The trailing underscore is needed because ``assert`` is
  a keyword).

* ``assertFalse(x)``. The opposite of ``assert_()``.

* ``assertRaises(exception, callable)``. Used to assert that an exception passed
  as the first argument is thrown when invoking the callable specified as the
  second argument. The rest of arguments passed to assertRaises is passed on to
  the callable.

As an example, let's extend our test of mathematical functions using some of
these other assertion functions::

    import math
    import unittest
    import operator
    
    class TestMath(unittest.TestCase):
            
        # ...
    
        def testMultiplication(self):
            self.assertAlmostEqual(0.3, 0.1 * 3)
    
        def testDivision(self):
            self.assertRaises(ZeroDivisionError, operator.div, 1, 0)
            # The same assertion using a different idiom:
            self.assertRaises(ZeroDivisionError, lambda: 1 / 0)
    
Now, you may be wondering how to run this testcase. The simple answer is to add
the following to the file in which we defined it::

    if __name__ == '__main__':
        unittest.main()

Finally, just run the module. Say, if you wrote all this code on a file named
``test_math.py``, then run::

    $ jython test_math.py

And you will see this output::

    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.005s
    
    OK

Each dot about the dash line represent a successfully ran test. Let see what
happens if we add a test that fails. Change the invocation
``assertAlmostEqual()`` method in ``testMultiplication()`` to use
``assertEqual()`` instead. If you run the module again, you will see the
following output::

    ...F
    ======================================================================
    FAIL: testMultiplication (__main__.TestMath)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_math.py", line 22, in testMultiplication
        self.assertEqual(0.3, 0.1 * 3)
    AssertionError: 0.3 != 0.30000000000000004
    
    ----------------------------------------------------------------------
    Ran 4 tests in 0.030s

    FAILED (failures=1)

As you can see, the last dot is now an "F", and an explanation of the failure is
printed, pointing out that ``0.3`` and ``0.30000000000000004`` are not
equal. The last line also shows the grand total of 1 failure.

By the way, now you can imagine why using ``assertEquals(x, y)`` is better than
``assert_(x == y)``: if the test fails, ``assertEquals()`` provides helpful
information, which ``assert_()`` can't possibly provide. To see this in action,
let's change ``testMultiplication()`` to use ``assert_()``::

    class TestMath(unittest.TestCase):
        
        #...

        def testMultiplication(self):
            self.assert_(0.3 == 0.1 * 3)

If you run the test again, the output will be::

    ...F
    ======================================================================
    FAIL: testMultiplication (__main__.TestMath)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_math.py", line 24, in testMultiplication
        self.assert_(0.3 == 0.1 * 3)
    AssertionError
    
    ----------------------------------------------------------------------
    Ran 4 tests in 0.054s
    
    FAILED (failures=1)

As you can see, now all what we have is the traceback and the "AssertionError"
message. No extra information is provided to help us diagnostic the failure, as
it was the case when we use ``assertEqual()``. That's why all the specialized
``assert*()`` methods are so helpful.

Now, as your application gets bigger, the number of test cases will grow
too. Eventually, you may not want to keep all the tests on one python module,
for maintainability reasons. 

Let's create a new module, named ``test_lists.py`` with the following test
code::

    import unittest
    
    class TestLists(unittest.TestCase):
        def setUp(self):
            self.list = ['foo', 'bar', 'baz']
    
        def testLen(self):
            self.assertEqual(3, len(self.list))
    
        def testContains(self):
            self.assert_('foo' in self.list)
            self.assert_('bar' in self.list)
            self.assert_('baz' in self.list)
    
        def testSort(self):        
            self.assertNotEqual(['bar', 'baz', 'foo'], self.list)
            self.list.sort()
            self.assertEqual(['bar', 'baz', 'foo'], self.list)
                
.. note:: 

   In the previous code you can see an example on a ``setUp()`` method, which
   allows us to avoid repeating the same initialization code on each ``test*()``
   method.

And, restoring our math tests to a good state, the ``test_math.py`` will contain
the following::
 
    import math
    import unittest
    import operator
    
    class TestMath(unittest.TestCase):
        def testFloor(self):
            self.assertEqual(1, math.floor(1.01))
            self.assertEqual(0, math.floor(0.5))
            self.assertEqual(-1, math.floor(-0.5))
            self.assertEqual(-2, math.floor(-1.1))
    
        def testCeil(self):
            self.assertEqual(2, math.ceil(1.01))
            self.assertEqual(1, math.ceil(0.5))
            self.assertEqual(0, math.ceil(-0.5))
            self.assertEqual(-1, math.ceil(-1.1))
    
        def testDivision(self):
            self.assertRaises(ZeroDivisionError, operator.div, 1, 0)
            # The same assertion using a different idiom:
            self.assertRaises(ZeroDivisionError, lambda: 1 / 0)

        def testMultiplication(self):
            self.assertAlmostEqual(0.3, 0.1 * 3)

Now, how do we run, in one pass, tests defined in different modules? One option
is to manually build a *test suite*. A test suite is a simply collection of test
cases (and/or other test suites) which, when ran, will run all the test cases
(and/or test suites) contained by it. Note that a new test case instance is
built for each test method, so suites have already been build under the hood
every time you have run a test module. Our work, then, is to "paste" the suites
together.

Let's build suites using the interactive interpreter. First, import the involved
modules:

    >>> import unittest, test_math, test_lists

Then, we will obtain the test suites for each one of our test modules (which
were implicitly created when running them using the ``unittest.main()``
shortcut), using the ``unittest.TestLoader`` class::

    >>> loader = unittest.TestLoader()
    >>> math_suite = loader.loadTestsFromModule(test_math)
    >>> lists_suite = loader.loadTestsFromModule(test_lists)

Now we build a new suite which combine these suites::

    >>> global_suite = unittest.TestSuite([math_suite, lists_suite])

And finally, we run the suite::

    >>> unittest.TextTestRunner().run(global_suite)
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.010s
    
    OK
    <unittest._TextTestResult run=7 errors=0 failures=0>
    
Or, if you feel like wanting a more verbose output::

    >>> unittest.TextTestRunner(verbosity=2).run(global_suite)              
    testCeil (test_math.TestMath) ... ok
    testDivision (test_math.TestMath) ... ok
    testFloor (test_math.TestMath) ... ok
    testMultiplication (test_math.TestMath) ... ok
    testContains (test_lists.TestLists) ... ok
    testLen (test_lists.TestLists) ... ok
    testSort (test_lists.TestLists) ... ok
    
    ----------------------------------------------------------------------
    Ran 7 tests in 0.020s
    
    OK
    <unittest._TextTestResult run=7 errors=0 failures=0>

Using this low level knowledge about loaders, suites and runner you can easily
write a script to run the tests of any project. Obviously, the details of the
script will vary from project to project depending the way in which you decide
to organize your tests. 

On the other hand, in practice you won't write custom scripts to run all your
tests. Using test tools which do automatic test discovery will be a much
convenient approach. We will look one of them shortly. But first, I must show
you other testing tool very popular in the Python world: doctests.

Doctests
--------

Doctests are a very ingenious combination of, well, documentation and tests. A
doctest is, in essence, no more than a snapshot of a interactive interpreter
session, mixed with paragraphs of documentation, typically inside of a
docstring. Here is a simple example::

    def is_even(number):
        """
        Checks if an integer number is even. 
        
        >>> is_even(0)
        True
        
        >>> is_even(2)
        True
        
        >>> is_even(3)
        False
    
        It works with very long numbers:
        
        >>> is_even(100000000000000000000000000000)
        True
        
        And also with negatives:
        
        >>> is_even(-1000000000000000000000000000001)
        False
        
        But not with floats:
        
        >>> is_even(4.1)
        Traceback (most recent call last):
        ...
        ValueError: 4.1 isn't an integer
        
        However, a value of type float as long as it value is an integer:
        
        >>> is_even(4.0)
        True
        """
        remainder = number % 2
        if 0 < remainder < 1:
            raise ValueError("%f isn't an integer" % number)
        return remainder == 0

Note that, if we weren't talking about testing, we may have thought that the
docstring of ``is_even()`` is just normal documentation, in which the convention
of using the interpreter prompt to mark examples and output was adopted (also
note also that irrelevant stack trace has been striped of in the exception
example). After all, in many cases we use examples as part of the
documentation. Take a look at Java's ``SimpleDateFormat`` documentation located
in http://java.sun.com/javase/6/docs/api/java/text/SimpleDateFormat.html and you
will spot fragments like:

* "...using a pattern of MM/dd/yy and a SimpleDateFormat instance created on
  Jan 1, 1997, the string 01/11/12 would be interpreted as Jan 11, 2012..."

* "...01/02/3 or 01/02/003 are parsed, using the same pattern, as Jan 2, 3 AD..."

* "..."01/02/-3" is parsed as Jan 2, 4 BC..."

The magic of doctests if that it encourages the inclusion of these examples by
doubling them as tests. Let's save our example code as ``even.py`` and add the
following snippet at the end::

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
    
Then, run it::

    $ jython even.py

And well, doctests are a bit shy and don't show any output on success. But to
convince you that it is indeed testing our code, run it with the ``-v`` option::

    $ jython even.py -v

    Trying:
        is_even(0)
    Expecting:
        True
    ok
    Trying:
        is_even(2)
    Expecting:
        True
    ok
    Trying:
        is_even(3)
    Expecting:
        False
    ok
    Trying:
        is_even(100000000000000000000000000000)
    Expecting:
        True
    ok
    Trying:
        is_even(-1000000000000000000000000000001)
    Expecting:
        False
    ok
    Trying:
        is_even(4.1)
    Expecting:
        Traceback (most recent call last):
        ...
        ValueError: 4.1 isn't an integer
    ok
    Trying:
        is_even(4.0)
    Expecting:
        True
    ok
    1 items had no tests:
        __main__
    1 items passed all tests:
       7 tests in __main__.is_even
    7 tests in 2 items.
    7 passed and 0 failed.
    Test passed.

Doctests are a very, very convenient way to do testing, since the interactive
examples can be directly copy-pasted from the interactive shell, transforming
the manual testing in documentation example and automated tests in one shot. 

You don't really *need* to include doctests as part of the documentation of the
feature they test. Nothing stops you to write the following code in, say, the
``test_math_using_doctest.py`` module::

    """
    Doctests equivalent to test_math unittests seen in the previous section.
    
    >>> import math
    
    Tests for floor():
    
    >>> math.floor(1.01)
    1
    >>> math.floor(0.5)
    0
    >>> math.floor(-0.5)
    -1
    >>> math.floor(-1.1)
    -2
    
    Tests for ceil():
    
    >>> math.ceil(1.01)
    2
    >>> math.ceil(0.5)
    1
    >>> math.ceil(-0.5)
    0
    >>> math.ceil(-1.1)
    -1
    
    Test for division:
    
    >>> 1 / 0
    Traceback (most recent call last):
    ...
    ZeroDivisionError: integer division or modulo by zero
   
    Test for floating point multiplication:
 
    >>> (0.3 - 0.1 * 3) < 0.0000001
    True
    
    """
    if __name__ == "__main__":
        import doctest
        doctest.testmod()
    
To take advantage of doctests we have to follow some simple rules, like using
the ``>>>`` prompt and leaving a blank line between sample output and the next
paragraph. But if you think about it, is the same kind of sane rules that makes
the documentation readable by people.

The only common rule not shown by the above example is the way to write
expressions which are written in more than one line. As you may expect, you have
to follow the same convention used by the interactive interpreter: start the
continuation lines with an ellipsis: ``...``. For example::

    """    
    Addition is commutative:

    >>> ((1 + 2) ==
    ...  (2 + 1))
    True
    """

By the way, as you can see on the last test in the previous example, in some
cases doctests are not the most clean way to express a test. And note that, if
that test fails you will *not* get useful information from the failure, as it
will say that the output was ``False`` when ``True`` was expected, without the
extra details ``assertAlmostEquals()`` would give you. The morale of the history
is to realize that doctest is just another tool in the toolbox, which can fit
very well in some cases and not fit well in others.

.. warning::

   A very common temptation that breaks the portability of your doctests across
   Python implementations (e.g. Jython, CPython and IronPython) is the usage of
   dictionary outputs in doctests. The trap here is that *the order of dict keys
   is implementation-dependent*, so the test may pass when working on some
   implementation and fail horribly on others. The workaround is to convert the
   dict to a sequence of tuples and sort them, using ``sorted(mydict.items())``.

   That's the big downfall of doctests: It always does a textual comparison of
   the expression, converting the result to string. It isn't aware of the
   objects structure.

