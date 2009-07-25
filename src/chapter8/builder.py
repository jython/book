import os
import sys
import glob

from javax.tools import (ForwardingJavaFileManager, ToolProvider,
        DiagnosticCollector,)

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
    parser.add_option("-q", "--quiet", 
            action="store_false", dest="verbose", default=True,
            help="Don't print out task messages.")
    parser.add_option("-p", "--projecthelp", 
            action="store_true", dest="projecthelp",
            help="Print out list of tasks.")
    (options, args) = parser.parse_args()
    
    if options.projecthelp:
        for task in tasks:
            print task
        sys.exit(0)

    if len(args) < 1:
        print "Usage: jython builder.py [options] task"
        sys.exit(1)
    try:
        current = tasks[args[0]]
    except KeyError:
        print "Task %s not defined." % args[0]
        sys.exit(1)
    current()

