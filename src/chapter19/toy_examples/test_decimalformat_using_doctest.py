"""
Tests for Java's DecimalFormat

>>> from java.text import DecimalFormat

A format for money:

>>> dolarFormat = DecimalFormat("$ ###,###.##")

The decimal part is only printed if needed:
    
>>> dolarFormat.format(1000)    
u'$ 1.000'

Rounding is used when there are more decimal numbers than those defined by the
format:

>>> dolarFormat.format(123456.789)
u'$ 123.456,79'

The format can be used as a parser:

>>> dolarFormat.parse('$ 123')
123L

The parser ignores the unparseable text after the number:

>>> dolarFormat.parse("$ 123abcd")
123L

However, if it can't parse a number, it throws a ParseException:

>>> dolarFormat.parse("abcd")
Traceback (most recent call last):
...
ParseException: java.text.ParseException: Unparseable number: "abcd"
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()

