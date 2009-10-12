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
one or more virtual environments for a particular Python installation so that the libraries can be installed into controlled
environments other than the global site-packages area for your Python or Jython installation.  The release of Jython 2.5.0 opened new doors
for the possibility of using such tools as virtualenv.

To use virtualenv with Jython, we first need to obtain it.  The easiest way to do so is via the Python Package
Index.  As you had learned in the previous section, easy_install is the way to install packages from the PyPI.  The following
example shows how to install virtualenv using easy_install with Jython.

::
    jython easy_install.py virtualenv

Once installed, it is quite easy to use the tool for creation of a virtual environment.  The virtual environment
will include a Jython executable along with an installation of setuptools and it's own site-packages directory.
This was done so that you have
the ability to install different packages from the PyPI to your virtual environment.  Let's create an enviroment
named JY2.5.1Env using the virtualenv.py module that exists within our Jython environment.

::
    
    jython <<path to Jython>>/jython2.5.1/Lib/site-packages/virtualenv-1.3.3-py2.5.egg/virtualenv.py JY2.5.1Env
    New jython executable in JY2.5.1Env/bin/jython
    Installing setuptools............done.

Now a new directory named JY2.5.1Env should have been created within your current working directory.  You can run
Jython from this virtual environment by simply invoking the executable that was created.  The virtualenv tool allows
us the ability to open a terminal and disignate it to be used for our virutal Jython environment exclusively via the
use of the *activate* command.  To do so, open up a terminal and type the following:
::
    
    source <path-to-virtual-environment/JY2.5.1Env/bin/activate

Once this is done, you should notice that the command line is preceeded with the name of the virutal environment that
you have activated.  Any Jython shell or tool used in this terminal will now be using the virtual environment.  This is an
excellent way to run a tool using two different versions of a particular libarary or for running a production and development
environment side-by-side.  If you run the easy_install.py tool within the activated virtual environment terminal then the tool(s)
will be installed into the virtual environment.  There can be an unlimited number of virtual environments installed
on a particular machine.  To stop using the virtual environment within the terminal, simply type:

::
    
    deactivate

Now your terminal should go back to normal use and default to the global Jython installation.  Once deactivated any of the Jython
references made will call the global installation or libraries within the global site-packages area.  It should be noted that
when you create a virtual environment, it automatically inherits all of the packages used by the global installation.  Therefore
if you have a library installed in your global site-packages area then it can be used from the virtual environment right away.
A good practice is to install only essential libraries into your global Jython environment and then install one-offs or test
libraies into virtual environments.

It is useful to have the ability to list installations that are in use within a particular environment.  One way
to do this is to install the *yolk* utility and make use of it's *-l* command.  In order to install *yolk*, you must
grab a copy of the latest version of Jython beyond 2.5.1 as there has been a patch submitted that corrects some functionaility
which is used by *yolk*.  You must also be running with JDK 1.6 or above as the patched version of Jython makes use
of the *webbrowser* module.  The *webbrowser* module makes use of some java.awt.Desktop features that are only available
in JDK 1.6 and beyond.  To install *yolk*, use the ez_install.py script as we've shown previously.

::
    
    jython ez_install.py yolk

Once installed you can list the package installations for your Jython installations by issuing the *-l* command as follows:

::
    
    yolk -l
    Django          - 1.0.2-final  - non-active development (/jython2.5.1/Lib/site-packages)
    Django          - 1.0.3        - active development (/jython2.5.1/Lib/site-packages/Django-1.0.3-py2.5.egg)
    Django          - 1.1          - non-active development (/jython2.5.1/Lib/site-packages)
    SQLAlchemy      - 0.5.4p2      - active development (/jython2.5.1/Lib/site-packages)
    SQLAlchemy      - 0.6beta1     - non-active development (/jython2.5.1/Lib/site-packages)
    django-jython   - 0.9          - active development (/jython2.5.1/Lib/site-packages/django_jython-0.9-py2.5.egg)
    django-jython   - 1.0b1        - non-active development (/jython2.5.1/Lib/site-packages)
    nose            - 0.11.1       - active development (/jython2.5.1/Lib/site-packages/nose-0.11.1-py2.5.egg)
    setuptools      - 0.6c9        - active 
    setuptools      - 0.6c9        - active 
    snakefight      - 0.4          - active development (/jython2.5.1/Lib/site-packages/snakefight-0.4-py2.5.egg)
    virtualenv      - 1.3.3        - active development (/jython2.5.1/Lib/site-packages/virtualenv-1.3.3-py2.5.egg)
    wsgiref         - 0.1.2        - active development (/jython2.5.1/Lib)
    yolk            - 0.4.1        - active

As you can see, all installed packages will be listed.  If you are using yolk from within a virtual environment then
you will see all packages installed in that virtual environment as well as those installed into the global
environment.

Similarly to setuptools, there is no way to automatically uninstall virtualenv.  You must also manually delete the
package egg directory or zip file as well as remove references within ``easy-install.pth``.




