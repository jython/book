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
        raise ValueError("%s isn't an integer" % number)
    return remainder == 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
