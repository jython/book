Chapter 3: Operators, Expressions, and Program Flow
+++++++++++++++++++++++++++++++++++++++++++++++++++

Up until this point, we’ve have not yet covered the different means of writing expressions in Python.  The focus of this chapter is to go in depth on each of the ways we can evaluate code, and write meaningful blocks of conditional logic.  We’ll cover the details of each operator that can be used in Python expressions.  This chapter will also cover some topics that have already been discussed in more meaningful detail.



We will begin by discussing details of expressions.  We have already seen some expressions in use while reading through the previous chapters.  Here we will focus more on the internals of operators used to create expressions, and also different types of expressions that we can use.  This chapter will go into further detail on how we can define blocks of code for looping and conditionals.

Types of Expressions
--------------------

An expression in Python is a block of code that produces a result or value.  Most often, we think of expressions that are used to perform mathematical operations within our code.  However, there are a multitude of expressions used for other purposes as well.  In Chapter 2, we covered the details of String manipulation, sequence and dictionary operations, and touched upon working with sets.  All of the operations performed on these objects are forms of expressions in Python.

This chapter will go into detail on how you write and evaluate mathematical expressions, boolean expressions, and augmented assignments.

Mathematical Operations
-----------------------

The Python language of course contains all of your basic mathematical operations.  This section will briefly touch upon each operator that is available for use in Python and how they function.  You will also learn about a few built-in functions which can be used to assist in  your mathematical expressions.  Finally, you’ll see how to use conditionals in the Python language and learn order of evaluation.

Assuming that this is not the first programming language you are learning, there is no doubt that you are at least somewhat familiar with performing mathematical operations within your programs.  Python is no different than the rest when it comes to mathematics, as with most programming languages, performing mathematical computations and working with numeric expressions is straightforward.



==========  =============================================
Operator    Description
==========  =============================================
'+'           Addition
'-'           Subtraction
'*'           Multiplication
/           Division
//          Truncating Division
%           Modulo (Remainder of Division)
\*\*          Power Operator
+var        Unary Plus
-var        Unary Minus
==========  =============================================

Table 3-1:  Numeric Operators

Most of the operators in the table above are easily understood.  However, the truncating division, modulo, power, and unary operators could use some explanation.  Truncating division will automatically truncate a division result into an integer.  Modulo will return the remainder of a division operation.  The power operator does just what you’d expect as it returns the result of the number to the left of the operator multiplied by itself n times, where n represents the number to the right of the operator.  Unary plus and unary minus are used to evaluate positive or negative numbers.  The following set of examples will help to clarify these topics. ::

   # Performing basic mathematical computations

   >>> 10 - 6
   4
   >>> 9 * 7
   63
   >>> 9 / 3
   3
   >>> 10 / 3
   3
   >>> 10 // 3
   3
   >>> 3.14 / 2
   1.57
   >>> 3.14 // 2
   1.0
   >>> 36 / 5
   7
   >>> 36 % 5
   1
   >>> 5**2
   25
   >>> 100**2
   10000
   >>> -10 + 5
   -5
   >>> +5 - 5
   0

There is a new means of division available in Jython 2.5 by importing from __future__.  In a standard division for 2.5 and previous releases, the quotient returned is an integer or the floor of the quotient when arguments are ints or longs.  However, a reasonable approximation of the division is returned if the arguments are floats or complex.  Often times this solution is incorrect as the quotient should be the reasonable approximation or “true division” in any case.  When we import *division* from the __future__ module then we alter the return value of division by causing true division when using the / operator, and floor division when using the // operator.  Since this is going to be the standard in future releases, it is best practice to import from __future__ when performing division in Jython 2.5. ::

   >>> from __future__ import division
   >>> 9/5
   1.8
   >>> 9/4
   2.25
   >>> 9/3
   3.0
   >>> 9//3
   3
   >>> 9//5
   1


As stated at the beginning of the section, there are a number of built-in mathematical functions that are at your disposal.

=================  ===============================================================================
Function           Description
=================  ===============================================================================
abs(var)           Absolute value
pow(x, y)          Used in place of power operator
pow(x,y,modulo)    Ternary power-modulo
round(var[, n])    Returns a value rounded to the nearest 10-n
divmod(x, y)       Returns both the quotient and remainder of division operation
=================  ===============================================================================

Table 3-2:  Mathematical Built-in functions ::

   #  The following code provides some examples for using mathematical built-ins
   >>> abs(9)
   9
   >>> abs(-9)
   9
   >>> divmod(8,4)
   (2, 0)
   >>> pow(8,2)
   64
   >>> pow(8,2,3)
   1
   >>> round(5.67,1)
   5.7
   >>> round(5.67)
   6.0



The bitwise and logical operators as well as the conditional operators can be used to combine and compare logic.  As with the mathematical operators described above, these operators have no significant difference to that of Java.



==========  ====================================
Operator    Description
==========  ====================================
>                          Greater than
<                          Less than
>=                         Greater than or equal
<=                         Less than or equal
!=                         Not equal
==                         Equal
&                          Bitwise and
|                          Bitwise or
^                          Bitwise xor
~                          Bitwise negation
<<                         Shift left
>>                         Shift right
==========  ====================================

Table 3-3: Bitwise and Conditional Operators



Augmented assignment operators are those that combine two or more operations into one.  While augmented assignment can assist in coding concisely, some say that too many such operators can make code more difficult to read.



==========  ===================================
Operator    Description and Logic
==========  ===================================
+=                                   a = a + b
-=                                   a = a – b
\*=                                   a = a * b
/=                                   a = a / b
%=                                   a = a % b
//=                                  a = a // b
\*\*=                                  a = a \*\* b
&=                                   a = a & b
\|=                                   a = a \| b
^=                                   a = a ^ b
>>=                                  a = a >> b
<<=                                  a = a << b
==========  ===================================

Table 3-4:  Augmented Assignment Operators



Boolean Expressions
-------------------

Comparing two or more values or expressions also uses a similar syntax to that of other languages, and the logic is quite the same.  Note that in Python, *True* and *False* are very similar to constants in the Java language.  *True* actually represents the number *1*, and *False* represents the number *0*.  One could just as easily code using 0 and 1 to represent the boolean values, but for readability and maintenance the *True* and *False* “constants” are preferred.  Java developers, make sure that you capitalize the first letter of these two words as you will receive an ugly *NameError* if you do not.



=============  =======  =================================================================
Conditional    Logic
=============  =======  =================================================================
and                     In an *x and y* evaluation, both x and y must evaluate to True
or                      In an *x or y* evaluation, if x is false then y is evaluated.
not                     In a *not x* evaluation, if *not x*, we mean the opposite of x
=============  =======  =================================================================

Table 3-5: Boolean Conditionals

Conversions
-----------



There are a number of conversion functions built into the language in order to help conversion of one data type to another.  While every data type in Jython is actually a class object, these conversion functions will really convert one class type into another.  For the most part, the built-in conversion functions are easy to remember because they are primarily named after the type to which you are trying to convert.

=======================  =======================================================================================================
Function                 Description
=======================  =======================================================================================================
chr(value)               Converts integer to a character
complex(real [,imag])    Produces a complex number
dict(sequence)           Produces a dictionary from a given sequence of (key,value) tuples
eval(string)             Evaluates a string to return an object…useful for mathematical computations
float(value)             Converts to float
frozenset(set)           Converts a set into a frozen set
hex(value)               Converts an integer into a hex string
int(value [, base])      Converts to an integer using a base if a string is given
list(sequence)           Converts a given sequence into a list
long(value [, base])     Converts to a long using a base if a string is given
oct(value)               Converts integer to octal
ord(value)               Converts a character into it’s integer value
repr(value)              Converts object into an expression string.  Same as enclosing expression in reverse quotes ( `x + y`)
set(sequence)            Converts a sequence into a set
str(value)               Converts an object into a string
tuple(sequence)          Converts a given sequence to a tuple
unichr(value)            Converts integer to a Unicode character
=======================  =======================================================================================================

Table 3-6:  Conversion Functions

The following is an example of using the *eval()* functionality as it is perhaps the one conversion function for which an example helps to understand. ::

   # Suppose keyboard input contains an expression in string format (x * y)
   >>> x = 5
   >>> y = 12
   >>> keyboardInput = 'x * y'
   >>> eval(keyboardInput)
   60

Program Flow
------------

The Python programming language has structure that sets it apart from the others.  As you’ve learned in previous references in this book, the statements that make up programs in Python are structured with attention to spacing, order, and technique.  In order to develop a statement in Python, you must adhere to proper spacing techniques throughout the code block.  Convention and good practice adhere to four spaces of indentation per statement throughout the entire program.  Follow this convention along with some control flow and you’re sure to develop some easily maintainable software.

The standard Python if-else conditional statement is used in order to evaluate expressions and branch program logic based upon the outcome.  Expressions that are usable in an if-else statement can consist of any operators we’ve discussed previously.  The objective is to write and compare expressions in order to evaluate to a *True* or *False* outcome.  As shown in Chapter 1, the logic for an *if-else* statement follows one path if an expression evaluates to *True*, or a different path if it evaluates to *False.*

You can chain as many *if-else* expressions together as needed.  The combining *if-else* keyword is *elif*, which is used for every expression in between the first and the last expressions within a conditional statement. ::

   # terminal symbols are left out of this example so that you can see the concise indentation
   pi =3.14
   x = 2.7 * 1.45
   if x == pi:
       print ‘The number is pi’
   elif x > pi:
       print ‘The number is greater than pi’
   else:
       print ‘The number is less than pi’

Another construct that we touched upon in Chapter 1 was the loop.  Every programming language provides looping implementations, and Python is no different.  The Python language provides two main types of loops known as the *while* and the *for* loop.  The *while* loop logic follows the same semantics as the *while* loop in Java.  The loop will continue processing until the expression evaluates to *False*.  At this time the looping ends and that would be it for the Java implementation.  However, in Python the *while * loop construct also contains an *else* clause which is executed when the looping completes. ::

   while True:
       # perform some processing
   else:
       print ‘Processing Complete…’

This *else* clause can come in handy while performing intensive processing so that we can inform the user of the completion of such tasks.  It can also be handy when debugging code.  Also mentioned in Chapter 1 were the *break*, and *continue* statements.  These all come in handy when using any looping construct.  The *break* statement can be used to break out of a loop.  It should be noted that if there are nested loops then the *break* statement will break out of the inner-most loop only, the outer loops will continue to process.  The *continue* statement can be used to break out of the current processing statement and continue the loop from the beginning.  The *continue* can be thought of as a skipping statement as it will cause execution to skip all remaining statements in the block and restart from the beginning (if the loop expression still evaluates to *True* of course). ::

   while x != y:
       # perform some processing
       if x < 0:
           break
   else:
       print ‘The program executed to completion’

In the example above, the program will continue to process until x does not equal y.  However, if at any point during the processing the x variable evaluates less than zero, then the execution stops.  The *else* clause will not be executed if the *break* statement is invoked.  It will only be executed under normal termination of the loop.



The *for* loop can be used on any iterable object.  It will simply iterate through the object and perform some processing during each pass.  Both the *break* and *continue* statements can also be used within the *for* loop.  The *for* statement in Python also differs from the same statement in Java because in Python we also have the *else* clause with this construct.  Once again, the *else* clause is executed when the *for* loop processes to completion without any *break* intervention.  Also, if you are familiar with pre-Java 5 *for* loops then you will love the Python syntax.  In Java 5, the syntax of the *for* statement was adjusted a bit to make it more in line with syntactically easy languages such as Python. ::

   for(x = 0; x <= myList.size(); x++){
       // processing statements iterating through myList
       System.out.println(“The current index is: “ + x);
   }

   x = 0
   for value in myList:
       # processing statements using value as the current item in myList
       print ‘The current index is %i’ % (x)
       x = x + 1

As you can see, the Python syntax is a little easier to understand, but it doesn’t really save too many keystrokes at this point.  We still have to manage the index (x in this case) by ourselves by incrementing it with each iteration of the loop.  However, Python does provide a built-in function that can save us some keystrokes and provides a similar functionality to that of Java with the automatically incrementing index on the *for* loop.  The *enumerate(sequence)* function does just that.  It will provide an index for our use and automatically manage it for us. ::

   >>> myList = ['jython','java','python','jruby','groovy']
   >>> for index, value in enumerate(myList):
   ...     print index, value
   ...
   0 jython
   1 java
   2 python
   3 jruby
   4 groovy


Now we have covered the program flow for conditionals and looping constructs in the Python language.  Note that you can next to any level, and provide as many *if-else* conditionals as you’d like.  However, good programming practice will tell you to keep it as simple as possible or the logic will become too hard to follow.

Example Code
------------

Let’s take a look at an example program that uses some of the program flow which was discussed in this chapter.  The example program simply makes use of an external text file to manage a list of players on a sports team.  You will see how to follow proper program structure and use spacing effectively in this example.  You will also see file utilization in action, along with utiliation of the *raw_input()* function. ::

   playerDict = {}
   saveFile = False
   exitSystem = False
   # Enter a loop to enter inforation from keyboard
   while not exitSystem:
       print 'Sports Team Administration App'
       enterPlayer = raw_input("Would you like to create a team or manage an existing team?\n (Enter 'C' for create, 'M' for manage, 'X' to exit) ")
       if enterPlayer.upper() == 'C':
           exitSystem = False
       # Enter a player for the team
           print 'Enter a list of players on our team along with their position'
           enterCont = 'Y'
           #  While continuing to enter new players, perform the following
           while enterCont.upper() == 'Y':
               name = raw_input('Enter players first name: ')
               position = raw_input('Enter players position: ')
               playerDict[name] = position
               saveFile = True
               enterCont = raw_input("Enter another player? (Press 'N' to exit or 'Y' to continue)")
           else:
               exitSystem = True
      elif enterPlayer.upper() == 'M':
           exitSystem = False
           # Read values from the external file into a dictionary object
           print '\n’
          print 'Manage the Team'
           playerfile = open('players.txt','r')
           for player in playerfile:
               playerList = player.split(':')
               playerDict[playerList[0]] = playerList[1]
           print 'Team Listing'
           print '++++++++++++'
           for i, player in enumerate(playerDict):
               print 'Player %s Name: %s -- Position: %s' %(i, player, playerDict[player])
       else:
           exitSystem = True
   else:
       # Save the external file and close resources
       if saveFile:
           print 'Saving Team Data...'
           playerfile = open('players.txt','w')
           for player in playerDict:
               playerfile.write(player + ':' + playerDict[player] + '\n')
           playerfile.close()


Summary
-------

All programs are constructed out of definitions, statements and expressions.  In this chapter we covered details of creating expressions and using them.  Expressions can be composed of any number of mathematical operators and comparisons.  In this chapter we discussed the basics of using mathematical operators in our programs.  The __future__ division topic introduced us to using features from the __future__.  We then delved into comparisons and comparison operators.

We ended this short chapter by discussing proper program flow and properly learned about the *if* statement as well as how to construct different types of loops in Python.  In the next chapter you will learn how to write functions, and the use of many built-in functions will be discussed.









