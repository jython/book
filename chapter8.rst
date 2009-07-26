Chapter 8:  Scripting With Jython
+++++++++++++++++++++++++++++++++

In this chapter we will look at scripting with jython, that is, writing small
programs to help out with daily tasks like deleting and creating directories,
mananging files and programs, or anything else that feels repetitive that you
might be able to express as a small program. We'll start with an overview of
some of the most helpful modules that come with jython for these tasks. These
modules are os, shutil, getopt, optparse, subprocess. We will just be giving
you a quick feel for these modules.  For details you should look at reference
documentation like (fjw: reference needed).  Then we'll cover a medium sized
task to show the use of a few of these modules together.

Parsing Commandline Options
===========================
Many scripts are simple one-offs that you write once, use, and forget.  Others
become part of your weekly or even daily use over time.  When you find that you
are using a script over and over again, you often find it helpful to pass in
command line options.  There are three main ways that this is done in jython.
The first way is to hand parse the arguments, the second is the getopt module,
and the third is the newer, more flexible optparse module.

Let's say we have a script called foo.py and you want to be able to give it
some parameters when you invoke it the name of the script and the arguments
passed can be examined by importing the sys module and inspecting sys.argv like
so:

    # script foo.py
    import sys
    print sys.argv

If you run the above script with a, b, and c as arguments: ::

    $ jython foo.py a b c
    $ ['foo.py', 'a', 'b', 'c']

The name of the script ended up in sys.argv[0], and the rest in sys.argv[1:].  Often you will see this instead in jython programs:

    # script foo2.py
    import sys
    
    args = sys.argv[1:]
    print args

which will result in: ::

    $ jython foo2.py a b c
    $ ['a', 'b', 'c']

If you are going to do more than just feed the arguments to your script
directly, than parsing these arguments by hand can get pretty tedious.  The
jython libraries include two modules that you can use to avoid tedius hand
parsing.  Those modules are getopt and optparse.  The optparse module is the
newer, more flexible option, so i'll cover that one.  The getopt module is
still useful since it requires a little less code for simpler expected
arguments.  Here is a basic optparse script: ::

    # script foo3.py
    from optparse import optionparser
    parser = optionparser()
    parser.add_option("-f", "--foo" help="set foo option")
    parser.add_option("-b", "--bar" help="set bar option")
    (options, args) = parser.parse_args()
    print "options: %s" % options
    print "args: %s" % args

running the above: ::

    $ jython foo3.py -b a --foo b c d
    $ options: {'foo': 'b', 'bar': 'a'}
    $ args: ['c', 'd']

I'll come back to the optparse module with a more concrete example later in
this chapter.

Scripting The Filesystem
========================
We'll start with what is probably the simplest thing that you can do to a
filesystem, and that is listing the file contents of a directory. ::

    >>> import os
    >>> os.listdir('.')
    ['ast', 'doc', 'grammar', 'lib', 'license.txt', 'news', 'notice.txt', 'src']

First we imported the os module, and then we executed listdir on the current
directory, indicated by the '.'.  Of course your output will reflect the
contents of your local directory.  The os module contains many of the sorts of
functions that you would expect to see for working with your operating system.
The os.path module contains functions that help in working with filesystem
paths.

Compiling Java Source
=====================

While compiling java source is not strictly a typical scripting taks, it is a
task that i'd like to show off in my bigger example starting in the next
section.  The api i am about to cover was introduced in jdk 6, and is optional
for jvm vendors to implement.  I know that it works on the jdk 6 from sun and
on the jdk 6 that ships with mac os x.  For more details of the javacompiler
api, a good starting point is here: http://java.sun.com/javase/6/docs/api/javax/tools/javacompiler.html.  The following is a simple example of the use of this api from jython ::

    compiler = toolprovider.getsystemjavacompiler()
    diagnostics = diagnosticcollector()
    manager = compiler.getstandardfilemanager(diagnostics, none, none)
    units = manager.getjavafileobjectsfromstrings(names)
    comp_task = compiler.gettask(none, manager, diagnostics, none, none, units)
    success = comp_task.call()
    manager.close()

Example Script: builder.py
==========================

So i've discussed a few of the modules that tend to come in handy when writing
scripts for jython.  Now i'll put together a simple script to show off what can
be done.  I've chosen to write a script that will help handle the compilation
of java files to .class files in a directory, and clean the directory of .class
files as a separate task.  I will want to be able to create a
directory structure, delete the directory structure for a clean build, and of
course compile my java source files. ::

    import os
    import sys
    import glob

    from javax.tools import (forwardingjavafilemanager, toolprovider,
            diagnosticcollector,)

    tasks = {}

    def task(func):
        tasks[func.func_name] = func

    @task
    def clean():
        files = glob.glob("*.class")
        for file in files:
            os.unlink(file)

    @task
    def compile():
        files = glob.glob("*.java")
        _log("compiling %s" % files)
        if not _compile(files):
            quit()
        _log("compiled")

    def _log(message):
        if options.verbose:
            print message

    def _compile(names):
        compiler = toolprovider.getsystemjavacompiler()
        diagnostics = diagnosticcollector()
        manager = compiler.getstandardfilemanager(diagnostics, none, none)
        units = manager.getjavafileobjectsfromstrings(names)
        comp_task = compiler.gettask(none, manager, diagnostics, none, none, units)
        success = comp_task.call()
        manager.close()
        return success
     
    if __name__ == '__main__':
        from optparse import optionparser
        parser = optionparser()
        parser.add_option("-q", "--quiet", 
                action="store_false", dest="verbose", default=true,
                help="don't print out task messages.")
        parser.add_option("-p", "--projecthelp", 
                action="store_true", dest="projecthelp",
                help="print out list of tasks.")
        (options, args) = parser.parse_args()
        
        if options.projecthelp:
            for task in tasks:
                print task
            sys.exit(0)

        if len(args) < 1:
            print "usage: jython builder.py [options] task"
            sys.exit(1)
        try:
            current = tasks[args[0]]
        except keyerror:
            print "task %s not defined." % args[0]
            sys.exit(1)
        current()

The script defines a "task" decorator that gathers the names of the functions
and puts them in a dictionary.  We have an optionparser class that defines two
options --projecthelp and --quiet.  By default the script logs its actions to
standard out.  --quiet turns this logging off.  --projecthelp lists the
available tasks.  We have defined two tasks, "compile" and "clean".  The
"compile" task globs for all of the .java files in your directory and compiles
them.  The "clean" task globs for all of the .class files in your directory and
deletes them.  Do be careful!  The .class files are deleted without prompting!

So lets give it a try.  If you create a Java class in the same directory as
builer.py, say the classic "Hello World" program:

HelloWorld.java
===============
::

    public class HelloWorld {
       public static void main(String[] args) {
           System.out.println("Hello, World");
       }
    }

You could then issue these commands to builder.py with these results: ::

      [frank@pacman chapter8]$ jython builder.py --help
      Usage: builder.py [options]

      Options:
        -h, --help         show this help message and exit
        -q, --quiet        Don't print out task messages.
        -p, --projecthelp  Print out list of tasks.
      [frank@pacman chapter8]$ jython builder.py --projecthelp
      compile
      clean
      [frank@pacman chapter8]$ jython builder.py compile
      compiling ['HelloWorld.java']
      compiled
      [frank@pacman chapter8]$ ls
      DEBUG.classicHelloWorld.java
      HelloWorld.classicHelloWorldbuilder.py
      [frank@pacman chapter8]$ jython builder.py clean
      [frank@pacman chapter8]$ ls
      HelloWorld.javabuilder.py
      [frank@pacman chapter8]$ jython builder.py --quiet compile
      [frank@pacman chapter8]$ ls
      DEBUG.classicHelloWorldHelloWorld.java
      HelloWorld.classicHelloWorldHelloWorldbuilder.py
      [frank@pacman chapter8]$ 

