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
convenient approach. We will look one of them very shortly. But first, I must
show you other testing tool very popular in the Python world: doctests.


        
