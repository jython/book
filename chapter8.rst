Chapter 8:  Scripting with Jython
+++++++++++++++++++++++++++++++++

In this chapter we will look at scripting with Jython, that is, writing small
programs to help out with daily tasks like deleting and creating directories,
mananging files and programs, or anything else that feels repetitive that you
might be able to express as a small program. We'll start with an overview of
some of the most helpful modules that come with Jython for these tasks. These
modules are os, shutil, getopt, optparse, subprocess. We will just be giving
you a quick feel for these modules.  For details you should look at reference
documentation like (FJW: reference needed).  Then we'll cover a medium sized task
to show the use of a few of these modules together.

Parsing Commandline Options
===========================
Many scripts are simple one-offs that you write once, use, and forget.  Others
become part of your weekly or even daily use over time.  When you find that you
are using a script over and over again, you often find it helpful to pass in
command line options.  There are three main ways that this is done in Jython.
The first way is to hand parse the arguments, the second is the getopt module,
and the third is the newer, more flexible optparse module.

Let's say we have a script called foo.py and you want to be able to give it
some parameters when you invoke it
The name of the script and the arguments passed can be examined by importing
thesys module and inspecting sys.argv like so:

    # script foo.py
    import sys
    
    print sys.argv

If you run the above script with a, b, and c as arguments: ::

    $ jython foo.py a b c
    $ ['foo.py', 'a', 'b', 'c']

The name of the script ended up in sys.argv[0], and the rest in sys.argv[1:].  Often you will see this instead in Jython programs:

    # script foo2.py
    import sys
    
    args = sys.argv[1:]
    print args

Which will result in: ::

    $ jython foo2.py a b c
    $ ['a', 'b', 'c']

If you are going to do more than just feed the arguments to your script
directly, than parsing these arguments by hand can get pretty tedious.  The
Jython libraries include two modules that you can use to avoid tedius hand
parsing.  Those modules are getopt and optparse.  The optparse module is the
newer, more flexible option, so I'll cover that one.  The getopt module is
still useful since it requires a little less code for simpler expected
arguments.  Here is a basic optparse script: ::

    # script foo3.py
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--foo" help="set foo option")
    parser.add_option("-b", "--bar" help="set bar option")
    (options, args) = parser.parse_args()
    print "options: %s" % options
    print "args: %s" % args

Running the above: ::

    $ jython foo3.py -b a --foo b c d
    $ options: {'foo': 'b', 'bar': 'a'}
    $ args: ['c', 'd']

I'll come back to the optparse module with a more concrete example later in
this chapter.

Scripting the filesystem
========================
We'll start with what is probably the simplest thing that you can do to a
filesystem, and that is listing the file contents of a directory. ::

    >>> import os
    >>> os.listdir('.')
    ['ast', 'Doc', 'grammar', 'Lib', 'LICENSE.txt', 'NEWS', 'NOTICE.txt', 'src']

First we imported the os module, and then we executed listdir on the current
directory, indicated by the '.'.  Of course your output will reflect the
contents of your local directory.  The os module contains many of the sorts of
functions that you would expect to see for working with your operating system.
The os.path module contains functions that help in working with filesystem
paths.

Compiling Java Source
=====================

While compiling Java source is not strictly a typical scripting taks, it is a
task that I'd like to show off in my bigger example starting in the next
section.  The API I am about to cover was introduced in JDK 6, and is optional
for JVM vendors to implement.  I know that it works on the JDK 6 from Sun and
on the JDK 6 that ships with Mac OS X.  For more details of the JavaCompiler
API, a good starting point is here: http://java.sun.com/javase/6/docs/api/javax/tools/JavaCompiler.html.  The following is a simple example of the use of this API from Jython ::

    compiler = ToolProvider.getSystemJavaCompiler()
    diagnostics = DiagnosticCollector()
    manager = compiler.getStandardFileManager(diagnostics, None, None)
    units = manager.getJavaFileObjectsFromStrings(names)
    comp_task = compiler.getTask(None, manager, diagnostics, None, None, units)
    success = comp_task.call()
    manager.close()

Scripting processes
===================


Example script: build.py
========================

So I've discussed a few of the modules that tend to come in handy when
writing scripts for Jython.  Now I'll put together a nice medium sized script
to show off what can be done.  I've chosen to write a script that will help
handle a Java build from Jython.  I will want to be able to create a directory
structure, delete the directory structure for a clean build, and of course
compile my Java source files.  First I'll go over how I will compile Java source
files. ::

    from javax.tools import (ForwardingJavaFileManager, ToolProvider,
            DiagnosticCollector,)

    tasks = {}

    def task(func):
        tasks[func.func_name] = func

    @task
    def foo():
        print "hello"

    @task
    def compile():
        files = ["Foo.java"]
        if not _compile(["Foo.java"]):
            quit()
        print "compiled"

    def _log(message):
        if verbose:
            print message

    def _compile(names):
        compiler = ToolProvider.getSystemJavaCompiler()
        diagnostics = DiagnosticCollector()
        manager = compiler.getStandardFileManager(diagnostics, None, None)
        units = manager.getJavaFileObjectsFromStrings(names)
        comp_task = compiler.getTask(None, manager, diagnostics, None, None, units)
        success = comp_task.call()
        manager.close()
        return success
     
    if __name__ == '__main__':
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-f", "--foo", help="set foo option")
        parser.add_option("-b", "--bar", help="set bar option")
        (options, args) = parser.parse_args()
        
        print "options: %s" % options
        print "args: %s" % args

        try:
            current = tasks[args[0]]
        except KeyError:
            print "Task %s not defined." % args[0]
        current()

