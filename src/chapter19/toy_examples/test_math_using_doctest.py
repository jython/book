"""
Doctests equivalent to test_math unittests seen in the previous section

>>> import math

Tests for floor():

>>> math.floor(1.01)
1.0
>>> math.floor(0.5)
0.0
>>> math.floor(-0.5)
-1.0
>>> math.floor(-1.1)
-2.0

Tests for ceil():

>>> math.ceil(1.01)
2.0
>>> math.ceil(0.5)
1.0
>>> math.ceil(-0.5)
-0.0
>>> math.ceil(-1.1)
-1.0

Test for division:

>>> 1 / 0
Traceback (most recent call last):
...
ZeroDivisionError: integer division or modulo by zero

>>> (0.3 - 0.1 * 3) < 0.0000001
True

"""
if __name__ == "__main__":
    import doctest
    doctest.testmod()
