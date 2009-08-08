Chapter 2: Data Types and Referencing
+++++++++++++++++++++++++++++++++++++

We all know that programming languages and applications need data.  We define applications to work with data,
and we need to have containers that can be used to hold it.  This chapter is all about defining containers and
using them to work with application data.  This is the foundation of any programming language...it is how we get
tasks accomplished.  Whether the data we are using is coming from a keyboard entry or if we are working with a
database, there needs to be a way to temporarily store it in our programs so that it can be manipulated and used.
Once we're done working with the data then these temporary containers can be destroyed in order to make room for new constructs.

We'll start by taking a look at the different data types that are offered by the Python language, and then we'll
follow by discussing how to use that data once it has been collected and stored.  We will compare and contrast the
different types of structures that we have in our arsenal, and I'll give some examples of which structures to use
for working with different types of data.  There are a multitude of tasks that can be accomplished through the use
of lists, dictionaries, and tuples and I will cover the majority of them.  Once you learn how to define and use these
structures, then we'll talk a bit about what happens to them once they are no longer needed by our application.

Lets begin our journey into exploring data types and structures within the Python programming language...these are skills
that you will use in each and every practical Jython program.


Python Data Types
=================

As we’ve discussed, there is a need to store and manipulate data within programs.  In order to do so then we must also
have the ability to create containers used to hold that data so that the program can use it.  The language needs to know
how to handle data once it is stored, and we can do that by assigning data type to our containers.  However, in Python
it is not a requirement to do so because the interpreter is able to determine which type of data we are storing in a dynamic fashion.  

The following table lists each data type and gives a brief description of the characteristics that define each of them.



===========  =========================================================================================  
Data Type    Characteristics                                                                          
===========  =========================================================================================
None         NULL value object                                                                   
Numeric      A data type used to hold numeric values of integer, decimal, float, complex, and long    
Boolean      True or False value (also characterized as numeric values of 1 and 0 respectively)  
Sequence     Includes the following types:  string, unicode string, basestring, xrange, list, tuple   
Mapping      Includes the dictionary type                                                             
Set          Unordered collection of distinct objects; includes the following types:  set, frozenset  
File         Used to make use of file system objects                                                  
Iterator     Allows for iteration over a container                                               
           
===========  =========================================================================================

Table 2-1.  Python Data Types



Given all of that information and the example above, we need to know a way to declare a variable in the Python language.
You’ve seen some examples in the previous chapter, but here I will formally show how it is done.  Let’s take a look at some
examples of defining variables in the following lines of code. ::


	# Defining a String
	x = ‘Hello World’
	x = “Hello World Two”

	#  Defining a number
	y = 10

	#  Float
	z = 8.75

	# Complex
	i = 8.07j

An important point to note is that there really are no types in Jython.  Every object is an instance of a class.  Therefore,
in order to find the type of an object in Jython it is perfectly valid to write obj.__class__. ::



	# Return the type of an object in Jython using __class__
	>>> a = 'Hello'
	>>> a.__class__
	<type 'str'>
        
        
Strings and String Methods
--------------------------

Strings are a special type within most programming languages because they are often used to manipulate data.  A string
in Python is a sequence of characters, which is immutable.  This is very important to know as it has a large impact on
the overall understanding of strings.  Once a string has been defined it cannot be changed.  However, there are a large
amount of string methods that can be used to manipulate the contents of a particular string.  Although we can manipulate
the contents, Python really gives us a manipulated copy of the string…the original string is left unchanged.

Prior to the 2.5.0 release of Jython, CPython and Jython treated strings a bit differently.  There are two types of string objects in CPython, these are known as
*Standard* strings and *Unicode* strings.  Standard strings contain 8-bit data, whereas Unicode strings are sequences of data
composed of 16-bit characters.  There is a lot of documentation available that specifically focuses on the differences between
the two types of strings, this reference will only cover the basics.  It is worth noting that Python contains an abstract string
type known as *basestring* so that it is possible to check any type of string to ensure that it is a string instance.  

Prior to the 2.5.0 release of Jython, there was only one string type.  The string type in Jython supported full two-byte Unicode characters and all functions
contained in the string module are Unicode-aware.  If the u’’ string modifier was specified, it was ignored by Jython.  Since the release of 2.5.0, strings in Jython are treated
just like those in CPython, so the same rules will apply to both implementations.  It is also
worth noting that Jython uses character properties from the Java platform.  Therefore properties such as isupper and islower, which
we will discuss later in the section, are based upon the Java properties.

In remainder of this section we will go through each of the many string functions that are at our disposal.  These functions will
work on both Standard and Unicode strings.  As with many of the other features in Python and other programming languages, there are
often times more than one way to accomplish a task.  In the case of strings and string manipulation, this definitely holds true.
However, you will find that in most cases, although there are more than one way to do things, Python experts have added functions
which allow us to achieve better performing and easier to read code.  Sometimes one way to perform a task is better achieved by
utilizing a certain function in one case, and doing something different in another case.

The following table lists all of the string methods that have been built into the Python language as of the 2.5 release.  Since Python
is an evolving language, this list is sure to change in future releases.  Most often, additions to the language will be made, or
existing features are enhanced.  Following the table, I will give numerous examples of the methods and how they are used.  Although
I cannot provide an example of how each of these methods work (that would be a book in itself), they all function in the same manner
so it should be rather easy to pick up.



==================================  =========================================================================================================================================  ===
Method                              Description of Functionality                                                                                                             
==================================  =========================================================================================================================================  ===
capitalize()                        Capitalize string                                                                                                                        
center(width[,fill])                Reposition string and provide optional padding filler character                                                                          
count(sub[,start[,end]])            Count the number of times the substring occurs within the string                                                                         
decode([encoding[,errors]])         Decodes and returns Unicode string                                                                                                            
encode([encoding[,errors]])         Produces an encoded version of a string                                                                                                       
endswith(suffix[,start[,end]])      Returns a boolean to state whether the string ends in a given pattern                                                                         
expandtabs([tabsize])               Converts tabs within a string into spaces                                                                                                
find(sub[,start[,end]])             Returns the index of the position where the first occurrence of the given substring begins                                               
index(sub[,start[,end])             Returns the index of the position where the first occurrence of the given substring begins                                               
isalnum()                           Returns a boolean to state whether the string contain both alphabetic and numeric characters                                             
isalpha()                           Returns a boolean to state whether the string contains all alphabetic characters                                                         
isdigit()                           Returns a boolean to state whether the string contains all numeric characters                                                            
islower()                           Returns a boolean to state whether a string contains all lowercase characters                                                            
isspace()                           Returns a boolean to state whether the string consists of all whitespace                                                                 
istitle()                           Returns a boolean to state whether the first character of each word in the string is capitalized                                         
isupper()                           Returns a boolean to state whether all characters within the string are uppercase                                                        
join(sequence)                      Joins two strings by combining                                                                                                           
ljust(width[,fillchar])             Align the string to the left by width                                                                                                    
lower()                             Converts all characters in the string to lowercase                                                                                       
lstrip([chars])                     Removes the first found characters in the string from the left that match the given characters.  Also removes whitespace from the left.  
partition(separator)                Partitions a string starting from the left using the provided separator                                                                  
replace(old,new[,count])            Replaces the portion of string given in *old* with the portion given in *new*                                                            
rfind(sub[,start[,end]])            Searches and finds the first occurrence from the end of the given string                                                                           
rindex(sub[,start[,end]])           Searches and finds the first occurrence of the given string or returns an error                                                          
rjust(width[,fillchar])             Align the string to the right by width                                                                                                   
rpartition(separator)               Partitions a string starting from the right using the provided separator object                                                          
rsplit([separator[,maxsplit]])      Splits the string from the right side and uses the given separator as a delimiter                                                        
rstrip([chars])                     Removes the first found characters in the string from the right that match those given.  Also removes whitespace from the right.         
split([separator[,maxsplit]])       Splits the string and uses the given separator as a delimiter.                                                                           
splitlines([keepends])              Splits the string into a list of lines.  Keepends denotes if newline delimiters are removed.                                             
startswith(prefix[,start[,end]])    Returns a boolean to state whether the string starts with the given prefix                                                               
strip([chars])                      Removes the given characters from the string.                                                                                            
swapcase()                          Converts the case of each character in the string.                                                                                       
title()                             Returns the string with the first character in each word uppercase.                                                                      
translate(table[,deletechars])      Use the given character translation table to translate the string.                                                                       
upper()                             Converts all of the characters in the string to lowercase.                                                                               
zfill(width)                        Pads the string from the left with zeros for the specified width.                                                                        
==================================  =========================================================================================================================================  ===

Table 2-2.  String Methods

Now let’s take a look at some examples so that you get an idea of how to use the string methods.  As stated previously, most of them work in a similar manner. ::



	ourString=’python is the best language ever’


	# Capitalize a String
	>>> ourString.capitalize()                      
	'Python is the best language ever'

	# Center string
	>>> ourString.center(50)
	'         python is the best language ever         '
	>>> ourString.center(50,'-')
	'---------python is the best language ever---------'

	# Count substring within a string
	>>> ourString.count('a')
	2

	# Partition a string
	>>> x = "Hello, my name is Josh"
	>>> x.partition('n')
	('Hello, my ', 'n', 'ame is Josh')


String Formatting
~~~~~~~~~~~~~~~~~

You have many options when printing strings using the *print* statement.  Much like the C programming language, Python string
formatting allows you to make use of a number of different conversion types when printing. ::


	Using String Formatting
	# The two syntaxes below work the same
	>>> x = "Josh"
	>>> print "My name is %s" % (x)
	My name is Josh
	>>> print "My name is %s" % x  
	My name is Josh
        

======  ============================================================================
Type    Description                                                                 
======  ============================================================================
d            signed integer decimal                                                      
i            signed integer decimal                                                      
o            unsigned octal                                                              
u            unsigned decimal                                                            
x            unsigned hexidecimal                                                        
X            unsigned hexidecimal (upper)                                                
E            floating point exponential format (upper)                                   
e            floating point exponential format                                           
f            floating point decimal format                                               
F            floating point decimal format (upper)                                       
g            floating point exponential format if exponent > -4, otherwise float         
G            floating point exponential format (uppr) if exponent > -4, otherwise float  
c            single character                                                            
r            string (converts any python object using repr())                            
s            string (converts any python object using str())                             
%            no conversion, results in a percent (%) character                           
======  ============================================================================

Table 2-3.  Conversion Types

 ::


	>>> x = 10 
	>>> y = 5.75 
	>>> print 'The expression %d * %f results in %f' % (x, y, x*y)
	The expression 10 * 5.750000 results in 57.500000
        
Ranges
------

Ranges are not really a data type or a container; they are really a Jython built-in function (Chapter 4).  For this reason,
we will only briefly touch upon the range function here, and they’ll be covered in more detail in Chapter 4.  However,
because they play such an important role in the iteration of data, usually via the *for* loop, I think it is important to
discuss them in this section of the book.  The range is a special function that allows one to iterate between a range of
numbers; and/or list a specific range of numbers.  It is especially helpful for performing mathematical iterations, but
it can also be used for simple iterations.

The format for using the range function includes an optional starting number, an ending number, and an optional stepping number.
If specified, the starting number tells the range where to begin, whereas the ending number specifies where the range should end.
The optional step number tells the range how many numbers should be placed between each number contained within the range output.


Range Format
~~~~~~~~~~~~

	range([start], stop, [step])

::

	>>>range(0,10)

	>>>range(10)

	>>>range(0,10,2)
	>>> range(100,0,-10)
	[100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

As stated previously, this function can be quite useful when used within a *for* loop as the Jython *for* loop syntax works
very well with it.  The following example displays a couple examples of using the range function within a *for* loop context. ::

	>>> for i in range(10):
	...         print i
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

	# Multiplication Example
	>>> x = 1
	>>> for i in range(2, 10, 2):
	...         x = x + (i * x)
	...         print x
	... 
	3
	15
	105
	945


As you can see, a range can be used to iterate through just about any number set...be it positive or negative in range.  

Lists, Dictionaries, Sets, and Tuples
-------------------------------------

Data collection containers are a useful tool for holding and passing data throughout the lifetime of an application.  The data
can come from any number of places, be it the keyboard, a file on the system, or a database…it can be stored in a collection
container and used at a later time.  Lists, dictionaries, sets, and tuples all offer similar functionality and usability, but
they each have their own niche in the language.  We’ll go through several examples of each since they all play an important role
under certain circumstances.

Since these containers are so important, we’ll go through an exercise at the end of this chapter, which will give you a chance
to try them out for yourself.  

Lists
~~~~~

Perhaps one of the most used constructs within the Python programming language is the list.  Most other programming languages
provide similar containers for storing and manipulating data within an application.  The Python list provides an advantage to
those similar constructs which are available in statically typed languages.  The dynamic tendencies of the Python language help
the list construct to harness the great feature of having the ability to contain values of different types.  This means that a
list can be used to store any Python data type, and these types can be mixed within a single list.  In other languages, this type
of construct is defined as a typed object, which locks the construct to using only one data type.

The creation and usage of Jython lists is just the same as the rest of the language…very simple and easy to use.  Simply assigning
a set of empty square brackets to a variable creates an empty list.  We can also use the built-in list() type to create a list.
The list can be constructed and modified as the application runs, they are not declared with a static length.  They are easy to
traverse through the usage of loops, and indexes can also be used for positional placement or removal of particular items in the list.
We’ll start out by showing some examples of defining lists, and then go through each of the different avenues which the Jython
language provides us for working with lists. ::

	# Define an empty list
	myList = []
	myList = list()

	# Define a list of string values
	myStringList = [‘Hello’,’Jython’,’Lists’]

	# Define a list containing mulitple data types
	multiList = [1,2,’three’,4,’five’,’six’]

	# Define a list containing a list
	comboList = [1,myStringList,multiList]

As stated previously, in order to obtain the values from a list we can make use of indexes.  Much like the Array in the Java language,
using the *list[index]* notation will allow us to access an item.  If we wish to obtain a range or set of values from a list, we can
provide a *starting* index, and/or an *ending* index.  This technique is also known as *slicing*.  What’s more, we can also return
a set of values from the list along with a stepping pattern by providing a *step* index as well.  One key to remember is that while
accessing a list via indexing, the first element in the list is contained within the 0 index. ::

	# Obtain elements in the list
	>>> myStringList[0]
	‘Hello’

	>>> myStringList[2]
	‘Lists’

	>>> myStringList[-1]
	'Lists'

	# Using the slice method
	>>> myStringList[0:2]
	['Hello', 'Jython']

	# Return every other element in a list
	>>> newList=[2,4,6,8,10,12,14,16,18,20]
	>>> newList[0:10:2]
	[2, 6, 10, 14, 18]

	# Leaving a positional index blank will also work
	>>> newList[::2]
	[2, 6, 10, 14, 18]

Modifying a list is much the same, you can either use the index in order to insert or remove items from a particular position.
There are also many other ways that you can insert or remove elements from the list.  Jython provides each of these different
options as they provide different functionality for your operations. 

In order to add an item to a list, you can make use of the *append()* method in order to add an item to the end of a list.
The *extend()* method allows you to add an entire list or sequence to the end of a list.  Lastly, the *insert()* method
allows you to place an item or list into a particular area of an existing list by utilizing positional indexes.
You will examples of each method below.

Similarly, we have plenty of options for removing items from a list.  The *del* statement, as explained in Chapter 1,
can be used to remove or delete an entire list or values from a list using the index notation.  You can also use the
*pop() *or *remove()* method to remove single values from a list.  The *pop()* method will remove a single value from
the end of the list, and it will also return that value at the same time.  If an index is provided to the *pop()* function,
then it will remove and return the value at that index.  The *remove()* method can be used to find and remove a particular
value in the list.  If more than one value in the list matches the value passed into the *remove()* function, the first one
will be removed.  Another note about the *remove()* function is that the value removed is not returned.  Let’s take a look
at these examples of modifying a list. ::

	# Adding values to a list
	>>> newList=['a','b','c','d','e','f','g']
	>>> newList.append('h')
	>>> print newList
	['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	# Add another list to the existing list
	>>> newList2=['h','i','j','k','l','m','n','o','p']
	>>> newList.extend(newList2)
	>>> print newList
	['a', 'b', 'c', 'd', 'e', 'f', 'g', ‘h’,'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

	# Insert a value into a particular location via the index
	>>> newList.insert(2,'c') 
	>>> print newList
	['a', 'b', 'c', 'c', 'd', 'e', 'f', 'g', 'h', ‘h’,'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

	# Use the slice notation to insert another list or sequence
	>>> newListA=[100,200,300,400]
	>>> newListB=[500,600,700,800]
	>>> newListA[0:2]=newListB
	>>> print newListA
	[500, 600, 700, 800, 300, 400]

	# Use the del statement to delete a list
	>>> newList3=[1,2,3,4,5]
	>>> print newList3
	[1, 2, 3, 4, 5]
	>>> del newList3
	>>> print newList3
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	NameError: name 'newList3' is not defined

	# Use the del statement to remove a value or range of values from a list
	>>> newList3=['a','b','c','d','e','f']
	>>> del newList3[2]
	>>> newList3
	['a', 'b', 'd', 'e', 'f']
	>>> del newList3[1:3]
	>>> newList3
	['a', 'e', 'f']

	# Remove values from a list using pop and remove functions
	>>> print newList
	['a', 'b', 'c', 'c', 'd', 'e', 'f', 'g', 'h',’h’, 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
	>>> newList.pop(2)
	'c'
	>>> print newList
	['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',’h’, 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
	>>> newList.remove('h')
	>>> print newList
	['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

	# Useful example of using pop() function
	>>> x = 5
	>>> timesList = [1,2,3,4,5]
	>>> while timesList:
	...     print x * timesList.pop(0)
	...             
	5
	10
	15
	20
	25

Now that we know how to add and remove items from a list, it is time to learn how to manipulate the data within them.
Python provides a number of different methods that can be used to help us manage our lists.  See the table below for a
list of these functions and what they can do.



=========  ===============================================================================
Method     Tasks Performed                                                                
=========  ===============================================================================
index      Returns the index of the first value in the list which matches a given value.  
count      Returns the number of items in the list which match a given value.             
sort       Sorts the items contained within the list.                                     
reverse    Reverses the order of the items contained within the list                      
=========  ===============================================================================

Table 2-4.  Python List Methods

Let’s take a look at some examples of how these functions can be used on lists. ::

	# Returning the index for any given value
	>>> newList=[1,2,3,4,5,6,7,8,9,10]
	>>> newList.index(4)
	3

	# Add a duplicate into the list and then return the index
	>>> newList.append(6)
	>>> newList
	[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 6]
	>>> newList.index(6)
	5

	# Using count() function to return the number of items which match a given value
	>>> newList.count(2)
	1
	>>> newList.count(6)
	2

	# Sort the values in the list
	>>> newList.sort()
	>>> newList      
	[1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]

	# Reverse the order of the value in the list
	>>> newList.reverse()
	>>> newList
	[10, 9, 8, 7, 6, 6, 5, 4, 3, 2, 1]
        
Lists
~~~~~

Moving around within a list is quite simple.  Once a list is populated, often times we wish to traverse through it
and perform some action against each element contained within it.  You can use any of the Python looping constructs
to traverse through each element within a list.  While there are plenty of options available, the *for* loop works
especially well.  The reason is because of the simple syntax that the Python *for* loop uses.  This section will show
you how to traverse a list using each of the different Python looping constructs.  You will see that each of them has
advantages and disadvantages.  

Let’s first take a look at the syntax that is used to traverse a list using a *for* loop.  This is by far one of the
easiest modes of going through each of the values contained within a list.  The *for* loop traverses the list one
element at a time, allowing the developer to perform some action on each element if so desired. ::

	>>> ourList=[1,2,3,4,5,6,7,8,9,10]
	>>> for elem in ourList:
	...    print elem
	... 
	1
	2
	3
	4
	5
	6
	7
	8
	9
	10


As you can see from this simple example, it is quite easy to go through a list and work with each item individually.  The
*for* loop syntax requires a variable to which each element in the list will be assigned for each pass of the loop.
Additionally, we can still make use of the current index while traversing a loop this way if needed.  The only requirement
is to make use of the *index()* method on the list and pass the current element. ::

	>>>ourList=[1,2,3,4,5,6,7,8,9,10]
	>>> for elem in ourList:          
	...     print 'The current index is: %d' % (ourList.index(elem))
	... 
	The current index is: 0
	The current index is: 1
	The current index is: 2
	The current index is: 3
	The current index is: 4
	The current index is: 5
	The current index is: 6
	The current index is: 7
	The current index is: 8
	The current index is: 9

If we do not wish to go through each element within the list then that is also possible via the use of the *for* loop.
In this case, we’ll simply use a list slice to retrieve the exact elements we want to see.  For instance, take a look
a the following code which traverses through the first 5 elements in our list. :: 


	>>> for elem in ourList[0:5]:
	...     print elem
	... 
	1
	2
	3
	4
	5

To illustrate a more detailed example, lets say that you wished to retrieve every other element within the list. ::

	>>> for elem in ourList[0::2]:
	...     print elem
	... 
	1
	3
	5
	7
	9

As you can see, doing so is quite easy by simply making use of the built-in features that Python offers.


List Comprehensions
~~~~~~~~~~~~~~~~~~~

There are some advanced features for lists that can help to make a developer’s life easier.  Once such feature is known
as a *list comprehension*.  While this concept may be daunting at first, it offers a good alternative to creating many separate
lists manually or using map().  List comprehensions take a given list, and then iterate through it and apply a given expression
against each of the objects in the list.  This allows one to quickly take a list and alter it via the use of the provided expression.
Of course, as with many other Python methods the list comprehension returns an altered copy of the list.  The original list is left untouched.


Let’s take a look at the syntax for a list comprehension.  They are basically comprised of an expression of some kind followed by a
*for* statement and then optionally more *for* or *if* statements.  As they are a difficult technique to describe, let’s take a look
at some examples.  Once you’ve seen list comprehensions in action you are sure to understand them and see how useful they can be. ::

	# Create a list of ages and add one to each of those ages using a list comprehension
	>>> ages=[20,25,28,30]
	>>> [age+1 for age in ages]  
	[21, 26, 29, 31]

	# Create a list of names and convert the first letter of each name to uppercase as it should be
	>>> names=['jim','frank','vic','leo','josh']
	>>> [name.title() for name in names]
	['Jim', 'Frank', 'Vic', 'Leo', 'Josh']

	# Create a list of numbers and return the square of each EVEN number
	>>> numList=[1,2,3,4,5,6,7,8,9,10,11,12]
	>>> [num*num for num in numList if num % 2 == 0]
	[4, 16, 36, 64, 100, 144]

	# Use a list comprehension with a range
	>>> [x*5 for x in range(1,20)]
	[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]


List comprehensions can make code much more concise and allows one to apply expressions or functions to list elements quite easily.
Let’s take a quick look at an example written in Java for performing the same type of work as an easy list comprehension.  It is plain
to see that list comprehensions are much more concise.

Java Code ::

	// Define original integer array
        int[] ages = {20, 25, 28, 30};


        // Print original int array
        System.out.println("Starting List:");

        for (int age : ages) {
            System.out.println(age);
        }

        // Create new int array by adding one to each element of first array
        int x = 0;
        int[] newages = new int[4];
        for (int age : ages) {
            newages[x] = age+1;
            x++;
        }

        // Print ending list
        System.out.println("Ending List:");
        for (int age : newages) {
            System.out.println(age);

        }

Dictionaries
~~~~~~~~~~~~

A dictionary is quite different than a typical list in Python as there is no automatically populated index for any given element
within the dictionary.  When you use a list, you need not worry about assigning an index to any value that is placed within it.
However, a dictionary forces the developer to assign an index or “key” for every element that is placed into the construct.  Therefore,
each entry into a dictionary requires two values, the *key* and the *element*.

The beauty of the dictionary is that it allows the developer to choose the data type of the key value.  Therefore, if one wishes
to use a string value as a key then it is entirely possible.  Dictionary types also have a multitude of methods and operations that
can be applied to them to make them easier to work with.

=====================================================================================================================================  ============================================================================================================  
Method or Operation                                                                                                                    Description                                                                                                 
=====================================================================================================================================  ============================================================================================================  
len(dictionary)                                                                                                                        Returns number of items within the given dictionary.                                                     
dictionary[key]                                                                                                                        Returns the item from the list that is associated with the given key.                                    
dictionary[key] = value                                                                                                                Sets the associated item in the list to the given value.                                                    
del dictionary[key]                                                                                                                    Deletes the given key/value pair from the list.                                                             
dictionary.clear()                                                                                                                     Removes all items from the dictionary.                                                                      
dictionary.copy()                                                                                                                      Creates a shallow copy of the dictionary.                                                                   
has_key(key)                                                                                                                           Returns a boolean stating whether the dictionary contains the given key.                                 
items()                                                                                                                                Returns a copy of the key/value pairs within the dictionary.                                             
keys()                                                                                                                                 Returns the keys within the dictionary.                                                                  
update([dictionary2])                                                                                                                  Updates dictionary with the key/value pairs from the given dictionary.  Existing keys will be overwritten.  
fromkeys(sequence[,value])                                                                                                             Creates a new dictionary with keys from the given sequence.  The values will be set to the values given.  
values()                                                                                                                               Returns the values within the dictionary.                                                                
get(key[, b])                                                                                                                          Returns the value associated with the given key.  If the key does not exist, then returns b.                
setdefault(key[, b])                                                                                                                   Returns the value associated with the given key.  If the key does not exist, then returns and sets b.       
pop(key[, b])                                                                                                                          Returns and removes the value associated with the given key.  If the key does not exist then returns b.  
popItem()                                                                                                                              Removes and returns the first key/value pair in the dictionary.                                             
iteritems()                                                                                                                            Returns an iterator over the key/value pairs in the dictionary.                                             
iterkeys()                                                                                                                             Returns an iterator over the keys in the dictionary.                                                        
itervalues()                                                                                                                           Returns an iterator over the values in the dictionary.                                                      
=====================================================================================================================================  ============================================================================================================  

Table 2-5.  Mapping type methods and operations.

Now we will take a look at some dictionary examples.  This reference will not show you an example of using each of the mapping operations,
but it should provide you with a good enough base understanding of how they work. ::

	# Create an empty dictionary and a populated dictionary
	>>> myDict={}
	>>> myDict.values()
	[]
	>>> myDict.has_key(1)
	False
	>>> myDict[1] = 'test'
	>>> myDict.values()
	['test']
	>>> len(myDict)
	1

	# Replace the original dictionary with a dictionary containing string-based keys
	# The following dictionary represents a hockey team line
	>>> myDict = {'r_wing':'Josh','l_wing':'Frank','center':'Jim','l_defense':'Leo','r_defense':'Vic'}
	>>> myDict.values()
	['Josh', 'Vic', 'Jim', 'Frank', 'Leo']
	>>> myDict.get('r_wing')
	'Josh'

	# Iterate over the items in the dictionary
	>>> hockeyTeam = myDict.iteritems()
	>>> for player in hockeyTeam:
	...     print player
	... 
	('r_wing', 'Josh')
	('r_defense', 'Vic')
	('center', 'Jim')
	('l_wing', 'Frank')
	('l_defense', 'Leo')

	>>> for key,value in myDict.iteritems():
	...     print key, value
	... 
	r_wing Josh
	r_defense Vic
	center Jim
	l_wing Frank
	l_defense Leo
        
Sets
~~~~

Sets are unordered collections of unique elements.  What makes sets different than other sequence types is that they contain
no indexing.  They are also unlike dictionaries because there are no key values associated with the elements.  They are an arbitrary
collection of unique elements.  Sets cannot contain mutable objects, but they can be mutable.

There are two different types of sets, namely *set* and *frozenset*.  The difference between the two is quite easily conveyed
from the name itself.  A regular *set* is a mutable collection object, whereas a *frozen* set is immutable.  Much like sequences and
mapping types, sets have an assortment of methods and operations that can be used on them.  Many of the operations and methods work
on both mutable and immutable sets.  However, there are a number of them that only work on the mutable set types.  In the two tables
that follow, we’ll take a look at the different methods and operations.



============================  ==============================================================
Method or Operation           Description  
============================  ==============================================================
len(set)                      Returns the number of elements in a given set.   
copy()                      
difference(set2)            
intersection(set2)          
issubbset(set2)             
issuperset(set2)            
symmetric_difference(set2)  
union(set2)                 
============================  ==============================================================

Table 2-6.  Set Type Methods and Operations



===================================  =====================================================================
Method or Operation                  Description  
===================================  =====================================================================
add(item)                            Adds an item to a set if it is not already in the set.  
clear()                              Removes all items in a set.  
difference_update(set2)            
discard(item)                      
intersection_update(set2)          
pop()                              
remove()                           
symmetric_difference_update(set2)  
update(set2)                       
===================================  =====================================================================

Table 2-7.  Mutable Set Type Methods and Operations

Tuples
~~~~~~

Tuples are much like lists, however they are immutable.  Once a tuple has been defined, it cannot be changed.
They contain indexes just like lists, but again, they cannot be altered once defined.  Therefore, the index in
a tuple may be used to retrieve a particular value and not to assign or modify.

Since tuples are a member of the sequence type, they can use the same set of methods an operations available
to all sequence types. ::

	# Creating an empty tuple
	>>> myTuple = ()

	# Creating tuples and using them
	>>> myTuple2 = (1, 'two',3, 'four')
	>>> myTuple2         
	(1, 'two', 3, 'four')
        

Jython Specific Collections
---------------------------

There are a number of Jython specific collection objects that are available for use.  Most of these collection
objects are used to pass data into Java classes and so forth, but they add additional functionality into the Jython
implementation that will assist Python newcomers that are coming from the Java world.  Nonetheless, many of these
additional collection objects can be quite useful under certain situations.

In the Jython 2.2 release, Java collection integration was introduced.  This enables a bidirectional interaction
between Jython and Java collection types.  For instance, a Java ArrayList can be imported in Jython and then used
as if it were part of the language.  Prior to 2.2, Java collection objects could act as a Jython object, but Jython
objects could not act as Java objects. ::

	# Import and use a Java ArrayList
	>>> import java.util.ArrayList as ArrayList
	>>> arr = ArrayList()                      
	>>> arr.add(1)
	True
	>>> arr.add(2)
	True
	>>> print arr
	[1, 2]


Ahead of the integration of Java collections, Jython also had implemented the *jarray* object which basically allows
for the construction of a Java array in Jython.  In order to work with a *jarray*, simply define a sequence type in
Jython and pass it to the *jarray* object along with the type of object contained within the sequence.  The *jarray*
is definitely useful for creating Java arrays and then passing them into java objects, but it is not very useful for
working in Jython objects.  Moreover, all values within a jarray must be the same type.  If you try to pass a sequence
containing multiple types to a jarray then you’ll be given a *TypeError* of one kind or another.

===========  ===  =================  =========
Character         Java Equivalent  
===========  ===  =================  =========
z                                    boolean  
b                                    byte     
c                                    char     
d                                    double   
f                                    float    
h                                    short    
i                                    int      
l                                    long     
===========  ===  =================  =========

Table 2-8. Character Typecodes for use with Jarray ::

	>>> mySeq = (1,2,3,4,5)
	>>> from jarray import array
	>>> array(mySeq,int)
	array(org.python.core.PyInteger, [1, 2, 3, 4, 5])

	>>> myStr = "Hello Jython"
	>>> array(myStr,'c')
	array('c', 'Hello Jython')

Files
-----

File objects are used to read and write data to a file on disk.  The file object is used to obtain a reference
to the file on disk and open it for reading, writing, appending, or a number of different tasks.  If we simply
use the *open(filename[, mode])* function, we can return a file type and assign it to a variable for processing.
If the file does not yet exist on disk, then it will automatically be created.  The *mode* argument is used to
tell what type of processing we wish to perform on the file.  This argument is optional and if omitted then the
file is opened in read-only mode.

=======  ===  ====================================
Mode          Description                         
=======  ===  ====================================
‘r’           read only                           
‘w’           write                               
‘a’           append                              
‘r+’          read and write                      
‘rb’          Windows binary file read            
‘wb’          Windows binary file write           
‘r+b’         Windows binary file read and write  
=======  ===  ====================================

Table 2-9.  Modes of Operations for File Types

	# Open a file and assign it to variable f


There are plenty of methods that can be used on file objects for manipulation of the file content.  We can call
*read([size])* on a file in order to read it’s content.  Size is an optional argument here and it is used to tell
how much content to read from the file.  If it is omitted then the entire file content is read.  The *readline()*
method can be used to read a single line from a file.  *readlines([size])* is used to return a list containing
all of the lines of data that are contained within a file.  Again, there is an optional *size* parameter that
can be used to tell how many bytes from the file to read.  If we wish to place content into the file, the *write(string)*
method does just that.  The *write()* method writes a string to the file.

When writing to a file it is oftentimes important to know exactly what position in the file you are going to write to.
There are a group of methods to help us out with positioning within a file using integers to represent bytes in the file.
The *tell()* method can be called on a file to give the file object’s current position.  The integer returned is in bytes
and is an offset from the beginning of the file.  The *seek(offset, from)* method can be used to change position in a
file.  The *offset* is the number in bytes of the position you’d like to go, and *from* represents the place in the file
where you’d like to calculate the *offset* from.  If *from* equals 0, then the offset will be calculated from the beginning
of the file.  Likewise, if it equals 1 then it is calculated from the current file position, and 2 will be from the end of
the file.  The default is 0 if *from* is omitted.

Lastly, it is important to allocate and de-allocate resources efficiently in our programs or we will incur a memory overhead
and leaks.  The *close()* method should be called on a file when we are through working with it.  The proper methodology
to use when working with a file is to open, process, and then close each time.  However, there are more efficient ways
of performing such tasks.  In Chapter 5 we will discuss the use of context managers to perform the same functionality in
a more efficient manner. ::

	File Manipulation in Python
	# Create a file, write to it, and then read it’s content

	>>> f = open('newfile.txt','r+')
	>>> f.write('This is some new text for our file\n')
	>>> f.write('This should be another line in our file\n')
	#  No lines will be read because we are at the end of the written content
	>>> f.read()
	''
	>>> f.readlines()
	[]
	>>> f.tell()
	75L
	# Move our position back to the beginning of the file
	>>> f.seek(0)
	>>> f.read()
	'This is some new text for our file\nThis should be another line in our file\n'
	>>> f.seek(0)
	>>> f.readlines()
	['This is some new text for our file\n', 'This should be another line in our file\n']
	>>> f.close()

Iterators
---------

The iterator type was introduced into Python back in version 2.2.  It allows for iteration over Python containers.
All iterable containers have built-in support for the iterator type.  For instance, sequence objects are iterable
as they allow for iteration over each element within the sequence.  If you try to return an iterator on an object
that does not support iteration, you will most likely receive an *AttributeError* which tells you that __iter__
has not been defined as an attribute for that object.

Iterators allow for easy access to sequences and other iterable containers.  Some containers such as dictionaries
have specialized iteration methods built into them as you have seen in previous sections.  Iterator objects are
required to support two main methods that form the iterator protocol.  Those methods are defined below.



=====================  ===================================================================================================  =========================================
Method                 Description                              
=====================  ===================================================================================================  =========================================
iterator.__iter__()    Returns the iterator object on a container.  Required to allow use with *for* and *in* statements  
iterator.next()        Returns the next item from a container.  
=====================  ===================================================================================================  =========================================

Table 2-10:  Iterator Protocol

To return an iterator on a container, just assign *container.__iter__()* to some variable.  That variable will become
the iterator for the object.  If using the *next()* call, it will continue to return the next item within the list
until all items have been retrieved.  Once this occurs, a *StopIteration* error is issued.  The important thing to note
here is that we are actually creating a copy of the list when we return the iterator and assign it to a variable.  That
variable returns and removes an item from that copy each time the *next()* method is called on it.  If we continue to
call *next()* on the iterator variable until the *StopIteration* error is issued, the variable will no longer contain
any items and is empty.

Referencing and Copies
======================

Creating copies and referencing items in the Python language is fairly straightforward.  The only thing you’ll need to
keep in mind is that the techniques used to copy mutable and immutable objects differ a bit.

In order to create a copy of an immutable object, you simply assign it to a different variable.  The new variable is an
exact copy of the object.  If you attempt to do the same with a mutable object, you will actually just create a reference
to the original object.  Therefore, if you perform operations on the “copy” of the original then the same operation will
actually be performed on the original.  This occurs because the new assignment references the same mutable object in memory
as the original.  It is kind of like someone calling you by a different name.  One person may call you by your birth name
and another may call you by your nickname, but both names will reference you of course.

To effectively create a copy of a mutable object, you have two choices.  You can either create what is known as a *shallow*
copy or a *deep* copy of the original object.  The difference is that a shallow copy of an object will create a new object
and then populate it with references to the items that are contained in the original object.  Hence, if you modify any of
those items then each object will be affected since they both reference the same items.  A deep copy creates a new object
and then recursively copies the contents of the original object into the new copy.  Once you perform a deep copy of an object
then you can perform operations on the copied object without affecting the original.  You can use the *deepcopy* function in
the Python standard library to create such a copy.  Let’s look at some examples of creating copies in order to give you a
better idea of how this works. ::


	# Create an integer variable, copy it, and modify the copy
	>>> a = 5
	>>> b = a
	>>> print b
	5
	>>> b = a * 5
	>>> b
	25
	>>> a
	5

	# Create a list, assign it to a different variable and then modify
	>>> listA = [1,2,3,4,5,6]
	>>> print listA
	[1, 2, 3, 4, 5, 6]
	>>> listB = listA
	>>> print listB 
	[1, 2, 3, 4, 5, 6]
	>>> del listB[2]
	# Oops, we’ve altered the original list!
	>>> print listA
	[1, 2, 4, 5, 6]

	# Create a deep copy of the list and modify it
	>>> import copy
	>>> listA = [1,2,3,4,5,6]
	>>> listB = copy.deepcopy(listA)
	>>> print listA
	[1, 2, 3, 4, 5, 6]
	>>> del listB[2]
	>>> print listB
	[1, 2, 4, 5, 6]
	>>> print listA
	[1, 2, 3, 4, 5, 6]


Garbage Collection
==================

This is one of those major differences between CPython and Jython.  Unline CPython, Jython does not implement a
reference counting technique for aging out or garbage collection unused objects.  Instead, Jython makes use of the
garbage collection mechanisms that the Java platform provides.  When a Jython object becomes stale or unreachable,
the JVM may or may not reclaim it.  One of the main aspects of the JVM that made developers so happy in the early
days is that there was no longer a need to worry about cleaning up after your code.  In the C programming language,
one must maintain an awareness of which objects are currently being used so that when they are no longer needed the
program would perform some clean up.  Not in the Java world, the gc thread on the JVM takes care of all garbage
collection and cleanup for you.  This is a benefit of using the Jython implementation; unlike Python there is no need
to worry about reference counting.

Even though we haven’t spoken about classes yet, it is a good time to mention that Jython provides a mechanism for
object cleanup.  A finalizer method can be defined in any class in order to ensure that the garbage collector performs
specific tasks.  Any cleanup code that needs to be performed when an object goes out of scope can be placed within
this finalizer method.  It is important to note that the finalizer method cannot be counted on as a method which will
always be invoked when an object is stale.  This is the case because the finalizer method is invoked by the Java garbage
collection thread, and there is no way to be sure when and if the garbage collector will be called on an object.  Another
issue of note with the finalizer is that they incur a performance penalty.  If you’re coding an application that already
performs poorly then it may not be a good idea to throw lots of finalizers into it.


Below is an example of a Jython finalizer.  It is an instance method that must be named __del__. ::

	class MyClass:
	    def __del__(self):
	        pass    # Perform some cleanup here


The downside to using the JVM garbage collection mechanisms is that there is really no guarantee as to when and if an
object will be reclaimed.  Therefore, when working with performance intensive objects it is best to not rely on a finalizer
to be called.  It is always important to ensure that proper coding techniques are used in such cases when working with objects
like files and databases.  Never code the close() method for a file into a finalizer because it may cause an issue if the
finalizer is not invoked.  Best practice is to ensure that all mandatory cleanup activities are performed before a finalizer
would be invoked.

Summary
=======

A lot of material was covered in this chapter.    You should be feeling better acquainted with Python after reading through
this material.  We began the chapter by covering the basics of assignment an assigning data to particular objects or data types.
We learned that working with each type of data object opens different doors as the way we work with each type of data object
differs.  Our journey into data objects began with numbers and strings, and we discussed the many functions available to the
string object.  We learned that strings are part of the sequence family of Python collection objects along with lists and tuples.
We covered how to create and work with lists, and the variety of options available to us when using lists.  We discovered that
list comprehensions can help us create copies of a given list and manipulate their elements according to an expression or function.
After discussing lists, we went on to discuss dictionaries, sets and tuples.  These objects give us different alternatives to
the list object.  

After discussing the collection types, we learned that Jython has it’s own set of collection objects that differ from those in
Python.  We can leverage the advantage of having the Java platform at our fingertips and use Java collection types from within
Jython.  Likewise, we can pass a Jython collection to Java as a *jarray* object.  We followed that topic with a discussion of file
objects and how they are used in Python.  The topic of iteration and creating iterables followed.  We finished up by discussing
referencing, copies, and garbage collection.  We saw how creating different copies of objects does not always give you what you’d
expect, and that Jython garbage collection differs quite a bit from that of Python.

The next chapter will help you to combine some of the topics you’ve learned about in this chapter as you will learn how to define
expressions and work with control flow.






