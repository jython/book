#! /usr/bin/python

# This is an implementation of the Java OutputStream abstract class
#
# The implementation takes an object to use for writing the stream.  In the
# case of a Jython swing application, a JTextField could be passed in and
# used for writing.
#
# Author: J Juneau

from java.io import OutputStream
from java.lang import String

class JythonOutputStream(OutputStream, object):
    def __init__(self, textfield):
        self.textArea = textfield


    def write(self, b):
        self.textArea.append(b)

    def write(self, b, off, len):
        self.textArea.append(String(b, off, len))
