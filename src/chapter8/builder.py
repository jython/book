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
    parser.add_option("-q", "--quiet", help="Don't print out task messages")
    (options, args) = parser.parse_args()
    
    print "options: %s" % options
    print "args: %s" % args

    try:
        current = tasks[args[0]]
    except KeyError:
        print "Task %s not defined." % args[0]
    current()

