Chapter 5: Exception Handling and Debugging
+++++++++++++++++++++++++++++++++++++++++++

Any good program makes use of a language’s exception handling mechanisms.  There is no better way to frustrate an end-user then by having them run into an issue with your software and displaying a big ugly error message on the screen, followed by a program crash.  Exception handling is all about ensuring that when your program encounters an issue, it will continue to run and provide informative feedback to the end-user or program administrator.  Any Java programmer becomes familiar with exception handling on day one, as some Java code won’t even compile unless there is some form of exception handling put into place via the try-catch-finally syntax.  Python has similar constructs to that of Java, and we’ll discuss them in this chapter.



After you have found an exception, or preferably before your software is distributed, you should go through the code and debug it in order to find and repair the erroneous code.  There are many different ways to debug and repair code; we will go through some debugging methodologies in this chapter.  In Python as well as Java, the *assert* keyword can help out tremendously in this area.  We’ll cover *assert* in depth here and learn the different ways that it can be used to help you out and save time debugging those hard-to-find errors.

Exception Handling Syntax and Differences with Java
===================================================

Java developers are very familiar with the *try-catch-finally* block as this is the main mechanism that is used to perform exception handling.  Python exception handling differs a bit from Java, but the syntax is fairly similar.  However, Java differs a bit in the way that an exception is *thrown* in code.  Now, realize that I just used the term *throw* …this is Java terminology.  Python does not *throw* exceptions, but instead it *raises* them.  Two different terms which mean basically the same thing.  In this section, we’ll step through the process of handling and raising exceptions in Python code, and show you how it differs from that in Java.

For those who are unfamiliar, I will show you how to perform some exception handling in the Java language.  This will give you an opportunity to compare the two syntaxes and appreciate the flexibility that Python offers.::

	try {
	    // perform some tasks that may throw an exception
	} catch (ExceptionType messageVariable) {
	    // perform some exception handling
	} finally {
	    // execute code that must always be invoked
	}


Now let’s go on to learn how to make this work in Python.  Not only will we see how to handle and raise exceptions, but you’ll also learn some other great techniques later in the chapter.

Catching Exceptions
-------------------

How often have you been working in a program and performed some action that caused the program to abort and display a nasty error message?  It happens more often than it should because most exceptions can be caught and handled nicely.  By nicely, I mean that the program will not abort and the end user will receive a descriptive error message stating what the problem is, and in some cases how it can be resolved.  The exception handling mechanisms within programming languages were developed for this purpose.  

Below is a table of all exceptions that are built into the Python language along with a description of each.  You can write any of these into a clause and try to handle them.  Later in this chapter I will show you how you and 	 them if you’d like.  Lastly, if there is a specific type of exception that you’d like to throw that does not fit any of these, then you can write your own exception type object.


================================  =================================================================
Exception                         Descripton                                                            
================================  =================================================================
BaseException                     This is the root exception for all others                             
   GeneratorExit                  Raised by close() method of generators for terminating iteration      
   KeyboardInterrupt              Raised by the interrupt key                         
   SystemExit                     Program exit                                                          
   Exception                      Root for all non-exiting exceptions                                   
     StopIteration                Raised to stop an iteration action                                    
     StandardError                Base class for all built-in exceptions              
      ArithmeticError             Base for all arithmetic exceptions                  
         FloatingPointError       Raised when a floating-point operation fails        
         OverflowError            Arithmetic operations that are too large            
         ZeroDivisoinError        Division or modulo operation with zero is divisor   
      AssertionError              Used when an assert statement fails                 
      AttributeError              Attribute reference or failure to assign correctly  
      EnvironmentError            An error occurred outside of Python                 
         IOError                  Error in Input/Output operation                                       
         OSError                  An error occurred in the os module                                    
      EOFError                    input() or raw_input() tried to read past the end of a file           
      ImportError                 Import failed to find module or name                                  
      LookupError                 Base class for IndexError and KeyError                                
         IndexError               A sequence index goes out of range                                    
         KeyError                 Referenced a non-existent mapping (dict) key                          
      MemoryError                 Memory exhausted                                    
      NameError                   Failure to find a local or global name                                
         UnboundLocalError        Unassigned local variable is referenced             
      ReferenceError              Attempt to access a garbage-collected object        
      RuntimeError                Obsolete catch-all error                            
          NotImplementedError     Raised when a feature is not implemented            
      SyntaxError                 Parser encountered a syntax error                                     
         IndentationError         Parser encountered an indentation issue
            TabError              Incorrect mixture of tabs and spaces
      SystemError                 Non-fatal interpreter error
      TypeError                   Inappropriate type was passed to a built-in operator or function      
      ValueError                  Argument error not covered by TypeError or a more precise error       
      Warning                     Base for all warnings                                                 
================================  =================================================================

The *try-except-finally* block is used in Python programs to perform the exception-handling task.  Much like that of Java,
code that may or may not raise an exception should be placed in the *try* block.  Differently though, exceptions that may be
caught go into an *except* block much like the Java *catch* equivalent.  Any tasks that must be performed no matter if an exception
is thrown or not should go into the *finally* block.

try-except-finally Logic ::

    try:                             
        # perform some task that may raise an exception                                                                                                                                                              
    except Exception, value:         
        # perform some exception handling                                                                                                                                                                            
    finally:                         
        # perform tasks that must always be completed                                                                                                                                                                
                                 
Python also offers an optional *else* clause to create the *try-except-else* logic.  This optional code placed inside the
*else* block is run if there are no exceptions found in the block.                    
                                 
try-finally logic:  ::

    try:                             
        # perform some tasks that may raise an exception                                                                                                                                                             
    finally:                         
        # perform tasks that must always be completed                                                                                                                                                                
                                 
try-except-else logic: ::

    try:                             
        # perform some tasks that may raise an exception                                                                                                                                                             
    except:                          
        # perform some exception handling                                                                                                                                                                            
    else:                            
        # perform some tasks that should only be performed if no exceptions are thrown                                                                                                                               
                                 
You can name the specific type of exception to catch within the *except* block , or you can generically define an exception
handling block by not naming any exception at all.  Best practice of course states that you should always try to name
the exception and then provide the best possible handling solution for the case.  After all, if the program is simply
going to spit out a nasty error then the exception handling block does not help resolve the issue at all.  However, there
are some rare cases where it would be advantageous to not explicitly refer to an exception type when we simply wish to
ignore errors and move on.  The *except* block also allows us to define a variable to which the exception message will
be assigned.  This allows us the ability to store that message and display it somewhere within our exception handling code
block.  If you are calling a piece of Java code from within Jython and the Java code throws an exception, it can be handled
within Jython in the same manner as Jython exceptions.  
                                 
Example 5-1:  Exception Handling in Python ::


    # Code without an exception handler                                                                                                                                                                              
    >>> x = 10                       
    >>> z = x / y                    
    Traceback (most recent call last):                                                                                                                                                                               
      File "<stdin>", line 1, in <module>                                                                                                                                                                            
    NameError: name 'y' is not defined                                                                                                                                                                               
                                     
    # The same code with an exception handling block                                                                                                                                                                 
    >>> x = 10                       
    >>> try:                         
    ...     z = x / y                
    ... except NameError, err:       
    ...     print "One of the variables was undefined: ", err                                                                                                                                                        
    ...
    
    One of the variables was undefined:  name 'y' is not defined
    
    
Take note of the syntax that is being used for defining the variable that holds the error message.
Namely, the *except ExceptionType, value* statement syntax in Python and Jython 2.5 differs from that beyond 2.5.
In Python 2.6, the syntax changes a bit in order to ready developers for Python 3, which exclusively uses the new syntax.
Without going off topic too much, I think it is important to take note that this syntax will be changing in future
releases of Jython.                                                                                                                                                                                                                             
                                 
Jython and Python 2.5 and Prior  ::
    
    try:                             
        // code                      
    except ExceptionType, messageVar:
        // code                      
                                 
Jython 2.6 (Not Yet Implemented) and Python 2.6 and Beyond  ::

    try:                             
        // code                      
    except ExceptionType as messageVar:                                                                                                                                                                              
        // code                      
                                 
We had previously mentioned that it was simply bad programming practice to not explicitly name an exception type
when writing exception handling code.  This is true, however Python provides us with another means to obtain the
type of exception that was thrown.  There is a function provided in the *sys* package known as *sys.exc_info()*
that will provide us with both the exception type and the exception message.  This can be quite useful if we are
wrapping some code in a *try-except* block but we really aren’t sure what type of exception may be thrown.  Below
is an example of using this technique.

Example 5-2:  Using sys.exc_info()    ::

    # Perform exception handling without explicitly naming the exception type                                                                                                                                        
    >>> x = 10                       
    >>> try:                         
    ...     z = x / y                
    ... except:                      
    ...     print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]                                                                                                                                         
    ...                              
    Unexpected error:  <type 'exceptions.NameError'> name 'y' is not defined                                                                                                                                         

Sometimes you may run into a situation where it is applicable to catch more than one exception.  Python offers a
couple of different options if you need to do such exception handling.  You can either use multiple *except­ clauses*,
which does the trick and works well, but may become too wordy.  The other option that you have is to enclose your
exception types within parentheses and separated by commas on your *except* statement.  Take a look at the following
example that portrays the latter approach using the same example from *Example 5-1.*

Example 5-3:  Handling Multiple Exceptions    ::

    # Catch NameError, but also a ZeroDivisionError in case a zero is used in the equation                                                                                                                           
    >>> x = 10                       
    >>> try:                         
    ...     z = x / y                
    ... except (NameError,ZeroDivisionError),  err:                                                                                                                                                                  
    ...     print "One of the variables was undefined: ", err                                                                                                                                                        
    ...                              
    One of the variables was undefined:  name 'y' is not defined                                                                                                                                                     
                                 
                                 
    # Using mulitple except clauses  
    >>> x = 10                       
    >>> y = 0                        
    >>> try:                         
    ...     z = x / y                
    ... except NameError, err1:      
    ...     print err1               
    ... except ZeroDivisionError, err2:                                                                                                                                                                              
    ...     print 'You cannot divide a number by zero!'                                                                                                                                                              
    ...                              
    You cannot divide a number by zero!                                                                                                                                                                              
 
The *try-except­* block can be nested as deep as you’d like.  In the case of nested exception handling blocks,
if an exception is thrown then the program control will jump out of the inner most block that received the error,
and up to the block just above it.  This is very much the same type of action that is taken when you are working
in a nested loop and then run into a *break* statement, your code will stop executing and jump back up to the outer
loop.  The following example shows an example for such logic.

Example 5-4:  Nested Exception Handling Blocks ::

    # Perform some division on numbers entered by keyboard                                                                                                                                                           
     try:                            
         # do some work              
         try:                        
             x = raw_input ('Enter a number for the dividend:  ')                                                                                                                                                    
             y = raw_input('Enter a number to divisor: ')                                                                                                                                                            
             x = int(x)              
             y = int(y)              
         except ValueError, err2:    
             # handle exception and move to outer try-except                                                                                                                                                         
             print 'You must enter a numeric value!'                                                                                                                                                                 
         z = x / y                   
     except ZeroDivisionError, err1: 
        # handle exception           
         print 'You cannot divide by zero!'                                                                                                                                                                          
     except TypeError, err3:         
         print 'Retry and only use numeric values this time!'                                                                                                                                                        
     else:     print 'Your quotient is: %d' % (z)                                                                                                                                                                    
                                     
Raising Exceptions               
------------------

Often times you will find reason to raise your own exceptions.  Maybe you are expecting a certain type
of keyboard entry, and a user enters something incorrectly that your program does not like.  This would
be a case when you’d like to raise your own exception.  The *raise* statement can be used to allow you to
raise an exception where you deem appropriate.  Using the *raise* statement, you can cause any of the Python
exception types to be raised, you could raise your own exception that you define (discussed in the next section),
or you could raise a string exception.  The *raise* statement is analogous to the *throw* statement in the
Java language.  In Java we may opt to throw an exception if necessary.  However, Java also allows you to
apply a *throws* clause to a particular method if an exception may possibly be thrown within instead of
using try-catch handler in the method.  Python does not allow you do perform such techniques using the
*raise* statement.

raise Statement Syntax ::

    raise ExceptionType or String[, message[, traceback]]                                                                                                                                                            
                                 
As you can see from the syntax, using *raise* allows you to become creative in that you could use your own
string when raising an error.  However, this is not really looked upon as a best practice as you should try
to raise a defined exception type if at all possible.  You can also provide a short message explaining the
error.  This message can be any string.  Lastly, you can provide a *traceback* via use of *sys.exc_info()*.
Now you’ve surely seen some exceptions raised in the Python interpreter by now.  Each time an exception is
raised, a message appears that was created by the interpreter to give you feedback about the exception and
where the offending line of code may be.  There is always a *traceback* section when any exception is raised.
This really gives you more information on where the exception was raised.

Example 5-5: Using the raise Statement ::

    >>> raise TypeError,"This is a special message"                                                                                                                                                                  
    Traceback (most recent call last):                                                                                                                                                                               
      File "<stdin>", line 1, in <module>                                                                                                                                                                            
    TypeError: This is a special message                                                                                                                                                                             
                                 
Defining Your Own Exceptions
============================

You can define your own exceptions in Python by creating an exception class.  Now classes are a topic that
we have not yet covered, so this section gets a little ahead, but it is fairly straightforward.  You simply
define a class using the *class* keyword and then give it a name.  An exception class should inherit from
the base exception class, *Exception*.  The easiest defined exception can simply use a pass statement inside
the class.  More involved exception classes can accept parameters and define an initializer.  It is also
a good practice to name your exception giving it a suffix of *Error*.

Example 5-6: Defining an Exception Class   ::

    class MyNewError(Exception):     
        pass                         
                                 
The example above is the simplest type of exception you can create.  This exception that was created above
can be raised just like any other exception now.   ::                                                   
                                 
    raise MyNewError, “Something happened in my program”                                                                                                                                                             
                                 
A more involved exception class may be written as follows.

Example 5-7: Exception Class Using Initializer    ::

    class MegaError(Exception):      
        “”” This is raised when there is a huge problem with my program”””                                                                                                                                           
        def __init__(self, val):     
            self.val = val           
        def __str__(self):           
            return repr(self.val)
            
Issuing Warnings
================
                                 
Warnings can be raised at any time in your program and can be used to display some type of warning message,
but they do not necessarily cause execution to abort.  A good example is when you wish to deprecate a method
or implementation but still make it usable for compatibility.  You could create a warning to alert the user
and let them know that such methods are deprecated and point them to the new definition, but the program would
not abort.  Warnings are easy to define, but they can be complex if you wish to define rules on them using
filters.  Much like exceptions, there are a number of defined warnings that can be used for categorizing.  In
order to allow these warnings to be easily converted into exceptions, they are all instances of the *Exception*
type.

Table 5-2. Python Warning Categories

=======================  ==========================================================================
Warning                  Description
=======================  ==========================================================================
Warning                  Root warning class                                                    
UserWarning              A user-defined warning                                                
DeprecationWarning       Warns about use of a deprecated feature             
SyntaxWarning            Syntax issues                                                         
RuntimeWarning           Runtime issues                                      
FutureWarning            Warns that a particular feature will be changing in a future release  
=======================  ==========================================================================

Table 5-1:  Exceptions

To issue a warning, you must first import the *warnings* module into your program.  Once this has been done
then it is as simple as making a call to the *warnings.warn()* function and passing it a string with the warning
message.  However, if you’d like to control the type of warning that is issued, you can also pass the warning
category. ::

	import warnings
	…
	warnings.warn(“this feature will be deprecated”)
	warnings.warn(“this is a more involved warning”, RuntimeWarning)


Importing the warnings module into your code gives you access to a number of built-in warning functions that can
be used.  If you’d like to filter a warning and change its behavior then you can do so by creating a filter.
The following is a list of functions that come with the *warnings* module.

===========================================================================  ===============================================================
Function and Description
===========================================================================  ===============================================================
warn(message[, category[, stacklevel]])                                                                                 
                                                                             Issues a warning.  Parameters include a message string,
                                                                             the optional category of warning, and the optional
                                                                             stacklevel that tells which stack frame the warning
                                                                             should originate from.                                                                                                                                                                                                                                                                          
                                                                                                                        
warn_explicit(message, category, filename, lineno[, module[, registry]])                                                
                                                                             This offers a more detailed warning message and makes category
                                                                             a mandatory parameter.  filename, lineno, and
                                                                             module tell where the warning is located.  registry represents
                                                                             all of the current warning filters that are active.                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                        
showwarning(message, category, filename, lineno[, file])                                                                
                                                                             Gives you the ability to write the warning to a file.                                                               
                                                                                                                        
formatwarning(message, category, filename, lineno)                                                                      
                                                                             Creates a formatted string representing the warning.                                                                
                                                                                                                        
resetwarnings()                                                                                                         
                                                                             Resets all of the warning filters.                                                                                  
                                                                                                                        
filterwarnings(action[, message[, category[, module[, lineno[, append]]]]])
===========================================================================  ===============================================================

This adds an entry into a warning filter list.  Warning filters allow you to modify the behavior of a warning.
The action in the warning filter can be one from the following table of actions, message is a regular expression,
category is the type of a warning to be issued, module can be a regular expression, lineno is a line number to
match against all lines, append specifies whether the filter should be appended to the list of all filters.

======================  ===========================================================
Filter Actions          Description
======================  ===========================================================
‘always’                Always print warning message                                
‘default’               Print warning once for each location where warning occurs   
‘error’                 Converts a warning into an exception  
‘ignore’                Ignores the warning                   
‘module’                Print warning once for each module in which warning occurs  
‘once’                  Print warning only one time           
======================  ===========================================================

Table 5-3. Warning Functions

Warning filters are used to modify the behavior of a particular warning.  There can be many different warning filters
in use, and each call to the *filterwarnings()* function will append another warning to the list of filters if so desired.
In order to see which filters are currently in use, issue the command *print warnings.filters*.  One can also specify
a warning filter from the command line by use of the –W option.  Lastly, all warnings can be reset to defaults by using
the *resetwarnings()* function.::

	-Waction:message:category:module:lineno
        
        
Assertions and Debugging
========================

Debugging can be an easy task in Python via use of the *assert* statement and the *__debug__* variable.  Assertions
are statements that can print to indicate that a particular piece of code is not behaving as expected.  The assertion
checks an expression for a True or False value, and if False then it issues an *AssertionError* along with an optional
message.  If the expression evaluates to True then the assertion is ignored completely. ::

	assert expression [, message]

By effectively using the *assert* statement throughout your program, you can easily catch any errors that may occur
and make debugging life much easier.  The following example will show you the use of the assert statement.::

	#  The following example shows how assertions are evaluated
	>>> x = 5
	>>> y = 10
	>>> assert x < y, "The assertion is ignored"
	>>> assert x > y, "The assertion works"
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	AssertionError: The assertion works


You can make use of the internal ­­*­­__debug__* variable by placing entire blocks of code that should be run for debugging
purposes only inside a conditional based upon value of the variable.

Example 5-10: Making Use of __debug__ ::

	if __debug__:
	    # perform some debugging tasks

Context Managers
================

Ensuring that code is written properly in order to manage resources such as files or database connections is an important
topic.  If files or database connections are opened and never closed then our program could incur issues.  Often times,
developers elect to make use of the issues.  Often times, developers elect to make use of the *try-finally* blocks to ensure
that such resources are handled properly.  While this is an acceptable method for resource management, it can sometimes
be misused and lead to problems when exceptions are raised in programs.  For instance, if we are working with a database
connection and an exception occurs after we’ve opened the connection, the program control may break out of the current block
and skip all further processing.  The connection may never be closed in such a case.  That is where the concept of context
management becomes an important new feature in Jython.  Context management via the use of the *with* statement is new to
Jython 2.5, and it is a very nice way to ensure that resources are managed as expected.  

In order to use the *with* statement, you must import from __future__.  The *with* statement basically allows you to take
an object and use it without worrying about resource management.  For instance, let’s say that we’d like to open a file
on the system and read some lines from it.  To perform a file operation you first need to open the file, perform any
processing or reading of file content, and then close the file to free the resource.  Context management using the *with*
statement allows you to simply open the file and work with it in a concise syntax.

Example 5-11: Python with Statement Example ::

	#  Read from a text file named players.txt
	>>> from __future__ import with_statement
	>>> with open('players.txt','r') as file:
	...     x = file.read() 
	... 
	>>> print x
	This is read from the file


In the example above, we did not worry about closing the file because the context took care of that for us.  This works
with object that extends the context management protocol.  In other words, any object that implements two methods named
*__enter__()* and *__exit__()* adhere to the context management protocol.  When the *with *statement begins, the *__enter__()*
method is executed.  Likewise, as the last action performed when the *with* statement is ending, the *__exit__()*
method is executed.  The __enter__() method takes no arguments, whereas the __exit__() method takes three optional arguments
*type, value, *and* traceback.  *The *__exit__()* method returns a *True* or *False* value to indicate whether an exception
was thrown.  The *as variable* clause on the *with* statement is optional as it will allow you to make use of the object from
within the code block.  If you are working with resources such as a lock then you may not the optional clause.

If you follow the context management protocol, it is possible to create your own objects that can be used with this technique.
The *__enter__()* method should create whatever object you are trying to work if needed.  If you are working with an immutable
object then you’ll need to create a copy of that object to work with in the *__enter__()* method.  The *__exit__()* method
on the other hand can simply return *False* unless there is some other type of cleanup processing that needs to take place.

Summary
=======



In this chapter, we discussed many different topics regarding exceptions and exception handling within a Python application.
First, you learned the exception handling syntax of the *try-except-finally* code block and how it is used.  We then discussed
why it may be important to *raise* your own exceptions at times and how to do so.  That topic led to the discussion of how
to define an exception and we learned that in order to do so we must define a class that extends the *Exception* type object.  

After learning about exceptions, we went into the warnings framework and discussed how to use it.  It may be important to use
warnings in such cases where code may be deprecated and you want to warn users, but you do not wish to *raise* any exceptions.
That topic was followed by assertions and how assertion statement can be used to help us debug our programs.  Lastly, we touched
upon the topic of context managers and using the *with* statement that is new in Jython 2.5.

In the next chapter you will delve into creating classes and learning about object-oriented programming in Python.  Hopefully
if there were topics discussed in this chapter or previously in the book that may have been unclear due to unfamiliarity with
object orientation, they will be clarified in Chapter 6.


