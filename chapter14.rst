Chapter 14:  Web Applications with Django
=========================================

J2EE deployment and integration
-------------------------------

At the time of this writing, Django on Jython works on the 1.0.x release.
Unfortunately, the official Django site hasn't released a new build with all
the latest patches from source control.  To download the latest 1.0.x
release, you'll need to download the code with subversion and install
it ::

    svn co http://code.djangoproject.com/svn/django/tags/releases/1.0.2/ django-1.0.x
    cd django-1.0.x
    jython setup.py install

Next, you'll need to install the DjangoOnJython - a set of extensions
to Django to enable Jython integration. Grab the latest release from
Google Code ::

    http://code.google.com/p/django-jython/downloads/list

Download either the zip or the tar file and run "jython setup.py install" on
the package. This will install the 'doj' package into your Jython
installation. You've now got everything you need to start deploying
Django on Jython applications into a servlet container. 

Although you *could* deploy your application using Django's built in
development server, it's a terrible idea.  The development server
isn't designed to operate under heavy load and this is really a job
that is more suited to a proper application server.  We're going to
install Glassfish v2.1 - an opensource highly performant J2EE
application server from Sun Microsystems and show deployment onto it.

Let's install Glassfish now - obtain the release from ::

    https://glassfish.dev.java.net/public/downloadsindex.html

At the time of this writing, Glassfish v3.0 is being prepared for
release and it will support Django and Jython out of the box, but
we'll stick to the stable release as the documentation and stability
has been well established.  Download the v2.1 release (currently
v2.1-b60e).  I strongly suggest you use JDK6 to do your deployment.

Once you have the installation JAR file, you can install it by issuing
::

   % java -Xmx256m -jar glassfish-installer-v2.1-b60e-windows.jar


If your glassfish installer file has a different name, just use that
instead of the filename listed in the above example. Be careful where
you invoke this command though - Glassfish will unpack the application
server into a subdirectory 'glassfish' in the directory that you start
the installer.

One step that tripped me up during my impatient installation of
Glassfish is that you actually need to invoke ant to complete the
installation.  On UNIX you need to invoke ::

    % chmod -R +x lib/ant/bin
    % lib/ant/bin/ant -f setup.xml 

or for Windows ::

    % lib\ant\bin\ant -f setup.xml

This will complete the setup - you'll find a bin directory with
"asadmin" or "asadmin.bat" which will indicate that the application
server has been installed.. You can start the server up by invoking ::

    % bin/asadmin start_domain -v

On Windows, this will start the server in the foreground - the process
will not daemonize and run in the background.  On UNIX operating
systems, the process will automatically daemonize and run in the
background. In either case, once the server is up and running, you
will be able to reach the web administration screen through a browser
by going to http://localhost:5000/. The default login is 'admin' and
the password is 'adminadmin'.

Currently, Django on Jython only supports the Postgresql database
officially, but there is a preliminary release of a SQL Server backend
as well as a SQLite3 backend.  Let's get the postgresql backend
working - you will need to obtain the Postgresql JDBC driver from
http://jdbc.postgresql.org.   

At the time of this writing, the latest version was in
postgresql-8.4-701.jdbc4.jar, copy that jar file into your
GLASSFISH_HOME/domains/domain/domain1/lib directory. This will enable
all your applications hosted in your appserver to use the same JDBC
driver.

You should now have a GLASSFISH_HOME/domains/domain1/lib directory with the
following contents ::

    applibs/
    classes/
    databases/
    ext/
    postgresql-8.3-604.jdbc4.jar

You will need to stop and start the application server to let those
libraries load up. ::

    % bin/asadmin stop_domain
    % bin/asadmin start_domain -v

Deploying your first application
--------------------------------

Django on Jython includes a built in command to support the creation of WAR
files, but first, you will need to do a little bit of configuration you will
need to make everything run smoothly.  First we'll setup a simple Django
application that has the administration application enabled so that we have
some models that we play with.  Create a project called 'hello' and make sure
you add 'django.contrib.admin' and 'doj' applications to the INSTALLED_APPS.

Now enable the user admin by editting urls.py and uncomment the admin lines.
Your urls.py should now look something like this ::

    from django.conf.urls.defaults import *
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = patterns('',
        (r'^admin/(.*)', admin.site.root),
    )

One downside with running Django on Jython is that there is only support for
Postgresql currently.  Work is underway to support MSSQL, Oracle and SQLite.
For now, let's just use the postgresql backend to get things going.

Disabling Postgresql logins
---------------------------

The first thing I inevitably do on a development machine with Postgresql is
disable authenticaion checks to the database.  The fastest way to do this is to enable
only local connections to the database by editting the pg_hba.conf file.  For
Postgresql 8.3, this file is typically located in
c:\postgresql\8.3\data\pg_hba.conf and on UNIXes - it is typically located in
/etc/postgresql/8.3/data/pg_hba.conf  

At the bottom of the file, you'll find connection configuration information.
Comment out all the lines and enable trusted connections from localhost. 
Your editted configuration should look something like this ::

    # TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD
    host    all         all         127.0.0.1/32          trust

This will let any username password to connect to the database.  You do not
want to do this for a public facing production server.  Consult the Postgresql
documentation for instructions for more suitable settings.  After you've
editted the connection configuration, you will need to restart the
postgresql server.

Create your postgresql database using the createdb command now ::

    > createdb demodb

Setting up the database is straightforward - just enable the pgsql
backend from Django on Jython.  Note that backend will expect a
username and password pair even though we've disabled them in
Postgresql.  You can populate anything you want for the DATABASE_NAME
and DATABASE_USER settings.  The database section of your settings
module should now look something like this ::

   DATABASE_ENGINE = 'doj.backends.zxjdbc.postgresql'
   DATABASE_NAME = 'demodb' 
   DATABASE_USER = 'ngvictor' 
   DATABASE_PASSWORD = 'nosecrets'

Initialize your database now 

    > jython manage.py syncdb
    Creating table django_admin_log
    Creating table auth_permission
    Creating table auth_group
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username: admin
    E-mail address: admin@abc.com
    Warning: Problem with getpass. Passwords may be echoed.
    Password: admin
    Warning: Problem with getpass. Passwords may be echoed.
    Password (again): admin
    Superuser created successfully.
    Installing index for admin.LogEntry model
    Installing index for auth.Permission model
    Installing index for auth.Message model


All of this should be review so far, now we're going to take the
application and deploy it into the running Glassfish server.  This is
actually the easy part. Django on Jython comes with a custom 'war'
command that builds a self contained file which you can use to deploy
into any Java servlet container.

A note about WAR files
----------------------

For J2EE servers, a common way to deploy your applications is to
deploy a 'WAR' file.  This is just a fancy name for a zip file that
contains your application and any dependencies it requires that the
application server has not made available as a shared resource.  This
is a robust way of making sure that you minimize the impact of
versioning changes of libraries if you want to deploy multiple
applications in your app server.

Consider your Django applications over time - you will undoubtedly
upgrade your version of Django, you may upgrade the version of your
database drivers - you may even deciede to upgrade the version of the
Jython language you wish to deploy on.  These choices are ultimately
up to you if you bundle all your dependencies in your WAR file.
By bundling up all your dependencies into your WAR file, you
can ensure that your app will "just work" when you go to deploy it.
The server will automatically partition each application into its own
space with concurrently running versions of the same code. 


---

To enable the war command, add the 'doj' appplication to your
settings in the INSTALLED_APPS list.  Next, you will need to enable
your site's media directory and a context relative root for your
media.  Edit your settings.py module so that that your media files are 
properly configured to be served.  The war command will automatically
configure your media files so that they are served using a static file
servlet and the URLs will be remapped to be after the context root.

Edit your settings module and configure the MEDIA_ROOT and MEDIA_URL lines.

MEDIA_ROOT = 'c:\\dev\\hello\\media_root'
MEDIA_URL = '/site_media/'

Now you will need to create the media_root subdirectory under your 'hello'
project and drop in a sample file so you can verify that static content serving
is working.  Place a file "sample.html" into yoru media_root directory.  Put
whatever contents you want into it - we're just using this to ensure that
static files are properly served.

In english - that means when the above configuration is used - 'hello'
will deployed into your servlet container and the container will
assign some URL path to be the 'context root' in Glassfish's case -
this means your app will live in 'http://localhost:8000/hello/'.  The
site_media directory will be visible at
"http://localhost:8000/hello/site_media".  DOJ will automatically set
the static content to be served by Glassfish's fileservlet which is
already highly performant.  There is no need to setup a separate
static file server for most deployments.

Build your war file now using the standard manage.py script, and
deploy using the asadmin tool ::

    c:\dev\hello>jython manage.py war

    Assembling WAR on c:\docume~1\ngvictor\locals~1\temp\tmp1-_snn\hello

    Copying WAR skeleton...
    Copying jython.jar...
    Copying Lib...
    Copying django...
    Copying media...
    Copying hello...
    Copying site_media...
    Copying doj...
    Building WAR on C:\dev\hello.war...
    Cleaning c:\docume~1\ngvictor\locals~1\temp\tmp1-_snn...

    Finished.

    Now you can copy C:\dev\hello.war to whatever location your application server wants it.

    C:\dev\hello>cd \glassfish
    C:\glassfish>bin\asadmin.bat deploy hello.war
    Command deploy executed successfully.

    C:\glassfish>

That's it.  You should now be able to see your application running on ::

    http://localhost:8080/hello/

The administration screen should also be visible at :

    http://localhost:8080/hello/admin/

You can verify that your static media is being served correctly by going to:

    http://localhost:8080/hello/site_media/sample.html

That's it.  Your basic deployment to a servlet container is now working.

Extended installation
---------------------

XXX: TODO: war command extensions

Connection pooling with J2EE
----------------------------

While Django does not natively support database connection pools with CPython,
you can enable them in the Postgresql driver for Django on Jython.  Creating a
connection pool that is visible to Django/Jython is a two step process in
Glassfish.  First, we'll need to create a JDBC connection pool, then we'll need
to bind a JNDI name to that pool.  In a J2EE container, JNDI - the Java Naming
and Directory Interface - is a registry of names bound to objects.   It's
really best thought of as a hashtable that typically abstracts a factory that
emits objects.

In the case of database connections - JNDI abstracts a ConnectionFactory which
provides proxy objects that behave like database connections.  These proxies
automatically manage all the pooling behavior for us.  Lets see this in
practice now.

First we'll need to create a JDBC ConnectionFactory. Go to the administration
screen of Glassfish and go down to Resources/JDBC/JDBC Resources/Connection
Pools.  From there you can click on the 'New' button and start to configure
your pool.

Set the name to "pgpool-demo", the resource type should be
"javax.sql.ConnectionPoolDataSource" and the Database Vendor should be
PostgreSQL. Click 'Next'.

.. XXX: VN put a screen shot here

At the bottom of the next page, you'll see a section with "Additional
Properties".  You'll need to set four parameters to make sure the connection is
working, assuming that the database is configured for a username/password of
ngvictor/nosecrets - here's what you need to connect to your database.

============== ==========
Name           Value 
============== ==========
databaseName   demodb
serverName     localhost
password       nosecrets
user           ngvictor
============== ==========

You can safely delete all the other properties - they're not needed. Click 'Finish'.

.. XXX: Add screenshot here

Your pool will now be visible on the left hand tree control in the Connection
Pools list. Select it and try pinging it to make sure it's working.  If all is
well, Glassfish will show you a successful Ping message.

.. XXX: add screenshot of 'ping succeeded'

We now need to bind a JNDI name to the connection factory to provide a mechanism for Jython to see the pool.  Go to the JDBC Resources and click 'New'.
Use the JNDI name: "jdbc/pgpool-demo", select the 'pgpool-demo' as your pool name and hit "OK">

.. XXX: add screenshot here of the new JNDI resource

Verify from the command line that the resource is available ::

    glassfish\bin $ asadmin list-jndi-entries --context jdbc
    Jndi Entries for server within jdbc context:
    pgpool-demo__pm: javax.naming.Reference
    __TimerPool: javax.naming.Reference
    __TimerPool__pm: javax.naming.Reference
    pgpool-demo: javax.naming.Reference
    Command list-jndi-entries executed successfully.

Now, we need to enable the Django application use the JNDI name based lookup if
we are running in an application server, and fail back to regular database
connection binding if JNDI can't be found.  Edit your settings.py module and
add an extra configuration to enable JNDI. ::

   DATABASE_ENGINE = 'doj.backends.zxjdbc.postgresql'
   DATABASE_NAME = 'demodb' 
   DATABASE_USER = 'ngvictor' 
   DATABASE_PASSWORD = 'nosecrets'
   DATABASE_OPTIONS  = {'RAW_CONNECTION_FALLBACK': True, \
                        'JNDI_NAME': 'jdbc/pgpool-demo' }

Note that we're duplicating the configuration to connect to the database.  This
is because we want to be able to fall back to regular connection binding in the
event that JNDI lookups fail.  This makes our life easier when we're running in
a testing or development environment.

That's it.

You're finished configuring database connection pooling.  That wasn't that bad
now was it?


Integrating with threadpools
----------------------------
XXX: TODO


Integrating with JMS 
--------------------
XXX: TODO




