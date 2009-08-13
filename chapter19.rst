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
	    # Could also be writen as:
            # self.assertRaises(ZeroDivisionError, lambda: 1 / 0)
 
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

