import sys
import hello, hello.console, hello.window, hello.speech
from optparse import OptionParser
        
def main(args):
    parser = OptionParser()
    parser.add_option('--ui', dest='ui', default='console', 
                      help="Sets the UI to use to greet the user. One of: %s" %
                      ", ".join("'%s'" % ui for ui in hello.list_uis()))
    parser.add_option('--lang', dest='lang', default='en',
                      help="Sets the language to use")
    options, args = parser.parse_args(args)
    if len(args) < 2:        
        print "Sorry, I can't greet you if you don't say your name"
        return 1    
    try:
        hello.greet(args[1], options.lang, options.ui)        
    except hello.LanguageNotSupportedException:
        print "Sorry, I don't speak '%s'" % options.lang
        return 1
    except hello.UINotSupportedExeption:
        print "Invalid UI name\n"    
        print "Valid UIs:\n\n" + "\n".join(' * ' + ui for ui in hello.list_uis())
        return 1
    
if __name__ == "__main__":
    main(sys.argv)    

