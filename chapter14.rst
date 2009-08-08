Chapter 14:  Web Applications with Django
=========================================

Django basics:

# TODO: walk through of a basic django application
# . Models
# . Exploring the model with the shell
# . Basic query and filter API walk through
# . Enabling the admin for your models
# . Running the debug server
# . URL dispatching
# . Basic form construction and cleaning of data
# . View controllers
# . Templates and Reverse URLs

JavaEE deployment and integration
---------------------------------

At the time of this writing, Django on Jython works on the 1.0.x release.
Unfortunately, the official Django site hasn't released a new build with all
the latest patches from source control.  To download the latest 1.0.x
release, you'll need to download the code with subversion and install
it ::

    svn co http://code.djangoproject.com/svn/django/tags/releases/1.0.2/ django-1.0.x
    cd django-1.0.x
    jython setup.py install

Next, you'll need to install the Django On Jython - a set of extensions
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
install Glassfish v2.1 - an opensource highly performant JavaEE 5 
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
want to do this for a public facing production server.  You should
consult the Postgresql documentation for instructions for more
suitable settings.  After you've editted the connection configuration,
you will need to restart the postgresql server.

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

For JavaEE servers, a common way to deploy your applications is to
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

The war command in doj provides extra options for you to specify extra
JAR files to include with your application and which can bring down the size of
your WAR file. By default, the 'war' command will bundle the following items:

    * Jython
    * Django and it's administration media files
    * your project and media files
    * all of your libraries in site-packages

You can specialize your WAR file to include specific JAR files and you
can instruct doj to assemble a WAR file with just the python packages
that you require.  The respective options for "manage.py war" are
"--include-py-packages" and "--include-jar-libs".  The basic usage is
straight forward, simply pass in the location of your custom python
packages and the JAR files to these two arguments and distutils will
automatially decompress the contents of those compressed volumes and
recompess them into your WAR file.

To bundle JAR files up, you will need to specify a list of files to
"--include-java-libs".  

The following example bundles the jTDS JAR flie and a regular python
module called urllib3 with our WAR file.::

    $ jython manage.py war --include-java-libs=$HOME/downloads/jtds-1.2.2.jar \
            --include-py-package=$HOME/PYTHON_ENV/lib/python2.5/site-packages/urllib3

You can have multiple JAR files or python packages listed, but you
must delimit them with your operating system's path separator.  For
UNIX like systems - this means ":" and for Windows it is ";". 

Eggs can also be installed using "--include-py-path-entries" using the
egg filename.  For example ::

    $ jython manage.py war --include-py-path-entries=$HOME/PYTHON_ENV/lib/python2.5/site-packages/urllib3

Connection pooling with JavaEE
------------------------------

Whenever your web application goes to fetch data from the database,
that data has to come back over a database connection.  Some databases
have 'cheap' database connections like MySQL, but for many databases -
creating and releasing connections is quite expensive.  Under high
load conditions - opening and closing database connections on every
request can quickly consume too many file handles - and your
application will crash.

The general solution to this is to employ database connection pooling.
While your application will continue to create new connections and close them off,
a connection pool will manage your database connections from a
reusable set.  When you go to close your connection - the connection
pool will simply reclaim your connection for use at a later time.
Using a pool means you can put an enforced upper limit restriction on
the number of concurrent connections to the database.  Having that
upper limit means you can reason about how your application will
perform when the upper limit of database connections is hit.

While Django does not natively support database connection pools with CPython,
you can enable them in the Postgresql driver for Django on Jython.  Creating a
connection pool that is visible to Django/Jython is a two step process in
Glassfish.  First, we'll need to create a JDBC connection pool, then we'll need
to bind a JNDI name to that pool.  In a JavaEE container, JNDI - the Java Naming
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


Dealing with long running tasks
-------------------------------

When you're building a complex web application, you will inevitably end up
having to deal with processes which need to be processed in the background.  If
you're building on top of CPython and Apache, you're out of luck here - there's
no standard infrastructure available for you to handle these tasks.   Luckily
these services have had years of engineering work already done for you in the
Java world.   We'll take a look at two different strategies for dealing with
long running tasks.  

Thread Pools
------------

The first strategy is is to leverage managed thread pools in the
JavaEE container.  When your webapplication is running within
Glassfish, each HTTP request is processed by the HTTP Service which
contains a threadpool.  You can change the number of threads to affect
the performance of the webserver.  Glassfish will also let you create
your own threadpools to execute arbitrary work units for you.

The basic API for threadpools is simple:

 * WorkManager which provides an abstracted interface to the thread pool
 * Work is an interface which encapsulates your unit of work
 * WorkListener which is an interface that lets you monitor the
   progress of your Work tasks.


First, we need to tell Glassfish to provision a threadpool for our
use.  In the Adminstration screen, go down to Configuration/Thread
Pools.  Click on 'New' to create a new thread pool.  Give your
threadpool the name "backend-workers".  Leave all the other settings
as the default values and click "OK".

You've now got a thread pool that you can use.  The threadpool exposes
an interface where you can submit jobs to the pool and the pool will
either execute the job synchronously within a thread, or you can
schedule the job to run asynchronously.  As long as your unit of work
implements the javax.resource.spi.work.Work interface, the threadpool
will happily run your code.  A unit of class may be as simple as the
following snippet of code ::

    from javax.resource.spi.work import Work

    class WorkUnit(Work):
        """
        This is an implementation of the Work interface.
        """
        def __init__(self, job_id):
            self.job_id = job_id

        def release(self):
            """
            This method is invoked by the threadpool to tell threads
            to abort the execution of a unit of work.
            """
            logger.warn("[%d] Glassfish asked the job to stop quickly" % self.job_id)

        def run(self):
            """
            This method is invoked by the threadpool when work is
            'running'
            """
            for i in range(20):
                logger.info("[%d] just doing some work" % self.job_id)

This WorkUnit class above doesn't do anything very interesting, but it
does illustrate the basic structure of what unit of work requires.
We're just logging message to disk so that we can visually see the
thread execute.

WorkManager implements several methods which can run your job and
block until the threadpool completes your work, or it can run the job
asynchronously.  Generally, I prefer to run things asynchronously and
simply check the status of the work over time.  This lets me submit
multiple jobs to the threadpool at once and check the status of each
of the jobs.

To monitor the progress of work, we need to implement the WorkListener
interface.  This interface gives us notifications as a task progresses
through the 3 phases of execution within the thread pool.  Those
states are :

 1) Accepted
 2) Started 
 3) Completed

All jobs must go to either Completed or Rejected states. The simplest
thing to do then is to simple build up lists capturing the events.
When the length of the completed and the rejected lists together are
the same as the number of jobs we submitted, we know that we are done.
By using lists instead of simple counters, we can inspect the work
objects in much more detail.

Here's the code for our SimpleWorkListener ::

    from javax.resource.spi.work import WorkListener
    class SimpleWorkListener(WorkListener):
        """
        Just keep track of all work events as they come in
        """
        def __init__(self):
            self.accepted = []
            self.completed = []
            self.rejected = []
            self.started = []

        def workAccepted(self, work_event):
            self.accepted.append(work_event.getWork())
            logger.info("Work accepted %s" % str(work_event.getWork()))

        def workCompleted(self, work_event):
            self.completed.append(work_event.getWork())
            logger.info("Work completed %s" % str(work_event.getWork()))

        def workRejected(self, work_event):
            self.rejected.append(work_event.getWork())
            logger.info("Work rejected %s" % str(work_event.getWork()))

        def workStarted(self, work_event):
            self.started.append(work_event.getWork())
            logger.info("Work started %s" % str(work_event.getWork()))

To access the threadpool, you simply need to know the name of the
pool we want to access and schedule our jobs.  Each time we schedule
a unit of work, we need to tell the pool how long to wait until we
timeout the job and provide a reference to the WorkListener so that we
can monitor the status of the jobs.  

The code to do this is listed below ::

    from com.sun.enterprise.connectors.work import CommonWorkManager
    from javax.resource.spi.work import Work, WorkManager, WorkListener
    wm = CommonWorkManager('backend-workers')
    listener = SimpleWorkListener()
    for i in range(5):
        work = WorkUnit(i)
        wm.scheduleWork(work, -1, None, listener)

You may notice that the scheduleWork method takes in a None in the
third argument.  This is the execution context - for our purposes,
it's best to just ignore it and set it to None.  The scheduleWork
method will return immediately and the listener will get callback
notifications as our work objects pass through.  To verify that all
our jobs have completed (or rejected) - we simply need to check the
listener's internal lists. ::

    while len(listener.completed) + len(listener.rejected) < num_jobs:
        logger.info("Found %d jobs completed" % len(listener.completed))
        time.sleep(0.1)

That covers all the code you need to access thread pools and monitor
the status of each unit of work.  Ignoring the actual WorkUnit class,
the actual code to manage the threadpool is about a dozen lines long.

JavaEE standards and thread pools
-------------------------------

Unfortunately, this API is not standard in the JavaEE 5 specification
yet so the code  listed here will only work in Glassfish.  The
API for parallel processing is being standardized for JavaEE 6, and
until then you will need to know a little bit of the internals of your
particular application server to get threadpools working.  If you're
working with Weblogic or Websphere, you will need to use the CommonJ
APIs to access the threadpools, but the logic is largely the same.

Passing messages across process boundaries
------------------------------------------

While threadpools provide access to background job processing,
sometimes it may be beneficial to have messages pass across process
boundaries.  Every week there seems to be a new Python package that
tries to solve this problem, for Jython we are lucky enough to
leverage Java's JMS.  JMS specifies a message brokering technology
where you may define publish/subscribe or point to point delivery of
messages between different services.  Messages are asychnronously sent
to provide loose coupling and the broker deals with all manner of
boring engineering details like delivery guarantees, security,
durability of messages between server crashes and clustering.

While you could use a handrolled RESTful messaging implementation -
using OpenMQ and JMS has many advantages.

1) It's mature.  Do you really think your messaging implementation
   handles all the corner cases? Server crashes?  Network connectivity
   errors?  Reliability guarantees?  Clustering?  Security? OpenMQ has
   almost 10 years of engineering behind it.  There's a reason for
   that.

2) The JMS standard is just that - standard.  You gain the ability to
   send and receive messages between any JavaEE code.

3) Interoperability.  JMS isn't the only messaging broker in town.
   The Streaming Text Orientated Messaing Protocol (STOMP) is another
   standard that is popular amongst non-Java developers.  You can turn
   a JMS broker into a STOMP broker by using stompconnect.  This means
   you can effectively pass messages between any messaging client and
   any messaging broker using any of a dozen different languages.

In JMS there are two types of message delivery mechanisms:

 * Publish/Subscribe: This is for the times when we want to message
   one or more subscribers about events that are occuring.  This is
   done through JMS 'topics'.
 * Point to point messaging:  These are single sender, single receiver
   message queues.  Appropriately, JMS calls these 'queues'

We need to provision a couple objects in Glassfish to get JMS going.
In a nutshell, we need to create a connection factory which clients
will use to connect to the JMS broker.   We'll create a
publish/subscribe resource and a point to point messaging queue.  In
JMS terms, there are called "destinations".  They can be thought of as
postboxes that you send your mail to.

Go to the Glassfish administration screen and go to Resources/JMS
Resources/Connection Factories.  Create a new connection factory with
the JNDI name: "jms/MyConnectionFactory".  Set the resource type to
javax.jms.ConnectionFactory.  Delete the username and password
properties at the bottom of the screen and add a single property:
'imqDisableSetClientID' with a value of 'false'.  Click 'OK'.

# TODO screenshot of the property setting

By setting the imqDisableSetClientID to false, we are forcing clients
to declare a username and password when they use the
ConnectionFactory.  OpenMQ uses the login to uniquely identify the
clients of the JMS service so that it can properly enforce the
delivery guarantees of the destination.

We now need to create the actual destinations - a topic for
publish/subscribe and a queue for point to point messaging. Go to
Resources/JMS Resources/Destination Resources and click 'New'. Set the
JNDI name to 'jms/MyTopic', the destination name to 'MyTopic' and the
Resource type to be 'javax.jms.Topic'.  Click "OK" to save the topic.

# TODO: create the topic image

Now we need to create the JMS queue for point to point messages.
Create a new resource, set the JNDI name to 'jms/MyQueue', the
destination name to 'MyQueue' and the resource type to
"javax.jms.Queue".  Click OK to save.

# TODO: create the queue image

Like the database connections discussed earlier, the JMS services are
also acquired in the JavaEE container through the use of JNDI name
lookups.  Unlike the database code, we're going to have to do some
manual work to acquire the naming context which we do our lookups
against.    When our application is running inside of Glassfish,
acquiring a context is very simple.  We just import the class and
instantiate it.  The context provides a lookup() method which we use
to acquire the JMS connection factory and get access to the particular
destinations that we are interested in. In the folowing example, I'll
publish a message onto our topic. Lets see some code first and I'll go
over the finer details of what's going on ::

    from javax.naming import InitialContext, Session
    from javax.naming import DeliverMode, Message
    context = InitialContext()

    tfactory = context.lookup("jms/MyConnectionFactory")

    tconnection = tfactory.createTopicConnection('senduser', 'sendpass')
    tsession = tconnection.createTopicSession(False, Session.AUTO_ACKNOWLEDGE)
    publisher = tsession.createPublisher(context.lookup("jms/MyTopic"))

    message = tsession.createTextMessage()
    msg = "Hello there : %s" % datetime.datetime.now()
    message.setText(msg)
    publisher.publish(message, DeliveryMode.PERSISTENT, 
            Message.DEFAULT_PRIORITY, 100)
    tconnection.close()
    context.close()

In this code snippet, we acquire a topic connection through the connection
factory.  To reiterate - topics are for publish/subscribe scenarios.
We create a topic session - a context where we can send and receive
messages to next.  The two arguments passed to creating the topic
session specify a transactional flag and how our client will
acknowledge receipt of messages.  We're giong to just disable
transactions and get the session to automatically send
acknowledgements back to the broker on message receipt.

The last step to getting our publisher is well - creating the
publisher.  From there we can start publishing messages up to the
broker.

At this point - it is important to distinguish between persistent
messages and durable messages.  JMS calls a message 'persistent' if
the messages received by the *broker* are persisted.  This guarantees
that senders know that the broker has received a message.  It makes no
guarantee that messages will actually be delivered to a final
recipient.

Durable subscribers are guaranteed to receive messages in the case
that they temporarily drop their connection to the broker and
reconnect at a later time.  The JMS broker will uniquely identify
subscriber clients with a combination of the client ID, username and
password to uniquely identify clients and manage message queues for
each client.

Now we need to create the subscriber client.  We're going to write a
standalone client to show that your code doesn't have to live in the
application server to receive messages.  The only trick we're going to
apply here is that while we can simple create an InitialContext with
an empty constructor for code in the app server, code that exists
outside of the appliaction server must know where to find the JNDI
naming service.  Glassfish exposes the naming service via CORBA - the
Common Object Request Broker Architechture.. In short - we need to
know a factory class name to create the context and we need to know
the URL of where the object request broker is located. 

The following listener client can be run on the same host as the
Glassfish server ::

    """
    This is a standalone client that listens messages from JMS 
    """
    from javax.jms import TopicConnectionFactory, MessageListener, Session
    from javax.naming import InitialContext, Context
    import time

    def get_context():
        props = {}
        props[Context.INITIAL_CONTEXT_FACTORY]="com.sun.appserv.naming.S1ASCtxFactory"
        props[Context.PROVIDER_URL]="iiop://127.0.0.1:3700"
        context = InitialContext(props)
        return context

    class TopicListener(MessageListener):
        def go(self):
            context = get_context()
            tfactory = context.lookup("jms/MyConnectionFactory")
            tconnection = tfactory.createTopicConnection('recvuser', 'recvpass')
            tsession = tconnection.createTopicSession(False, Session.AUTO_ACKNOWLEDGE)
            subscriber = tsession.createDurableSubscriber(context.lookup("jms/MyTopic"), 'mysub')
            subscriber.setMessageListener(self)
            tconnection.start()
            while True:
                time.sleep(1)
            context.close()
            tconnection.close()

        def onMessage(self, message):
            print message.getText()

    if __name__ == '__main__':
        TopicListener().go()

There are only a few key differences between the subscriber and
publisher side of a JMS topic.  First, the subscriber is created with
a unique client id - in this case - it's 'mysub'.  This is used by JMS
to determine what pending messages to send to the client in the case
that the client drops the JMS connections and rebinds at a later time.
If we don't care to receive missed messages, we could have created a
non-durable subscriber with "createSubscriber" instead of
"createDurableSubscriber" and we would not have to pass in a client
ID.

Second, the listener employs a callback pattern for incoming messages.
When a message is received, the onMessage will be called automatically
by the subscriber object and the message object will be passed in.

Now we need to create our sending user and receiving user on the
broker.  Drop to the command line and go to GLASSFISH_HOME/imq/bin.
We are going to create two users - one sender and one receiver. ::

  GLASSFISH_HOME/imq/bin $ imqusermgr add -u senduser -p sendpass
  User repository for broker instance: imqbroker
  User senduser successfully added.

  GLASSFISH_HOME/imq/bin $ imqusermgr add -u recvuser -p recvpass
  User repository for broker instance: imqbroker
  User recvuser successfully added.

We now have two new users with username/pasword pairs of
senduser/sendpass and recvuser/recvpass.

You have enough code now to enable publish/subscribe messaging
patterns in your code to signal applications that live outside of your
application server.  We can potentially have multiple listeners
attached to the JMS broker and JMS will make sure that all subscribers
get messages in a reliable way.

Let's take a look now at sending message through a queue - this
provides reliable point to point messaging and it adds guarantees that
messages are persisted in a safe manner to safeguard against server
crashes.   This time, we'll build our send and receive clients as
individual standalone clients that communicate with the JMS broker. ::

    from javax.jms import Session
    from javax.naming import InitialContext, Context
    import time

    def get_context():
        props = {}
        props[Context.INITIAL_CONTEXT_FACTORY]="com.sun.appserv.naming.S1ASCtxFactory"
        props[Context.PROVIDER_URL]="iiop://127.0.0.1:3700"
        context = InitialContext(props)
        return context

    def send():
        context = get_context()
        qfactory = context.lookup("jms/MyConnectionFactory")
        # This assumes a user has been provisioned on the broker with
        # username/password of 'senduser/sendpass'
        qconnection = qfactory.createQueueConnection('senduser', 'sendpass')
        qsession = qconnection.createQueueSession(False, Session.AUTO_ACKNOWLEDGE)
        qsender = qsession.createSender(context.lookup("jms/MyQueue"))
        msg = qsession.createTextMessage()
        for i in range(20):
            msg.setText('this is msg [%d]' % i)
            qsender.send(msg)

    def recv():
        context = get_context()
        qfactory = context.lookup("jms/MyConnectionFactory")
        # This assumes a user has been provisioned on the broker with
        # username/password of 'recvuser/recvpass'
        qconnection = qfactory.createQueueConnection('recvuser', 'recvpass')
        qsession = qconnection.createQueueSession(False, Session.AUTO_ACKNOWLEDGE)
        qreceiver = qsession.createReceiver(context.lookup("jms/MyQueue"))
        qconnection.start()  # start the receiver

        print "Starting to receive messages now:"
        while True:
            msg = qreceiver.receive(1)
            if msg <> None and isinstance(msg, TextMessage):
                print msg.getText()


The send() and recv() functions are almost identical to the
publish/subscriber code used to manage topics.  A minor difference is
that the JMS queue APIs don't use a callback object for message
receipt.  It is assumed that client applications will actively
dequeue objects from the JMS queue instead of acting as a passive
subscriber.

The beauty of this JMS code is that you can send messages to the
broker and be assured that even in case the server goes down, your
messages are not lost.  When the server comes back up and your
endpoint client reconnects - it will still receive all of it's pending
messages.

We can extend this example even further.  Codehaus.org has a messaing
project called STOMP - the Streaming Text Orientated Messaging
Protocol.  STOMP is simpler, but less performant than raw JMS
messages, but the tradeoff is that clients exist in a dozen different
languages.  STOMP also provides an adapter called 'stomp-connect'
which allows us to turn a JMS broker into a STOMP messaging broker.

This will enable us to have applications written in just about *any*
language communicate with our applications over JMS.  There are times
when I have existing CPython code that leverages various C libraries
like Imagemagick or NumPy to do computations that are simply not
supported with Jython or Java.  

By using stompconnect, I can send work messages over JMS, bridge those
messages over STOMP and have CPython clients process my requests.  The
completed work is then sent back over STOMP, bridged to JMS and
received by my Jython code.

First, you'll need to obtain latest version of stomp-connect from
codehaus.org. Download stompconnect-1.0.zip from here :

    http://stomp.codehaus.org/Download

After you've unpacked the zip file, you'll need to configure a JNDI
property file so that STOMP can act as a JMS client.  The
configuration is identical to our Jython client.  Create a file called
"jndi.properties" and place it in your stompconnect directory. The
contents should have the two following lines ::

    java.naming.factory.initial=com.sun.appserv.naming.S1ASCtxFactory
    java.naming.provider.url=iiop://127.0.0.1:3700

You now need to pull in some JAR files from Glassfish to gain access
to JNDI, JMS and some logging classes that STOMP requires. Copy the
following JAR files from GLASSFISH_HOME/lib into 
STOMPCONNECT_HOME/lib :

 * appserv-admin.jar
 * appserv-deployment-client.jar
 * appserv-ext.jar
 * appserv-rt.jar
 * j2ee.jar
 * javaee.jar

Copy the imqjmsra.jar file from GLASSFISH_HOME/imq/lib/imqjmsra.jar to
STOMPCONNECT_HOME/lib.

You should be able to now start the connector with the following
command line ::

    java -cp "lib\*;stompconnect-1.0.jar" \
        org.codehaus.stomp.jms.Main tcp://0.0.0.0:6666 \
        "jms/MyConnectionFactory"

If it works, you should see a bunch of output that ends with a message
that the server is listening for connection on tcp://0.0.0.0:6666.
Congratulations, you now have a STOMP broker acting as a bidirectional
proxy for the OpenMQ JMS broker.

Receiving messages in CPython that orginate from Jython+JMS is as
simple as the following code. ::

    import stomp
    serv = stomp.Stomp('localhost', 6666)
    serv.connect({'client-id': 'reader_client', \
                      'login': 'recvuser', \
                   'passcode': 'recvpass'})
    serv.subscribe({'destination': '/queue/MyQueue', 'ack': 'client'})
    frame = self.serv.receive_frame()
    if frame.command == 'MESSAGE':
        # The message content will arrive in the STOMP frame's
        # body section
        print frame.body
        serv.ack(frame)

Sending messages is just as straight forward. From our CPython ocde,
we just need to import the stomp client and we can send messages back
to our Jython code.  ::

    import stomp
    serv = stomp.Stomp('localhost', 6666)
    serv.connect({'client-id': 'sending_client', \
                      'login': 'senduser', \
                   'passcode': 'sendpass'})
    serv.send({'destination': '/queue/MyQueue', 'body': 'Hello world!'})

Conclusion
----------

We've covered a lot of ground here.  I've shown you how to get Django
on Jython to use database connection pooling to enforce limits on the
database resources an application can consume.  We've looked at
setting up JMS queues and topic to provide both point to point and
publish/subscribe messages between Jython processes.  We then took
those messaging services and provided interoperability between
Jython code and non-Java code.

In my experience, the ability to remix a hand picked collection of
technologies is what gives Jython so much power.  You can use both the
technology in JavaEE, leverging years of hard won experience and get
the benefit of using a lighter weight, more modern web application
stack like Django.
