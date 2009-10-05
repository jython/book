Appendix A:  Using Other Tools with Jython
==========================================

The primary focus of this appendix is to provide information on using some external
python packages with Jython.  In some circumstances, the tools must be used or installed
a bit differently on Jyton than on CPython, and those differences will be noted.  Since there
is a good deal of documentation on the usage of these tools available on the web, this appendix
will focus on using the tool specifically with Jython.  However, relevant URLs will be cited
for finding more documentation on each of the topics.

setuptools
----------

** (In Progress) **

virtualenv
----------

Oftentimes it is nice to have separate versions of tools running on the same machine.  The virtualenv tool
provides a way to create a virtual Python environment that can be used for various purposes including installation
of different package versions.  Virtual environments can also be nice for those who do not have administrative
access for a particular Python installation but still need to have the ability to install packages to it, such is often
the case when working with domain hosts.  Whatever the case may be, the virtualenv tool provides a means for creating
one or more virtual environments for a particular Python installation.  The release of Jython 2.5.0 opened new doors
for the possibility of using such tools as virtualenv.

To use virtualenv with Jython, we first need to obtain it.  The easiest way to do so is via the Python Package
Index.  As you had learned in the previous section, easy_install is the way to install packages from the PyPI.  The following
example shows how to install virtualenv using easy_install with Jython.

::
    jython easy_install.py virtualenv

Once installed, it is quite easy to use the tool for creation of a virtual environment.  The virtual environment
will include a Jython executable along with an installation of setuptools.  This was done so that you have
the ability to install different packages from the PyPI to your virtual environment.  Let's create an enviroment
named JY2.5.1Env using the virtualenv.py module that exists within our Jython environment.

::
    
    jython <<path to Jython>>/jython2.5.1/Lib/site-packages/virtualenv-1.3.3-py2.5.egg/virtualenv.py JY2.5.1Env
    New jython executable in JY2.5.1Env/bin/jython
    Installing setuptools............done.

Now a new directory named JY2.5.1Env should have been created within your current working directory.  You can run
Jython from this virtual environment by simply invoking the executable that was created.


snakefight
----------

As you have learned in previous chapters, the default file format for installing a Java web application to a Java
application server is the WAR (web archive) file.  When deploying Python applications to
Java application servers, the WAR file is also the standard format that should be used.  The *snakefight* tool
provides a means for creating WAR files for Jython projects using WSGI frameworks.  The snakefight package resides
within the PyPI and can be installed into your Jython environment using easy_install.

