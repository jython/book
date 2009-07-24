Chapter 17:  GUI Applications
=============================

The C implementation of Python comes with Tcl/TK for writing Graphical User Interfaces (GUIs).  On Jython, the GUI toolkit that you get automatically is Swing, which comes with the Java Platform.  Like CPython, there are other toolkits available for writing GUIs in Jython.  Since Swing is available on any modern Java installation, we will focus on the use of Swing GUIs in this chapter.

Swing is a large subject, and can't really be covered in a single chapter.  In fact there are entire books devoted to the subjuect.  I will provide some introduction to Swing, but only enough to describe the use of Swing from Jython. For in depth coverage of Swing, one of the many books or web tutorials should be used. [FJW: some suggested books/tutorials?].

Using Swing from Jython has a number of advantages over the use of Swing in Java.  For example, bean properties are less verbose in Jython, and binding actions in Jython is much less verbose (in Java anonymous classes are typically used, in Jython a function can be passed).

Let's start with an simple Swing application in Java, then we will look at the same application in Jython.


