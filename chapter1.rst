Chapter 1: Language and Syntax
++++++++++++++++++++++++++++++




“Elegant”, that is an adjective that is often used to describe the Python language.  The term elegant is defined as “pleasingly graceful and stylish in appearance or manner”.  “Uncomplicated”, and “powerful” could also be great words to assist in the description of this language.  It is a fact that Python is an elegant language that lets one create powerful applications in an uncomplicated manner.  One may say that if you look at trends that are occurring within the computing industry today, Python can be looked at as the main objective.  There are dozens, if not hundreds, of programming languages available today which each offer a different flavor to the field.  Although there are many flavors, there is a similar objective for each of these programming languages...and that is to produce powerful and uncomplicated code that is easy to construct and maintain.  Python does just that.



While we’ve easily defined the goal of programming languages in a broad sense in paragraph one, we have left out one main advantage of learning the Python programming language.  The Python language can run everywhere because it has been extended to run on the Java platform.  We are talking about Jython, the language implementation that takes the elegance, power, and ease of Python and runs it on the JVM.  The Java platform is an asset to the Jython language much like the C libraries are for Python.  Jython is able to run just about everywhere, which gives lots of flexibility when deciding how to implement an application.  Not only does the Java platform allow for flexibility, but it also offers a vast library containing thousands of APIs which are available for use by Jython.  Add-in the maturity of the Java platform and it becomes easy to see why Jython is undoubtedly the main objective of every programming language.  The goal, if you will, of any programming language is to grant its developers the same experience which Jython does.  Simply put, learning Jython will be an asset to any developer.



As I’ve mentioned that the Jython language implementation basically takes Python and runs it on the JVM, you will find out that it does so much more.  Once you have experienced the power of programming on the Java platform it would be a difficult feat to move away from it.  Learning Jython not only allows one to stay running on the JVM, but it also allows you to learn a new way to harness the power of the platform.  The language increases productivity as it has an easily understood syntax which reads almost as if it were pseudo code.  It also adds dynamic abilities that are not available in the Java language itself.  In this chapter you will learn how to install and configure your environment, and you will also get an overview of those features which the Python language has to offer.  This chapter is not intended to delve so deep into the concepts of syntax as to bore you, but rather to give you a quick and informative introduction to the syntax so that you will know the basics and learn the language as you move on through the book.  It will also allow you the chance to compare some Java examples with those which are written in Python so you can see some of the advantages this language has to offer.



By the time you have completed this chapter, you should know the basic structure and organization that Python code should follow.  You’ll know how to use basic language concepts such as defining variables, using reserved words, and performing basic tasks.  It will give you a taste of using statements and expressions.  As every great program contains comments, you’ll learn how to document single lines of code as well as entire code blocks.  As you move through the book, you will use this chapter as a reference to the basics.  This chapter will not cover each feature in completion, but it will give you enough basic knowledge to start using the Python language.



The Difference Between Jython and Python
========================================

Jython is an implementation of the Python language for the Java platform.  Throughout this book, you will be learning how to use the Python language, and along the way we will show you where the Jython implementation differs from CPython, which is the canonical implementation of Python written in the C language.  It is important to note that the Python language syntax remains consistent throughout the different implementations.  At the time of this writing, there are three mainstream implementations of Python.  These implementations are: CPython, Jython for the Java platform, and IronPython for the .NET platform.



This book will reference the Python language in sections regarding the language syntax or functionality that is inherent to the language itself.  However, the book will reference the name Jython when discussing functionality and techniques that are specific to the Java platform implementation.  No doubt about it, this book will go in-depth to cover the key features of Jython and you’ll learn concepts that only adhere the Jython implementation.  Along the way, you will learn how to program in Python and advanced techniques.



Developers from all languages and backgrounds will benefit from this book.  Whether you are interested in learning Python from for the first time or discovering Jython techniques and advanced concepts, this book is a good fit for any developer.  Java developers and those who are new to the Python language will find specific interest in reading through Part I of this book as it will teach the Python language from the basics to more advanced concepts.  Seasoned Python developers will probably find more interest in Part II and Part III as they focus more on the Jython implementation specifics.  Often times in this reference, you will see Java code compared with Python code.  



Installing and Configuring Jython
=================================




Before we delve into the basics of the language, we’ll learn how to obtain Jython and configure it for your environment.  To get started, you will need to obtain a copy of Jython from the official website http://www.jython.org.  Since this book focuses on release 2.5, it would be best to visit the site now and download that release.  You will see that there are previous releases that are available to you, but they do not contain many of the features which have been included in the 2.5 release.



I think at this point it is important to mention that the Jython implementation maintains consistent features which match those in the Python language for each version.  For example, if you download the Jython 2.2.1 release, it will include all of the features that the Python 2.2 release contains.  Similarly, when using the 2.5 release you will have access to the same features which are included in Python 2.5.  There are also a couple of extra pieces included with the 2.5 release which are specific to Jython.  We’ll discuss more about these extra features throughout the book.



Okay, well if you haven’t done so already then please grab yourself a copy of the Jython 2.5 release.  You will see that the release is packaged as a cross-platform executable JAR file.  Right away, you can see the obvious advantage of running on the Java platform…one installer that works for various platforms.  It doesn’t get much easier than that!  In order to install the Jython language, you will need to have Java 5 or greater installed on your machine.  If you do not have Java 5 or greater then you’d better go and grab that from http://www.java.com and install it before trying to initiate the Jython installer.



You can initiate the Jython installer by simply double-clicking on the JAR file.  It will run you through a series of standard installation questions.  At one point you will need to determine which features you’d like to install.  If you are interested in looking through the source code for Jython, or possibly developing code for the project then you should choose the “All” option to install everything…including source.  However, for most Jython developers and especially for those who are just beginning to learn the language, I would recommend choosing the “Standard” installation option.  Once you’ve chosen your options and supplied an installation path then you will be off to the races.



In order to run Jython, you will need to invoke the jython.bat executable file on Windows or the jython.sh file on *NIX machines and Mac OS X.  That being said, you’ll have to traverse into the directory that you’ve installed Jython where you will find the file.  It would be best to place this directory within your PATH environment variable on either Windows, *NIX, or OS X machines so that you can fire up Jython from within any directory on your machine.  Once you’ve done this then you should be able to open up a terminal or command prompt and issue type “jython” then hit enter to invoke the interactive interpreter.  This is where our journey begins!  The Jython interactive interpreter is a great place to evaluate code and learn the language.  It is a real-time testing environment that allows you to type code and instantly see the result.  As you are reading through this chapter, I recommend you open up the Jython interpreter and follow along with the code examples.

Identifiers and Declaring Variables
===================================

::


Every programming language needs to contain the ability to capture or calculate values and store them.  Python is no exception, and doing so is quite easy.  Defining variables in Python is very similar to other languages such as Java, but there are a few differences that you need to note.  



First, variables in Python have no declared type.  Therefore, this allows any variable to hold any type of data.  It also allows the ability of having one variable contain of different data types throughout the life cycle of a program.  So a variable that is originally assigned with an integer, can later contain a String.



To define a variable in the Python language, you simply name it using an identifier.  An identifier is a name that is used to identify an object.  The language treats the variable name as a label that points to a value.  It does not give any type for the value.  Identifiers in Python can consist of any ordering of letters, numbers, or underscores.  However, an identifier must always begin with a non-numeric character value.  We can use identifiers to name any type of variable, block, or object in Python.  As with most other programming languages, once an identifier is defined, it can be referenced elsewhere in the program.



Once declared, a variable is untyped and can take any value.  This is one difference between using a statically typed language such as Java, and using dynamic languages like Python.  In Java, you need to declare the type of variable which you are creating, and you do not in Python.  It may not sound like very much at first, but this ability can lead to some extraordinary results.  Consider the following, lets define a value ‘x’ below and we’ll give it a value of zero.  

::

	int x = 0;




As you see, we did not have to give a type to this variable.  We simply name it and assign a value.  You can also see that in Python there is no need to end the declaration with a semicolon.  Since we do not need to declare a type for the variable, we can change it to a different value and type later in the program.



	x = ‘Hello Jython’


We’ve just changed the value of the variable ‘x’ from a numeric value to a String without any consequences.  This is a key to the dynamic language philosophy...change should not be difficult, but rather easy to integrate.



Let us take what we know so far and apply it to some simple calculations.  Based upon the definition of a variable in Python, we can assign an integer value to a variable, and change it to a float at a later point.  For instance:


	>>> x = 6
	>>> y = 3.14
	>>> x = x * y
	>>> print x
	18.84

In the previous example we’ve demonstrated that we can dynamically change the type of any given variable by simply performing a calculation upon it.  In other languages, we would have had to begin by assigning a float type to the ‘x’ variable so that we could later change it’s value to a float.  Not here, Python allows us to bypass type constriction and gives us an easy way to do it.

Reserved Words
==============

::


There are a few more rules to creating identifiers that we must follow in order to adhere to the Python language standard.  Certain words are not to be used as identifiers as the Python language reserves them for performing a specific role within our programs.  These words which cannot be used are known as reserved words.  If we try to use one of these reserved words as an identifier, we will see a SyntaxError thrown as Python wants these reserved words as it’s own.  

There are no symbols allowed in identifiers.  Yes, that means the Perl developers will have to get used to defining variables without the $.



The complete listing of reserved words is as follows:

========  =========  =======  =======  ==========
Words
========  =========  =======  =======  ==========
and       assert     break    class    continue  
def       del        elif     else     except    
exec      finally    for      from     global
if        or         pass     print    raise
return    try        while    with     yield              
========  =========  =======  =======  ==========

Table 1-1. Reserved  Words. The following lists all of the Python language reserved words


Coding Structure
----------------
 
Another key factor in which Python differs from other languages is it’s coding structure.  Back in the day, we had to develop programs based upon a very strict structure such that certain pieces must begin and end within certain punctuations.  Python uses positioning and code must adhere to an ordered structure.  Unlike languages such as Java that use brackets to open or close a code block, Python uses spacing as to make code easier to read and also limit unnecessary symbols in your code.  It strictly enforces ordered and organized code, but it lets the programmer define the rules.

Python ensures that each block of code adheres to its defined spacing strategy in a consistent manner.  What is the defined spacing strategy?  You decide.  As long as the first line of a code block is out-dented by at least one space, the rest of the block can maintain a consistent indentation, which makes code easy to read.  Many argue that it is the structuring technique that Python adheres to which makes them so easy to read.  No doubt, adhering to a standard spacing throughout an application makes for organization.  As a matter of fact, the Python standard spacing technique is to use four spaces for indentation.  If you adhere to these standards then your code will be easy to read and maintain in the future. 
 
For instance, let’s jump ahead and look at a simple ‘if’ statement.  Although you may not yet be familiar with this construct, I think you will agree that it is easy to determine the outcome.  Take a look at the following block of code written in Java first, and then we’ll compare it to the Python equivalent.

Java if-statement


        x = 100;
        
        if(x > 0){                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            System.out.println(“Wow, this is Java”);                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        } else {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            System.out.println(“Java likes curly braces”);                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        }


Now, let’s look at a similar block of code written in Python.

Python if-statement

        x = 100                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        if x > 0:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            print ‘Wow, this is elegant’                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
            print ‘Organization is the key’                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     




Okay, my example is cheesy but we will go through it nonetheless as it is demonstrating a couple of key points to the Python language.  As you see, the program evaluates if the value of the variable ‘x’ is greater than zero.  If so, it will print ‘Wow, this is elegant’.  Otherwise, it will print ‘Organization is the key’.  Look at the indentation which is used within the ‘if’ block.  This particular block of code uses four spaces to indent the ‘print’ statement from the initial line of the block.  Likewise, the ‘else’ jumps back to the first space of the line and its corresponding implementation is also indented by four spaces.  This technique must be adhered to throughout an entire Python application.  By doing so we gain a couple of major benefits:  Easy-to-read code, and no need to use curly braces.  Most other programming languages such as Java use a bracket “[“ or curly brace “{“ to open and close a block of code.  There is no need to do so when using Python as the spacing takes care of this for you.  Less code = easier to read and maintain.  

Operators
---------

The operators that are used by Python are very similar to those used in other languages...straightforward and easy to use.  As with any other language, you have your normal operators such as +, -, *, and / which are available for performing calculations.  As you can see from the examples below, there is no special trick to using any of these operators.

Example 1:  Performing Integer based operations

>>> x = 9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> y = 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> x + y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
11                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
>>> x - y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
>>> x * y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
18                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
>>> x / y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

Perhaps the most important thing to note with calculations is that if you are performing calculations based on integer values then you will receive a rounded result.  If you are performing calculations based upon floats then you will receive float results, etc.

Example 2:  Performing float based operations

>>> x = 9.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
>>> y = 2.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
>>> x + y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
11.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
>>> x - y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
7.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
>>> x * y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
18.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
>>> x / y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
4.5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

It is important to note this distinction because as you can see from the differences in the results of the division (/) operations in examples 1 and 2, we have rounding on the integer values and not on the float.  A good rule of thumb is that if your application requires precise calculations to be defined, then it is best to use float values for all of your numeric variables, or else you will run into a rounding issue.                                                                                  

Expressions
-----------

Expressions are just what they sound like...they are a piece of Python code that produces a value.  For example, if we wish to assign a particular value to a variable then we would use an expression.  Similarly, if I wish to perform a calculation based upon two variables or numeric values then I am performing a expression.

Examples of Expressions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

>>> x = 9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> y = 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> z = 9 * 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
>>> x + y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> x - y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> x * y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
>>> x / y                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

The examples of expressions that are shown above are very simplistic.  Expressions can be made to be very complex and perform powerful computations.  They can be combined together to produce complex results.                                                                                                                                                                                                                                                                                                         



Statements
----------

When we refer to statements, we are really referring to a line of code that does something.  There are several statements that can be issued in Python that ultimately define the different constructs available for use within an application.  In this section, we will take a tour of statement keywords and learn how they can be used.                                                                                                                                                                             

Let’s start out by listing each of these different statement keywords, and then we will go into more detail about how to use each of them with different examples.  I will not cover each statement keyword in this chapter as some of them are better left for later in the chapter or the book, but you should have a good idea of how to code an action which performs a task after reading through this section.  While this section will provide implementation details about the different statements, you should refer to later chapters to find advance uses of these features.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

Table 1-1. Statement Keywords


========  =====
Words
========  =====
if
else
for
while
continue
break
========  =====


If - Else Statement
-------------------


The if statement simply performs a comparison on two or more values and provides a logical outcome based upon that evaluation.  If statements are quite often used for branching code into one direction or another based upon certain values which have been calculated or provided in the code.  


For instance, the statement will compare the values and return a boolean result, namely True or False.  A corresponding action is then taken based upon the outcome of the boolean result.  Pseudocode would be as follows:


	if True:
	    perform an action
	else:
	    perform another action


Any number of *if/else* statements can be linked together in order to create a logical code branch, if you wish to use more than one else statement then all but the last else statements must be *elif* instead...and the last would be *else*.  Note that each expression must be indented with the conditional statement out-dented and the resulting operation indented.  Remember, a consistent indentation must be followed throughout the course of the program.  The if statement is a good example of how well the consistent use of indention helps readability of a program.  If you are coding in Java for example, you can space the code however you’d like as long as you use the curly braces to enclose the statement.  This can lead to code that is very hard to read…the indentation which Python requires really shines through here.



	>>> if x == y:
	...     print 'x is equal to y'
	... elif x > y:
	...     print 'x is greater than y'
	... else:
	...     print 'x is less than y'
	... 
	x is greater than y


While the code is simple, it demonstrates that using an *if* statement can result in branching code logic.

There are also some statements in Python which assist in logic flow.  These statements can be placed within an if statement or a loop (discussed in chapter 2) which will cause the logic of the statement to go in one direction or the other.  



pass Statement
--------------

Another useful statement for while working within loops is the *pass* statement.  Often times we have the need to use a placeholder value in an application in order to simply pass through an area without performing any tasks when an area of code requires an implementation.  The pass statement simply does nothing.  An example for it’s usage would be when you have a block of code which you’d like to bypass for debugging purposes.  It can also be used as a placeholder for a block of code which has not yet been implemented.

        while False:
	    pass


def Statement
-------------

This is one of those statements that will become second nature for usage throughout any Python programmer's life.  The *def* statement is used to define a function in an application.  While we will not get into functions in this chapter, I will show you an example of this statement's usage.  

::


	def myFunctionName(parameterList):
	    implementation
::


The pseudocode above demonstrates how one would use the *def* statement.  

print Statement
---------------

The *print* statement is used to display program output onto the screen.  It can be used for displaying messages which are printed from within a program and also for printing values which may have been calculated.  In order to display variable values within a print statement, we need to learn how to use some of the formatting options which are available to Python.  This section will cover the basics of using the print statement along with how to display values by formatting your strings of text.



In the Java language, we need to make a call to the System library in order to print something to the command line.  In Python, this can be done with the use of the print statement.  The most basic use of the *print* statement is to display a line of text.  In order to do so, you simply enclose the text which you want to display within single or double quotes.  Take a look at the following example written in Java, and compare it to the example immediately following which is rewritten in Python.  I think you’ll see why the print statement in Jython makes life a bit easier.

Java Print Output Example ::

	public void inspectValue(String val){
	    if (val == null){
	        System.out.println(“The value you have entered is not valid, please try again”;
	    } else {
	        System.out.println(	“The value you have entered is valid”);


Python Print Output Example ::

    def inspectValue(val):
    if val == None:
        print 'The value you have entered is not valid, please try again'
    else:
        print 'The value you have entered valid'


As you can see from the example above, printing a line of text in Python is very straight forward.  We can also print variable values to the screen using the print  statement. ::

    myValue = 'I love programming in Jython'
    print myValue
    
    >>> I love programming in Jython


Once again, very straight forward in terms of printing values of variables.  Simply place the variable within a print statement.  We can also use this technique in order to append the values of variables to a line of text.  In order to do so, just place the concatenation operator (+) in between the String of text which you would like to append to, and the variable you'd like to append. ::

    print 'I like programming in Java, but ' + myValue

    >>> I like programming in Java, but I love programming in Jython
    
This is great and all, but really not useful if you'd like to properly format your text or work with int values.  After all, the Jython parser is treating the (+) operator as a concatenation operator in this case...not as an addition operator.  If you try to append a numeric value to a String you will end up with an error. ::

    z = 10
    >>> print 'I am a fan of the number: ' + z
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: cannot concatenate 'str' and 'int' objects



As you can see from the example, Python does not like this trick very much.  So in order to perform this task correctly we will need to use some of the aforementioned Python formatting options.  This is easy and powerful to do, and it allows one to place any content or value into a print statement.  Before you see an example, let's take a look at some of the formatting operators and how to choose the one that you need.

%s - String 
%d - Decimal
%f   - Float

If you wish to include the contents of a variable or the result of an expression in your print  statement, you'll use the following syntax: ::

    print 'String of text goes here %d %s %f' % (decimalValue, stringValue, floatValue)

In the pseudocode above (if we can really have pseudocode for print statements), we wish to print the string of text which is contained within the single quotes, but also have the values of the variables contained where the formatting operators are located.  Each of the formatting operators, which are included in the string of text, will be replaced with the corresponding values from those variables at the end of the print statement.  The % symbol between the line of text and the list of variables tells Python that the it should expect the variables to follow, and that these value of these variables should be placed within the string of text in their corresponding positions. ::

    >>> stringValue = 'hello world'
    >>> floatValue = 3.998
    >>> decimalValue = 5
    >>> print 'Here is a test of the print statement using the values: %d, %s, and %f' % (decimalValue, stringValue, floatValue)
    
    Here is a test of the print statement using the values: 5, hello world, and 3.998000

As you can see this is quite easy to use and very flexible.  The next example shows that we also have the option of using expressions as opposed to variables within our statement. ::

    >>> x = 1
    >>> y = 2
    >>> print 'The value of x + y is: %d' % (x + y)
    The value of x + y is: 3


Another useful feature of the print statement is that it can be used for debugging purposes .  If we simply need to find out the value of a variable during processing then it is easy to display using the *print* statement.  Often times, using this technique can really assist in debugging and writing your code.


try-except-finally 
-------------------

The *try-except-finally* is the supported method for performing error handling within a Python application.  The idea is that we try to run a piece of code and if it fails then it is caught and the error is handled in a proper fashion.  We all know that if someone is using a program that displays an ugly long error message, it is not usually appreciated.  Using the *try-except-finally* statement to properly catch and handle our errors can mitigate an ugly program dump.



This approach is the same concept that is used within many languages, including Java.  There are a number of defined *error types* within the Python programming language and we can leverage these error types in order to facilitate the *try-except-finally* process.  When one of the defined error types is caught, then an implementation can be coded for handling the error, or can simply be logged, ignored, etc.  The main idea is to avoid those ugly error messages and handle them neatly.  If there is an exception that is caught within the block of code and we need a way to perform some cleanup tasks, we would place the cleanup code within the finally clause of the block.  All code within the finally clause is always invoked.



To begin, let's work with defining a generic *try-except-finally* example in which we simply place the *try* block around a piece of code and catch any errors that may be thrown.  We'll assume that we are not sure exactly which type of error will be thrown, so to generically define the *try-except-finally*, we will use an error type of *Exception*...the default Python error type.



::


	try:
	    implementation that may throw an error
	except Exception:
	    handle the error which was thrown
	finally:
	    perform some cleanup…called everytime
::


To augment this example, we'll go ahead and define a simple function which takes two parameters and returns the value of the first parameter divided by the second.  In order to demonstrate the *try-except-finally*, we'll throw one around the print statement in order to catch the programmer's mistake gracefully.

::


	>>> def myFunction(x,y):
	...     try:
	...         print 	x / y
	...     except Exception:
	...         print 'An error has been caught by the program'
	...     finally:
	...         print 'Perform some cleanup'

	>>> myFunction(0,0)
	An error has been caught by the program
	Perform some cleanup



We can see that by throwing the *try-except-finally* statement around the erroneous code, we've successfully caught the error and displayed a nice message.  This will make our application users happy.  However, this is not very practical because we don't really have any idea why the error was thrown or which error was thrown.  In order to provide more specific details of the error, it is possible to name the exception and then display it or log it in the implementation.

::


	>>> def myFunction(x,y):
	...     try:
	...         print x / y
	...     except Exception, err:
	...         print 'The following error has been caught: %s' %(err)

	>>> myFunction(4,2)
	2
	>>> myFunction(0,0)
	The following error has been caught: integer division or modulo by zero



Alright, this is looking much better now as we have named the exception "err" and then displayed it in our output.  Now the application user has a meaningful error message to tell us about when they reach this piece of code.  While this is much better than the generic error that we included in the first example, we still have not found the best way to handle the error.  The details of this topic can be read about more in Chapter 5:  Exception Handling in Jython.

assert Statement
----------------

Assert statements are used for debugging purposes and error handling within a Python program.   Basically, the assert statement checks to ensure that some value or expression is True.  If it is True, then execution will continue without anything happening, but if it is False then the program will indicate as such by throwing an *AssertionError*.  Errors and exceptions will be covered in more detail in later chapters.  For now, understand that by throwing an *AssertionError*, the code can be flagged as incorrect in an instance where we are trying to debug for a True value.

Example of Assertion: ::

    >>> x = 10
    >>> assert x == 11
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AssertionError

In the given example, the assertion checks to see if x is equal to eleven.  Obviously we can see that it is not, so it throws the expected AssertionError.


raise Statement
---------------


The raise statement is used to throw or “raise” an exception in Python.  You can place a raise statement anywhere that you wish to throw a specified error.  There are a number of defined exceptions within the language which can be thrown.  For instance, NameError is thrown when a specific piece of code is undefined or has no name.  For a complete list of exceptions in Python, please visit Chapter 5.

::


	>>> raise NameError
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	NameError
::


If you wish to specify your own message within a raise then you can do so by raising a generic Exception, and then specifying your message on the statement as follows.



	>>> raise Exception	(‘	Custom Exception	’)
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	Exception: Custom Exception
::


import Statement
----------------


The import statement is use much like it is in other languages, it brings external modules or code into a program so that it can be used.  This statement is ultimately responsible for reuse of code in multiple locations.  The import statement allows us to save code into a flat file or script, and then use it in an application at a later time.



There are a couple of different ways in which this statement can be used.  It can be used to simply import a named module into an application, or it can be used to import a module or piece of code.  If a class is stored in an external module that is named the same as the class itself, the import statement can be used to explicitly bring that class into an application.  Similarly, if you wish to import only a portion of code which is contained within an external module, then the specific code can be named within using the syntax from <<module>> import <<specific code>>.   Time to see some examples.

::


	#  Import a class named TipCalculator which is contained within 
	#  a module named TipCalculator.py

	import TipCalculator



	#  Import a function tipCalculator from within a module called ExternalModule.py

	from ExternalModule import tipCalculator

Other Python Statements
-----------------------


There are some other Python statements that can be used within applications as well, but they are probably better meant to be discussed within a later chapter as they provide more advanced functionality.  The following is a listing of other Python statements which you will read more about later on:



exec – Execute Python code in a dynamic fashion

global – References a global variable (Chapter 4)

with – New feature in 2.5 using __future__  (Chapter 7)

class – Create or define a new class object (Chapter 6)

yield – Used with generators, returns a value (Chapter 4)


Iteration
=========


The Python language has several iteration structures which are used to traverse through a series of items in a list, database records, or any other type of collection.  The most commonly used iteration structure within the language is probably the *for* loop, which is known for its easy syntax and practical usage.  However, the *while* loop still plays an important role in iteration, especially when you are not dealing with collections of data, but rather working with conditional expressions.



This section will take you though each of these two iteration structures and touch upon the basics of using them.  The *while* loop is relatively basic in usage, whereas there are many different implementations and choices when using the *for* loop.  I will only touch upon the *for* loop from a high-level perspective in this introductory chapter, but if you wish to go more in-depth then please visit Chapter 3.



While Loop
----------

The *while* loop construct is used in order to iterate through code based upon a provided conditional statement.  As long as the condition is true, then the loop will continue to process.  Once the condition evaluates to false, the looping ends.  The pseudocode for *while* loop logic reads as follows:

::


	 while 	True
	    perform operation
The loop begins with the declaration of the *while* and conditional expression, and it ends once the conditional has been met.  Keep in mind that we need to indent each of the lines of code that exist within the *while* loop.  This not only helps the code to maintain readability, but it also allows Python to do away with the curly braces!



::

	int x = 9;
	int y = 2;
	int z = x – y;
	while (y < x){
	    System.out.println(“y is “ + z + “ less than	 x”);
	    y = y++;
	}

Now, let’s see the same code written in Python. 



	>>> x = 9
	>>> y = 2
	>>> while y < x:
	...     print 'y is %d less than x' % (x-y)
	...     y = y + 1
	... 
	y is 7 less than x
	y is 6 less than x
	y is 5 less than x
	y is 4 less than x
	y is 3 less than x
	y is 2 less than x
	y is 1 less than x
::


In the example above, you can see that the conditional *y < x* is evaluated each time the loop passes.  Along the way, we increment the value of *y* by one each time we iterate, so that eventually *y* is no longer < than *x* and the loop ends.



For Loop
--------

We will lightly touch upon *for* loops in this chapter, but you can delve deeper into the topic in chapter two or three when lists, dictionaries, tuples, and ranges are discussed.  For now, you should know that a *for* loop is used to iterate through a defined set of values.  *For* loops are very useful for performing iteration through values because this is a concept which is used in just about any application.  For instance, if you retrieve a list of database values, you can use a *for* loop to iterate through them and print each one out.  



The pseudocode to *for* loop logic is as follows:

::


	 for each value in this defined set:
	     perform operation
As you can see with the pseudocode, I’ve indented in a similar fashion to the way in which the other expression constructs are indented.  This uniform indentation practice is consistent throughout the Python programming language.  We’ll compare the for loop in Java to the Python syntax below so that you can see how the latter makes code more concise.



::

	for (x = 0; x <= 10; x++){
	    System.out.println(x);
	}
::


Now, the same code implemented in Python:

	>>> for x in range(10):
	...     print x
	... 
	0
	1
	2
	3
	4
	5
	6
	7
	8
	9
::


In the above example, we use a construct which has not yet been discussed.  A range is  a built-in function for Python which simply provides a range from one particular value to another.  In the example, we pass the value 10 into the range which gives us all values between 0 and 10.  We see this in the resulting print out after the expression.



It is time to go back and cover a couple of Python statement keywords which we passed over previously.  Now that we’ve seen how to implement a loop within the language, it is a good time to cover some statements that can be used along with a loop.

continue Statement
------------------

The *continue* statement is to be used when you are within a looping construct, and you have the requirement to tell Python to *continue* processing past the rest of the statements in the current loop.  Once the Python interpreter sees a *continue* statement, it ends the current iteration of the loop and goes on to continue processing the next iteration.  The continue statement can be used with any looping construct.



::


	>>> x = 10
	>>> while x >= 0:
	...     if x == 0:
	...         continue
	...     else:
	...         print "x is currently equal to ", x
	...         x = x - 1
	... 
	x is currently equal to  10
	x is currently equal to  9
	x is currently equal to  8
	x is currently equal to  7
	x is currently equal to  6
	x is currently equal to  5
	x is currently equal to  4
	x is currently equal to  3
	x is currently equal to  2
	x is currently equal to  1
::


In the example above, the x variable decreased by one each time the loop iterates.  On the final pass, as the x is equal to 0 we do not display a message.  Why is this example useful?  It’s not really…only to give you an understanding of the context in which the continue statement would be used.

break Statement
---------------

Much like the *continue* statement, the *break* statement can be used inside of a loop.  We use the *break* statement in order to break out of a current loop so that a program can move onto its next task.  If we are working with a break statement that resides within a loop that is contained in another loop (nested loop construct), then that inner loop will be terminated.  Let’s check it out:



::


	x = 10
        while x >= 0:
	     if x == 0:
	         print "x is now equal to zero!"
	         break
	     else:
	         if x % 2 == 0: 
	            print x
	     x = x – 1

	Results:

	10
	8
	6
	4
	2
	x is now equal to zero!
        

Documenting Code
================

Code documentation, an annoyingly important part of every application developer’s life.  Although many of us despise code documentation, it must exist for any application that is going to be used for production purposes.  Not only is proper code documentation a must for manageability and long-term understanding of Python code fragments, but it also plays an important role in debugging some code as we will see in some examples below.



Sometimes we wish to document an entire function or class, and other times we wish to document only a line or two.  Whatever the case, Python provides a way to do it in a rather unobtrusive manner.  Much like many of the other programming languages that exist today, we can begin a comment on any part of any code line.  We can also comment spanning multiple lines if we wish.  Just on a personal note, I rather like the Python documentation symbol (#) or hash, as it provides for clear-cut readability.  There are not many places in code that you will use the (#) symbol unless you are trying to perform some documentation.  Many other languages use symbols such as (/) which can make code harder to read as those symbols are evident in many other non-documenting pieces of code.  Okay, it is time to get off my soap box on Python and get down to business.

In order to document a line of code, you simply start the document or comment with a (#) symbol.  This symbol can be placed anywhere on the line and whatever follows it is ignored by the Python compiler and treated as a comment or documentation.  Whatever precedes the symbol will be parsed as expected.  

::


	>>> # This is a line of documentation
	>>> x = 0  # This is also documentation        
	>>> y = 20
	>>> print x + y
	20

As you can see, the Python parser ignores everything after the #, so we can easily document or comment as needed.



One can easily document multiple lines of code using the # symbol as well by placing the hash at the start of each line.
It nicely marks a particular block as documentation.  However, Python also provides a multi-line comment using the triple-quote (‘’’)
designation at the beginning and end of a comment.  This type of multi-line comment is also referred to as a doc string and it is only
to be used at the start of a module, class, or function.  Let’s take a look at these two instances of multi-line documentation in the examples that follow. ::

        
        # This function is used in order to provide the square
	# of any value which is passed in.  The result will be 
	# passed back to the calling code.
	def square_val(value):
	    return value * value
	... 
	>>> print square_val(3)
	9


	def tip_calc(value, pct):
	    ''' This function is used as a tip calculator based on a percentage
	       which is passed in as well as the value of the total amount.  In
	       this function, the first parameter is to be the total amount of a  
	       bill for which we will calculate the tip based upon the second 
	       parameter as a percentage '''
	    return value * (pct * .01)
	...
	>>> print tip_calc(75,15)
	11.25


Okay, as we can see, both of the documentation methods above can be used to get the task of documenting or comment code done.
In the first example, we used multiple lines of documentation beginning with the # symbol in order to document the *square_val* function.
In the second example, we use the triple-quote method in order to span multiple lines of documentation.  Both of them appear to work as
defined...however, the second option provides a greater purpose as it allows one to document specific named code blocks and retrieve that
documentation by calling the __doc__ function on that block.  For instance, if we wish to find out what the *square_val* code does, we need
to visit the code and either read the multi-line comment or simply parse the code.  However, if we wish to find out what the tip_calc function
does, we can call the tip_calc.__doc__ function and the multi-line comment will be returned to us.  This provides a great tool to use for
finding out what code does without actually visiting the code itself. ::


	>>> print tip_calc.__doc__
	 This function is used as a tip calculator based on a percentage
	       which is passed in as well as the value of the total amount.  In
	       this function, the first parameter is to be the total amount of a  
	       bill for which we will calculate the tip based upon the second 
	       parameter as a percentage 

These examples and short explanations should give you a pretty good feel for the power of documentation that is provided by the Python language.
As you can see, using the multi-line triple-quote method is very suitable for documenting classes or functions.  Commenting with the # symbol
provides a great way to organize comments within source and also for documenting those lines of code which may be “not so easy” to understand.



Python Help
===========

Getting help when using the Jython interpreter is quite easy.  Built into the interactive interpreter is an excellent help()
option which provides information on any module, keyword, or topic available to the Python language.  While making use of the
help() system, you can either use the interactive help which is invoked within the interpreter by simply typing help(), or you
can obtain help on a specific object by typing help(object).

Summary
=======

This chapter has covered lots of basic Python programming material.  It should have provided a basic foundation for the fundamentals
of programming in Python.  This chapter shall be used to reflect upon while delving deeper into the language throughout the remainder of this book.



We began by discussing the declaration of variables and explained the dynamic tendencies of the language.  This gives us an understanding
that variables do not have any type declared with them, rather, they are untyped and can be modified into any Python data type.
We then went on to present the reserved words of the language and then discussed the coding structure which must be adhered to when
developing a Python application.  After that, we discussed operators, expressions, and statements.  We learned that expressions are
generally blocks of code that produce a value, and that statements consist of conditional and declarative reserved words that allow
us to perform different tasks within our applications.  Each of the Python statements were discussed and examples were given.  Iteration
constructs were then discussed so that we could begin to use our statements and program looping tasks.



Following the language overview, documentation was discussed.  It is an important part of any application, and Python makes it easy to do.
Not only did we learn how to document lines of code, but also documenting entire blocks of code. 
Throughout the rest of the book, you will learn more in-depth and advanced uses of the topics that we’ve discussed in this chapter.
You will also learn concepts and techniques that you’ll be able to utilize in your own programs to make them more powerful and easy to maintain.







