Appendix A:  Using Other Tools with Jython
==========================================

The primary focus of this appendix is to provide information on using some external
python packages with Jython.  In some circumstances, the tools must be used or installed
a bit differently on Jython than on CPython, and those differences will be noted.  Since there
is a good deal of documentation on the usage of these tools available on the web, this appendix
will focus on using the tool specifically with Jython.  However, relevant URLs will be cited
for finding more documentation on each of the topics.

setuptools
----------

Setuptools is a library that builds upon distutils, the standard Python
distribution facility. It offers some advanced tools like ``easy_install``, a
command to automatically download and install a given Python package and its
dependencies.

To get setuptools, download ez_setup.py from
http://peak.telecommunity.com/dist/ez_setup.py. Then, go to the directory where
you left the downloaded file and execute::

    $ jython ez_setup.py

The output will be similar to the following::

    Downloading http://pypi.python.org/packages/2.5/s/setuptools/setuptools-0.6c9-py2.5.egg
    Processing setuptools-0.6c9-py2.5.egg
    Copying setuptools-0.6c9-py2.5.egg to /home/lsoto/jython2.5.0/Lib/site-packages
    Adding setuptools 0.6c9 to easy-install.pth file
    Installing easy_install script to /home/lsoto/jython2.5.0/bin
    Installing easy_install-2.5 script to /home/lsoto/jython2.5.0/bin
    
    Installed /home/lsoto/jython2.5.0/Lib/site-packages/setuptools-0.6c9-py2.5.egg
    Processing dependencies for setuptools==0.6c9
    Finished processing dependencies for setuptools==0.6c9

As you can read on the output, the ``easy_install`` script has been installed to the
``bin`` directory of the Jython installation (``/home/lsoto/jython2.5.0/bin`` in
the example above). If you work frequently with Jython it's a good idea to
prepend this directory to the ``PATH`` environment variable, so you don't have
to type the whole path each time you want to use ``easy_install`` or other
scripts installed to this directory. From now on I'll assume that this is the
case. If you don't want to prepend Jython's bin directory to your ``PATH`` for
any reason, remember to type the complete path on each example (i.e., type
``/path/to/jython/bin/easy_install`` when I say ``easy_install``).

OK, so now you have ``easy_install``. What's next? Let's grab a Python library
with it! For example, let's say that we need to access twitter from a program
written in Jython and we want to use python-twitter project, located at
http://code.google.com/p/python-twitter/.

Without ``easy_install`` you would go to that URL, read the building
instructions and after downloading the latest version and executing a few
commands you should be ready to go. Except that libraries often depend on other
libraries (as the case with python-twitter which depends on simplejson)
so you would have to repeat this boring process a few times.

With ``easy_install`` you simply run::

  $ easy_install python-twitter

And you get the following output::

  Searching for python-twitter
  Reading http://pypi.python.org/simple/python-twitter/
  Reading http://code.google.com/p/python-twitter/
  Best match: python-twitter 0.6
  Downloading http://python-twitter.googlecode.com/files/python-twitter-0.6.tar.gz
  Processing python-twitter-0.6.tar.gz
  Running python-twitter-0.6/setup.py -q bdist_egg --dist-dir /var/folders/mQ/mQkMNKiaE583pWpee85FFk+++TI/-Tmp-/easy_install-FU5COZ/python-twitter-0.6/egg-dist-tmp-EeR4RD
  zip_safe flag not set; analyzing archive contents...
  Unable to analyze compiled code on this platform.
  Please ask the author to include a 'zip_safe' setting (either True or False) in the package's setup.py
  Adding python-twitter 0.6 to easy-install.pth file
  
  Installed /home/lsoto/jython2.5.0/Lib/site-packages/python_twitter-0.6-py2.5.egg
  Processing dependencies for python-twitter
  Searching for simplejson
  Reading http://pypi.python.org/simple/simplejson/
  Reading http://undefined.org/python/#simplejson
  Best match: simplejson 2.0.9
  Downloading http://pypi.python.org/packages/source/s/simplejson/simplejson-2.0.9.tar.gz#md5=af5e67a39ca3408563411d357e6d5e47
  Processing simplejson-2.0.9.tar.gz
  Running simplejson-2.0.9/setup.py -q bdist_egg --dist-dir /var/folders/mQ/mQkMNKiaE583pWpee85FFk+++TI/-Tmp-/easy_install-VgAKxa/simplejson-2.0.9/egg-dist-tmp-jcntqu
  ***************************************************************************
  WARNING: The C extension could not be compiled, speedups are not enabled.
  Failure information, if any, is above.
  I'm retrying the build without the C extension now.
  ***************************************************************************
  ***************************************************************************
  WARNING: The C extension could not be compiled, speedups are not enabled.
  Plain-Python installation succeeded.
  ***************************************************************************
  Adding simplejson 2.0.9 to easy-install.pth file
  
  Installed /home/lsoto/jython2.5.0/Lib/site-packages/simplejson-2.0.9-py2.5.egg
  Finished processing dependencies for python-twitter

The output is a bit verbose, but it gives you a detailed idea of the steps
automated by ``easy_install``. Let's review it piece by piece::

  Searching for python-twitter
  Reading http://pypi.python.org/simple/python-twitter/
  Reading http://code.google.com/p/python-twitter/
  Best match: python-twitter 0.6
  Downloading http://python-twitter.googlecode.com/files/python-twitter-0.6.tar.gz

We asked for "python-twitter", which is looked up on PyPI, the Python Package
Index which lists all the Python packages produced by the community. The version
0.6 was selected since it was the most recent version at the time I ran the
command. 

Let's see what's next on the ``easy_install`` output::

  Running python-twitter-0.6/setup.py -q bdist_egg --dist-dir /var/folders/mQ/mQkMNKiaE583pWpee85FFk+++TI/-Tmp-/easy_install-FU5COZ/python-twitter-0.6/egg-dist-tmp-EeR4RD
  zip_safe flag not set; analyzing archive contents...
  Unable to analyze compiled code on this platform.
  Please ask the author to include a 'zip_safe' setting (either True or False) in the package's setup.py
  Adding python-twitter 0.6 to easy-install.pth file
  
  Installed /home/lsoto/jython2.5.0/Lib/site-packages/python_twitter-0.6-py2.5.egg

Nothing special here: it ran the needed commands to install the library. The
next bits are more interesting::

  Processing dependencies for python-twitter
  Searching for simplejson
  Reading http://pypi.python.org/simple/simplejson/
  Reading http://undefined.org/python/#simplejson
  Best match: simplejson 2.0.9
  Downloading http://pypi.python.org/packages/source/s/simplejson/simplejson-2.0.9.tar.gz#md5=af5e67a39ca3408563411d357e6d5e47

As you can see, the dependency on simplejson was discovered and, since it is not
already installed it is being downloaded. Next we see::

  Processing simplejson-2.0.9.tar.gz
  Running simplejson-2.0.9/setup.py -q bdist_egg --dist-dir /var/folders/mQ/mQkMNKiaE583pWpee85FFk+++TI/-Tmp-/easy_install-VgAKxa/simplejson-2.0.9/egg-dist-tmp-jcntqu
  ***************************************************************************
  WARNING: The C extension could not be compiled, speedups are not enabled.
  Failure information, if any, is above.
  I'm retrying the build without the C extension now.
  ***************************************************************************
  ***************************************************************************
  WARNING: The C extension could not be compiled, speedups are not enabled.
  Plain-Python installation succeeded.
  ***************************************************************************
  Adding simplejson 2.0.9 to easy-install.pth file
  
  Installed /home/lsoto/jython2.5.0/Lib/site-packages/simplejson-2.0.9-py2.5.egg

The warnings are produced because the ``simplejson`` installation tries to
compile a C extension which for obvious reasons only works with CPython and not
with Jython.

Finally, we see::

  Finished processing dependencies for python-twitter

Which signals the end of the automated installation process for
python-twitter. You can test that it was successfully installed by running
Jython and doing an ``import twitter`` on the interactive interpreter.

As noted above ``easy_install`` will try to get the latest version for the
library you specify. If you want a particular version, for example the 0.5
release of python-twitter then you can specify it in this way::

  $ easy_install python-twitter==0.5

.. warning::

  Note that it's not a good idea to have two version of the same library
  installed at the same time. Take a look at the `virtualenv`_ section below for
  a solution to the problem of running different programs requiring different
  versions of the same library.

For debugging purposes is always useful to know where the bits installed using
``easy_install`` go. As you can stop of the install output, they are installed
into ``<path-to-jython>/Lib/site-packages/<name_of_library>-<version>.egg``
which may be a directory or a compressed zip file. Also, ``easy_install`` adds
an entry to the file ``<path-to-jython>/Lib/site-packages/easy-install.pth``,
which ends up adding the directory or zip file to ``sys.path`` by default.

Unfortunately setuptools don't provide any automated way to uninstall
packages. You will have to manually delete the package egg directory or zip file
and remove the associated line on ``easy-install.pth``.


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

