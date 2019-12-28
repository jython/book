Chapter 5: Input and Output
+++++++++++++++++++++++++++

A program means very little if it does not take input of some kind from the program user.  Likewise, if there is no form of output from a program then one may ask whey we have a program at all.  Input and output operations can define the user experience and usability of any program.  This chapter is all about how to put information or data into a program, and then how to display it or save it to a file.  This chapter does not discuss working with databases, but rather, working at a more rudimentary level with files.  Throughout this chapter you will learn such techniques as how to input data for a program via a terminal or command line, likewise, you will learn now to read input from a file and write to a file.  After reading this chapter, you should know how to persist Python objects to disk using the *pickle* module and also how to retrieve objects from disk and use them.  There will be a broad variety of topics discussed in this chapter, all of them relating to input and output.

Input from the Keyboard
=======================



As stated in the preface to this chapter, almost every program takes input from a user in one form or another.  Most basic applications allow for keyboard entry via a terminal or command line environment.  Python makes keyboard input easy, and as with many other techniques in Python there are more than one way to enable keyboard input.  In this section, we’ll cover each of those different ways to perform this task, along with a couple of use-cases.  In the end you should be able to identify the most suitable application of this feature for your needs.

sys.stdin and raw_input
-----------------------

Making use of std.stdin is by far the most widely used method to read input from the command line or terminal.  This procedure consists of importing the sys package, then writing a message prompting the user for some input, and lastly reading the input by making a call to *sys.stdin.readln()* and assigning the returned value to a variable.  The process looks like the code that is displayed below. ::

	# Obtain a value from the command line and store it into a variable
	>>> import sys
	>>> sys.stdout.write("Enter your favorite team: ")
	>>> fav_team = sys.stdin.readline()
	>>> print fav_team
	Enter your favorite team: Cubs

You can see that the usage of sys modules is quite simplistic.  However, another approach to performing this same task is to make use of the *raw_input* function.  This function uses a more simplistic syntax in order to perform the same procedure.  It basically generates some text on the command line or terminal, accepts user input, and assigns it to a variable.  Let’s take a look at the same example from above using the *raw_input* syntax. ::

	# Obtain a value using raw_input and store it into a variable
	>>> fav_team = raw_input("Enter your favorite team: ")
	Enter your favorite team: Cubs

Obtaining Variables from Jython Environment
-------------------------------------------

It is possible to retrieve values directly from the Jython environment for use within your applications.  For instance, we can obtain system environment variables or use the variables that are assigned to sys.argv at runtime.

To use environment variable values within your Jython application, simply import the *os* module and use it’s *environ* dictionary to access them.  Since this is a dictionary object, you can obtain a listing of all environment variables by simply typing *os.environ*  at will. ::



	>>> import os
	>>> home = os.environ["HOME"]
	>>> home
	'/Users/juneau'

	# Change home directory for the Python session
	>>> os.environ["HOME"] = "/newhome"
	>>> home = os.environ["HOME"]
	>>> home
	'/newhome'

When you are executing a Jython module from the command prompt or terminal, you can make use of the *sys.argv* list that takes values from the command prompt or terminal after invoking the Jython module.  For instance, if we are interested in having our program user enter some text to be used by the module, they can simply invoke the module and then use type all of the text entries followed by spaces, using quotes if you wish to pass an argument that contains a space.  The number of arguments can be any size (I’ve never hit an upper bound anyways), so the possibilities are endless. ::

	# sysargv_print.py – Prints all of the arguments provided at the command line
	import sys
	    for sysargs in sys.argv:
	        print sysargs

	# Usage
	>>> jython sysargv_print.py "test" "test2" "test3"
	sysargv_print.py
	test
	test2
	test3

As you can see, the first entry in sys.argv is the script name, and then each additional argument provided after the module name is then added to the sys.argv list.  This is quite useful for creating scripts to use for automating tasks, etc.


File I/O
========

We learned a bit about the *File* data type in chapter 2 of this book.  In that chapter, we briefly discussed a few of the operations that can be performed using this type.  In this section, we will go into detail on what we can do with a *File* object.  We’ll start with the basics, and move into more detail.  To begin, you should take a look at the table below that lists all of the methods available to a *File* object and what they do.



=================  ======================================================================================  
Method             Description                                                                     
=================  ====================================================================================== 
close()            Close file                                                                      
fileno()           Returns integer file descriptor                                                 
flush()            Used to flush the output buffers                                                
isatty()           If the file is an interactive terminal, returns 1                               
next()             Returns the next line in the file.  If no line is found, returns StopIteration  
read(x)            Reads x bytes                                                                   
readline(x)        Reads single line up to x characters, or entire line if x is omitted                  
readlines(size)    Reads all lines in file into a list.  If *size* > 0, reads that number of characters  
seek()             Moves cursor to a new position in the file                                      
tell()             Returns the current position of the cursor                                      
truncate()         Truncates a file                                                                      
write(string)      Writes a string                                                                       
writelines(seq)    Writes all strings contained in a sequence                                            
=================  ======================================================================================  

Table 9-1:  File Object Methods

We’ll start by creating a file for use.  As discussed in chapter 2, the *open(filename[, mode])* built-in function creates and opens a specified file in a particular manner.  The *mode* specifies what mode we will open the file into, be it read, read-write, etc.  ::

	>>> myFile = open('mynewfile.txt','w')
	>>> firstString = “This is the first line of text.”
	>>> myFile.write(firstString)
	>>> myFile.close()

In the example above, the file “mynewfile.txt” did not exist until the *open* function was called.  The file was created in *write* mode and then we do just that, write a string to the file.  Now, it is important to make mention that the *firstString* is not actually written to the file until it is closed or *flush() *is performed.  It is also worth mentioning that if we were to perform a subsequent *write()* operation on the file then the first contents of the file would be overwritten by the subsequent contents.

Now we’ll step through each of the file functions in an example.  The main focus of this example is to provide you with a place to look for actual working file I/O code.  ::

	# Write lines to file, flush, and close
	>>> myFile.write('This is the first line of text.')
	>>> myFile.write('This is the second line of text.')
	>>> myFile.write('This is the last line of text.')
	>>> myFile.flush()
	>>> myFile.close()

	# Open file in read mode
	>>> myFile = open('mynewfile.txt','r')
	>>> myFile.read()
	'My second line of text.This is the first line of text.This is the second line of text.This is the last line of text.'

	# If we read again, we get a ‘’ because cursor is at the end of text
	>>> myFile.read()
	''

	# Seek back to the beginning of file and perform read again
	>>> myFile.seek(0)
	>>> myFile.read()
	'My second line of text.This is the first line of text.This is the second line of text.This is the last line of text.'

	# Seek back to beginning of file and perform readline()
	>>> myFile.seek(0)
	>>> myFile.readline()
	'This is the first line of text.This is the second line of text.This is the last line of text.'

	# Use tell() to display current cursor position
	>>> myFile.tell()
	93L
	>>> myFile.seek(0)
	>>> myFile.tell()
	0L

	# Loop through lines of file
	>>> for line in myFile:
	...     print line
	... 
	This is the first line of text.This is the second line of text.This is the last line of text.


There are a handful of read-only attributes that we can use to find out more information about file objects.  For instance, if we are working with a file and want to see if it is still open or if it has been closed, we could view the *closed* attribute on the file to return a boolean stating whether the file is closed.  The following table lists each of these attributes and what they tell us about a file object.

===========  =====================================================
Attribute    Description                                          
===========  =====================================================
closed       Returns a boolean to indicate if the file is closed  
encoding     Returns a string indicating encoding on file    
mode         Returns the I/O mode for a file                      
name         Returns the name of the file                         
newlines     Returns the newline representation in the file  
===========  ===================================================== 

File Attributes ::

	>>> myFile.closed
	False
	>>> myFile.mode
	'r'
	>>> myFile.name
	'mynewFile.txt'


Pickle
======

One of the most popular modules in the Python language is the *pickle* module.  The goal of this module is basically to allow for the serialization and persistence of Python objects to disk in file format.  A *pickled* object can be written to disk using this module, and it can also be read back in and utilized in object format.  Just about any Python object can be persisted using *pickle*.

To write an object to disk, we call the *pickle()* function.  The object will be written to file in a format that my be unusable by anything else, but we can then read that file back into our program and use the object as it was prior to writing it out.  In the following example, we’ll create a *Player* object and then persist it to file using *pickle.*  Later, we will read it back into a program and make use of it.  We will make use of the *File* object when working with the *pickle* module. ::

	>>> import pickle
	>>> class Player(object):
	...     def __init__(self, first, last, position):
	...         self.first = first
	...         self.last = last 
	...         self.position = position
	...   
	>>> player = Player('Josh','Juneau','Forward')
	>>> pickleFile = open('myPlayer','wb')
	>>> pickle.dump(player, pickleFile)
	>>> pickleFile.close()

In the example above, we’ve persisted a *Player* object to disk using the *dump(object, file)* method in the *pickle* module.  Now let’s read the object back into our program and print it out. ::

	>>> pickleFile = open('myPlayer','rb')
	>>> player1 = pickle.load(pickleFile)
	>>> pickleFile.close()
	>>> player1.first
	'Josh'
	>>> player1.last, player1.position
	('Juneau', 'Forward')


Similarly, we read the pickled file back into our program using the 	load(file)	 method.  Once read and stored into a variable, we can close the file and work with the object.  If we had to perform a sequence of 	dump	 or 	load	 tasks, we could do so one after the other without issue.  You should also be aware that there are different 	pickle 	protocols that can be used in order to make 	pickle	 work in different Python environments.  The default protocol is 0, but protocols 1 and 2 are also available for use.  It is best to stick with the default as it works well in most situations, but if you run into any trouble using 	pickle 	with binary formats then please give the others a try.

If we had to store objects to disk and reference them at a later time, it may make sense to use the 	shelve	 module which acts like a dictionary for pickeled objects.  With the 	shelve	 technique, you basically 	pickle	 an object and store it using a string-based key value.  You can later retrieve the object by passing the key to the opened file object.  This technique is very similar to a filing cabinet for our objects in that we can always reference our objects by key value.  Let’s take a look at this technique and see how it works. ::

	# Store different player objects
	>>> import shelve
	>>> player1 = Player('Josh','Juneau','forward')
	>>> player2 = Player('Jim','Baker','defense')
	>>> player3 = Player('Frank','Wierzbicki','forward')
	>>> player4 = Player('Leo','Soto','defense')
	>>> player5 = Player('Vic','Ng','center')
	>>> data = shelve.open("players")
	>>> data['player1'] = player1
	>>> data['player2'] = player2
	>>> data['player3'] = player3
	>>> data['player4'] = player4
	>>> data['player5'] = player5
	>>> playerTemp = data['player3']
	>>> playerTemp.first, playerTemp.last, playerTemp.position
	('Frank', 'Wierzbicki', 'forward')
	>>> data.close()

In the scenario above, we used the same *Player* object that was defined in the previous examples.  We then opened a new *shelve* and named it “players”, this shelve actually consists of a set of three files that are written to disk.  These three files can be found on disk named “players.bak”, “players.dat”, and “players.dir” once the objects were persisted into the *shelve* and it was closed.  As you can see, all of the *Player* objects we’ve instantiated have all been stored into this *shelve* unit, but they exist under different keys.  We could have named the keys however we wished, as long as they were each unique.  In the example, we persist five objects and then at the end one of the objects is retrieved and displayed.  This is quite a nice technique to make a small data store.

Output Techniques
=================

We basically covered the *print* statement in chapter 2 very briefly when discussing string formatting.  The *print* statement is by far the most utilized form of output in most Python programs.  Although we covered some basics such as conversion types and how to format a line of output in chapter 2, here we will go into a bit more depth on some different variations of the *print* statement as well as other techniques for generating output.  There are basically two formats that can be used with the *print* statement.  We covered the first in chapter two, and it makes use of a string and some conversion types embedded within the string and preceded by a percent (%) symbol.  After the string, we use another percent(%) symbol followed by a parenthesized list of arguments that will be substituted in place of the embedded conversion types in our string in order.  We can also use a comma instead of a percent symbol in order to achieve the same effect.  It is merely a matter of preference.  Check out the examples of each depicted in the example below. ::

	# Using the % symbol
	>>> x = 5
	>>> y = 10
	>>> print 'The sum of %d and %d is %d' % (x, y, (x + y))
	The sum of 5 and 10 is 15

	>>> adjective = "awesome"
	>>> print 'Jython programming is %s' % (adjective)
	Jython programming is awesome


	# Using a comma
	>>> print y, " divided by ", x, " is ", y/5
	10  divided by  5  is  2
        

You can also format floating-point output using the conversion types that are embedded in your string.  You may specify a number of decimal places you’d like to print by using a “.# of places” syntax in the embedded conversion type. ::

	>>> pi = 3.14
	>>> print 'Here is some formatted floating point arithmetic: %.2f' % (pi + y) 
	Here is some formatted floating point arithmetic: 13.14
	>>> print 'Here is some formatted floating point arithmetic: %.3f' % (pi + y)
	Here is some formatted floating point arithmetic: 13.140


If we were working with a list or a range of numbers, we could use a generator to help us with output.  It works like as follows:  create a generator function that “prints” some output using the *yield* statement.  Assign the returned value(s) from the generator to a variable, then print the variable to see the outcome. ::

	>>> def writeX(upper, lower):
	...     x = lower
	...     y = upper
	...     while x < y:
	...         yield 'The value of x is: %d' % (x+1)
	...         x = x + 1
	... 
	>>> out = "".join(writeX(10,5))
	>>> print out
	The value of x is: 6The value of x is: 7The value of x is: 8The value of x is: 9The value of x is: 10


Conclusion
==========

It goes without saying that Python has its share of input and output strategies.  This chapter covered most of those techniques starting with basic terminal or command line I/O and then onto file manipulation.  We learned how to make use of the *open* function for creating, reading, or writing a file.  The command line sys.argv arguments are another way that we can grab input, and environment variables can also be used from within our programs.  Following those topics, we took a brief look at the *pickle* module and how it can be used to persist Python objects to disk.  *shelve* is another twist on using *pickle* that allows for multiple objects to be indexed and stored within the same file.  Finally, we discussed a couple of techniques for performing output in our programs.



Although there are some details that were left out as I/O could consume an entire book, this chapter was a solid starting point into the broad topic of I/O in Python.  As with much of the Python language specifics discussed in this book, there are many resources available on the web and in book format that will help you delve deeper into the topics if you wish.



In the next chapter, we will discuss using Jython and Java together.  This topic is at the heart of Jython, it is one of the main reasons why Python was implemented in Java.  


