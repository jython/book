Introduction to Pylons

While Django is currently the most popular webframework for Python, it
is by no means your only choice.  Where Django grew out of the needs
of newsrooms to implement content management solutions rapidly -
Pylons grew out of a need to build web applications in environments
that may have existing databases to integrate with and the
applications don't fit into the a nice

Pylons greatest strength is that it takes a best of breed approach to
constructing it's technology stack.  Where everything is 'built in'
with Django - Pylons assembles carefully selected libraries together
and wires them together into a full webstack.

Ultimately picking Django or Pylons is about deciding which tradeoffs
you're willing to make.  While Django is extremly easy to learn
because all the documentation is in one place and all the
documentation relating to any particular component is always discussed
in the context of building a web application - you lose some
flexibility when you need to start doing things that are at the
margins of what most web developers do. 

For example, in a project I've worked on recently, I needed to
interact with a nontrivial database that was implemented in SQL Server
2000.  For Django, implementing the SQL Server backend was quite
difficult.  There aren't that many web developers using Django on
Windows, never mind SQL Server.  The Django ORM is a part of Django,
but it's obviously not the core focus of Django so building a working
SQL Server backend meant I had to read code in the ODBC implmentation,
parts of the ADODBAPI implementation and the psycopg2 implementation
of the database backends.  

This was fairly painful and took weeks of work - but again - can you
really blame a webframework for not supporting a 10 year old database
on a platform that nobody runs webservers on?  That's a bit unfair.

Pylons on the other hand leverages SQLAlchemy.  SQLAlchemy is probably
the most powerful database toolkit available in Python.  It *only*
focuses on database access.  The SQL Server backend was already built
in a robust way for CPython and implementing the extra code for a
Jython backend took 2 days - and this was from not seeing any of the
code in SQLAlchemy's internals.

That experience alone sold me on Pylons.  I don't have to rely the
'webframework' people to experts in databases.  Similarily, I don't
have to rely on the database experts to know anything about web
templating.

In short when you have to deal with the weird stuff - Pylons makes a
fabulous choice - and lets be honest - there's almost always weird
stuff you're going to have to do.

    * Convention over Configuration
    * Sensible defaults
    * Flexibilty to pick components that you need

A guide for the impatient
=========================

The best way to install Pylons is inside of a virtualenv.  Create a new virtualenv for Jython 
and run easy_install ::

    > easy_install "Pylons==0.9.7"

Create your application ::

    > paster create --template=pylons RosterTool

    # TODO: just use the defaults for everything.

Launch the development server ::

    > paster serve --reload development.ini

Open a browser and connect to http://127.0.0.1:5000/

    # TODO: include screenshot here

Drop a static file into rostertool/public/welcome.html ::

    <html>
        <body>Just a static file</body>
    </html>

You should now be able to load the static content by going to ::

    http://localhost:5000/welcome.html

Add a controller ::

    RosterTool/roster > paster controller roster

Paste will install a directory named "controllers" and install some
files in there including a module named "roster.py".  You can open it
up and you'll see a class named "RosterController" and it will have a
single method "index".  Pylons is smart enough to automatically map a
URL to a controller classname and invoke a method.  To invoke the
RosterController's index method, you just need to invoke ::

    http://localhost:5000/roster/index

Congratulations, you've got your most basic possible web application running
now.  It handles basic HTTP GET requests and calls a method on a controller and
a response comes out.  Lets cover each of these pieces in detail now.

A note about Paste
------------------
    
While you setup your toy Pylons application, you probably wondered
why Pylons seems to use a command line tool called "paster" instead of
something obvious like "pylons".  Paster is actually a part of the
Paste set of tools that Pylons uses.

Paste is used to build web application frameworks - not web
applications - but web application frameworks like Pylons.  Everytime
you use "paster", that's Paste being called.  Everytime you access the
HTTTP request and response objects - that's WebOb - a descendant of
Paste's HTTP wrapper code.  Pylons uses Paste extensively for
configuration management, testing, basic HTTP handling with WebOb.
You would do well to at least skim over the Paste documentation to see
what is available in paste.  

Pylons MVC
----------

Pylons, like Django any any reasonably sane webframework (or GUI
toolkit for that matter) uses the model-view-controller design
pattern.  

In Pylons this maps to:

===========  =========================================================================================  
Component    Implementation
===========  =========================================================================================
Model        SQLAlchemy (or any other database toolkit you prefer)
View         Mako (or any templating language you prefer)
Controller   Python
===========  =========================================================================================

To reiterate - Pylons is about letting you - the application developer
decide on the particular tradeoffs you're willing to make.  If using a
templating language more similar to Django is better for your web
designers, then switch go Jinja2.  If you don't really want to deal
with SQLAlchemy - you can use SQLObject or raw SQL if you prefer.

Pylons provides some plumbing to let you hook these pieces together
using Routes and webhelpers.

Routes is a library SQLAlchemy uses to define how URLs will be mapped
to invocations of methods on particular controller classes.
Webhelpers are a bundle of functions that web develeopers usually need
on any site - these can help you setup the templates that Pylons will
use as the views for your appliation.

Pylons also provides infrastructure so that you can manipulate things
that are particular to web applications including:

  * WSGI middleware to add functionality to your application with
    minimal intrusion into your existing codebase.
  * A robust testing framework including a shockingly good debugger
    you can use through the web. 
  * Helpers to enable REST-ful API development so you can expose your
    application as a programmatic interface.

Now let's wrap up the hockey roster up in a web application.  We'll
target a couple features:

 * form handling and validation to add new players through the web
 * login and authentication to make sure not anybody can edit our
   lists
 * add a JSON/REST api so that we can modify data from other tools

In the process, we'll use the interactive debugger from both command
line and through the web to directly observe and interact with the
state of the running application.


An interlude into Java's memory model
-------------------------------------

A note about reloading - sometimes if you're doing devleopment with
Pylons on Jython, Java will through an OutOfMemory error like this ::

    java.lang.OutOfMemoryError: PermGen space
            at java.lang.ClassLoader.defineClass1(Native Method)
            at java.lang.ClassLoader.defineClass(ClassLoader.java:620)

Java keeps track of class definitions in something called the Permanent
Generation heap space.  This is a problem for Pylons when the HTTP threads are
restarted and your classes are reloaded.  The old class definitions don't go
away.  In fact, you can think of Jython as a Java class generator.  So each
time your develpment server restarts - you're gettings hundreds of new versions
of your classes loaded *for the first time* since classes are never updated.

If you're really interestd in bumping up the permgen size, you can use
-XX:MaxPermSize=128M - or use another heap size setting to increase the generation's size.

You can edit your Jython startup script in JYTHON_HOME/bin/jython (or
jython.bat) by editting the line that reads ::

    set _JAVA_OPTS=

to be ::

    set _JAVA_OPTS=-XX:MaxPermSize=128M

This shouldn't be a problem in production environments where you're
not generating new class definitions during runtime, but it can be
quite annoying during development.

Invoking the Pylons shell
-------------------------

# cribbed from - Chapter 12: Testing

Yes, I'm going to start with testing right away because it will
provide you with a way to explore the Pylons application in an
interactive way.

Pylons gives you an interactive shell much like Django's. You can
start it up with the following commands. ::

    RosterTool > jython setup.py egg_info
    RosterTool > paster shell test.ini

This will yield a nice interactive shell you can start playing with
right away.  Now lets take a look at those request and response
objects in our toy application. ::

    RosterTool > paster shell test.ini

    Pylons Interactive Shell
    Jython 2.5.0 (Release_2_5_0:6476, Jun 16 2009, 13:33:26) 
    [OpenJDK Server VM (Sun Microsystems Inc.)]

    All objects from rostertool.lib.base are available
    Additional Objects:
    mapper     -  Routes mapper object
    wsgiapp    -  This project's WSGI App instance
    app        -  paste.fixture wrapped around wsgiapp

    >>> resp = app.get('/roster/index')
    >>> resp
    <Response 200 OK 'Hello World'>
    >>> resp.req
    <Request at 0x43 GET http://localhost/roster/index>

Pylons lets you actually run requests against the application and
play with the resulting response.  Even for something as 'simple' as
the HTTP request and response,, Pylons uses a library to provide
convenience methods and attributes to make your development life
easier.  In this case - it's WebOb - a derivative of Paste's older
HTTP wrapper code.

The request and the response objects both have literally dozens of
attributes and methods that are provided by the framework.  You'
almost certainly going to benefit if you take time to browse through
WebOb's documentation [1]_.

Here's four attributes you really have to know to make sense of the
request object.  The best thing to do is to try playing with the
request object in the shell.

request.GET
    GET is a special dictionary of the variables that were passed in
    the URL.  Pylons automatically converts URL arguments that appear
    multiple times into discrete key value pairs.

    >>> resp = app.get('/roster/index?foo=bar&x=42&x=50')
    >>> resp.req.GET
    UnicodeMultiDict([('foo', u'bar'), ('x', u'42'), ('x', u'50')])
    >>> req.GET['x']
    u'50'
    >>> req.GET.getall('x')
    [u'42', u'50']

Note how you can get either the last value or the list of values
depending on how you choose to fetch values from the dictionary.  This
can cause subtle bugs if you're not paying attention.

request.POST 
    POST does the same thing, but it includes only the variables that
    were sent up during HTML form submission.

request.params 
    Pylons merges all the GET and POST data into a single
    MultiValueDict.  In almost all cases, this is the one attribute
    that you really want to use to get the data that the user sent to
    the server.

request.headers 
    This dictionary provides all the HTTP headers that the client sent
    to the server.


Context Variables and Application Globals
-----------------------------------------

Most webframeworks provide a request scoped variable to act as a bag
of values. Pylons is no exception - whenever you create a new
controller with paste - it will automatically import an attribute 'c'
which is the context variable.  Note that this is a special variable
that will be available to the entire request, and that *paste* is
importing the variable for you.  The 'c' value is *not* an attribute
of your controller - Pylons has special global threadsafe variables
 - this is just one of them.

Application Globals are literally global variables available to all threads.
You should be careful about using something like this in the context of running
your application in an application server.  Your system administrator may
decide that your application will be redeployed in a multiserver configuration
and your shared state won't be quite so shared.

Routes
------

Routes is much like Django's URL dispatcher.  It provides a mechanism
for you to map URLs to controllers classes and methods to invoke.

Generally, I find that Routes makes a tradeoff of less URL matching
expressiveness in exchange for simpler reasoning about which URLs are
directed to a particular controller and method.  Routes doesn't
support regular expressions, just simple variable substitution.

A typical route will look something like this ::

    map.connect('/{mycontroller}/{someaction}/{var1}/{var2}')

The above route would find the controller called "Mycontroller" (note
the casing of the class) and invoke the "someaction" method on that
object.  Variables var1 and var2 woulld be passed in as arguments.

The connect() method of the map object will also take in optional
arguments to fill in default values for URLs that do not have enough
URL encoded data in them to properly invoke a method with the minimum
required number of arguments. The front page is an example of this -
let's try connecting the frontpage to the Roster.index method.

Edit rostertool/config/routing.py so that there are 3 lines after
#CUSTOM_ROUTES_HERE that should read something like this ::

    map.connect('/', controller='roster', action='index')
    map.connect('/{action}/{id}/', controller='roster')
    map.connect('/add_player/', controller='roster', action='add_player')

While this *looks* like it should work, you can try running "paster
serve", it won't.

Pylons always tries to serve static content before searching for
controllers and methods to invoke.  You'll need to go to
RosterTool/rostertool/public and delete the 'index.html' file that
paster installed when you first created your application.

Load http://localhost:5000/ again in your browser - the default
index.html should be gone and you should now get your welcome page.

Controllers and Templates
-------------------------

Leveraging off of the Table model we defined in chapter 12, let's
create the hockey roster, but this time using the postgresql database.
I'll assume that you have a postgresql installation running that
allows you create new databases. ::

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.schema import Sequence
    >>> db = create_engine('postgresql+zxjdbc://myuser:mypass@localhost:5432/mydb')
    >>> connection = db.connect()
    >>> metadata = MetaData()
    >>> player = Table('player', metadata,
    ...     Column('id', Integer, primary_key=True),
    ...     Column('first', String(50)),
    ...     Column('last', String(50)),
    ...     Column('position', String(30)))
    >>> metadata.create_all(engine)

Now let's wire the data up to the controllers, display some data and
get basic form handling working.  We're going to create a basic CRUD
(create, read, update, delete) inteface to the sqlalchemy model.
Because of space constraints, this HTML is going to be very basic, but
you'll get a taste of how things fit together.

Paste doesn't justs generate a stub for your controller - it will also
code generate an empty functional test case in
rostertool/tests/functional/ as test_roster.py.  We'll visit testing
shortly.

Controllers are really where the action occurs in Pylons.  This is
where your application will take data from the database and prepare it
for a template to render it as HTML.  Let's put the list of all
players on the front page of the site.  We'll implement a template to
render the list of all players.  Then, we'll implement a method in the
controller to override the index() method of Roster to use SQLAlchemy
to load the records from disk and send them to the template.

Along the way, we'll touch on template inheritance so that you can see
how you can save keystrokes by subclassing your templates in Mako.

First, let's create two templates, base.html and list_players.html in
the rostertool/templates directory.

base.html ::

    <html>
        <body>
            <div class="header">
                ${self.header()}
            </div>

            ${self.body()}
        </body>
    </html>

    <%def name="header()">
        <h1>${c.page_title}</h1>
        <% messages = h.flash.pop_messages() %>
        % if messages:
        <ul id="flash-messages">
            % for message in messages:
            <li>${message}</li>
            % endfor
        </ul>
        % endif
    </%def>

list_players.html ::

    <%inherit file="base.html" />
    <table border="1">
        <tr>
            <th>Position</th><th>Last name</th><th>First name</th><th>Edit</th>
        </tr>
        % for player in c.players:
            ${makerow(player)}
        % endfor
    </table>

    <h2>Add a new player</h2>
    ${h.form(h.url_for(controller='roster', action='add_player'), method='POST')} 
        ${h.text('first', 'First Name')} <br />
        ${h.text('last', 'Last Name')} <br />
        ${h.text('position', 'Position')} <br />
        ${h.submit('add_player', "Add Player")}
    ${h.end_form()}

    <%def name="makerow(row)">
    <tr>
        <td>${row.position}</td>\
        <td>${row.last}</td>\
        <td>${row.first}</td>\
        <td><a href="${h.url_for(controller='roster', action='edit_player', id=row.id)}">Edit</a></td>\
    </tr>
    </%def>


There's quite a bit going on here. The base template lets Mako define
a boilerplate set of HTML that all pages can reuse.  Each section is
defined with a <%def name="block()"> section and the blocks are
overloaded in the subclassed templates.  In effect - Mako lets your
page templates look like objects with methods that can render
subsections of your pages.

The list_players.html template has content that is immediately
substituted into the self.body() method of the base template. The
first part of our body uses our magic context variable 'c'. Here -
we're iterating over each of the players in the database and rendering
them into a table as a row.  Note here that we can use the Mako method
syntax to create a method called 'makerow' and invoke it directly
within our template.

    #XX: Aside for Mako
    Mako provides a rich set of functions for templating.  I'm only going
    ot use the most basic parts of Mako - inheritance, variable
    substitution and loop iteration to get the toy application working.  I
    strongly suggest you dive into the Mako documentation to discover
    features and get a better understanding of how to use the template
    library.
    ## 

Next, we add in a small form to create new players.  The trick here is
to see that the form is being generated programmatically by
helper functions.  Pylons automatically imports
YOURPROJECT/lib/helpers (in our case - rostertool.lib.helpers) as the
'h' variable in your template.  The helpers module typically imports
functions frmo parts of Pylons or a dependant library to allow access
to those features from anywhere in the application.  Although this
seems like a violation of 'separation of concerns' - look at the
template and see what it buys us?  We get fully decoupled URLs from
the particular controller and method that need to be invoked.  The
template uses a special routes function "url_for" to compute the URL
that would have been mapped for a particular controller and method.
The last part of our list_players.html file contains code to display
alert messages.  

Let's take a look at our rostertool.lib.helpers module now ::

    from routes import url_for
    from webhelpers.html.tags import *
    from webhelpers.pylonslib import Flash as _Flash

    # Send alert messages back to the user
    flash = _Flash()

Here, we're importing the url_for function from routes to do our URL
reversal computations.  We import HTML tag generators from the main
html.tags helper modules and we import Flash to provide alert messages
for our pages.  I'll show you how flash messages are used when we
cover the controller code in more detail in the next couple of pages.

Now, create a controller with paste (you've already done this if you
were impatient at the beginning of the chapter) ::

    $ cd ROSTERTOOL/rostertool
    $ paster controller roster

RosterContoller should get a method very short method that reads ::

    def index(self):
        session = Session()
        c.page_title = 'Player List'
        c.players = session.query(Player).all()
        return render('list_players.html')

This code is fairly straight forward, we are simply using a SQLAlchemy
session to load all the Player objects from disk and assigning to the
special context variable 'c'.  Pylons is then instructed to render the
list_player.html file.  Let's take a look at that file now:

The context should be your default place to place values you want to
pass to other parts of the application.  Note that Pylons will
automatically bind in URL values to the context so while you can grab
the form values from self.form_result, you can also grab raw URL
values from the context.

You should be able run the debug webserver now and you can get to the
front page to load an empty list of players.   Start up your debug
webserver as you did at the beginning of this chapter and go to
http://localhost:5000/ to se the page load with your list of players
(currently an empty list).

Now we need to get to the meaty part where we can start create, edit
and delete players. We'll make sure that the inputs are at least
minimally validated, errors are displayed to the user and that alert
messages are properly populated.

First, we need a page that shows just a single player and provides
buttons for edit and delete. ::

    <%inherit file="base.html" />

    <h2>Edit player</h2>
    ${h.form(h.url_for(controller='roster', action='save_player', id=c.player.id), method='POST')} 
        ${h.hidden('id', c.player.id)} <br />
        ${h.text('first', c.player.first)} <br />
        ${h.text('last', c.player.last)} <br />
        ${h.text('position', c.player.position)} <br />
        ${h.submit('save_player', "Save Player")}
    ${h.end_form()}

    ${h.form(h.url_for(controller='roster', action='delete_player', id=c.player.id), method='POST')} 
        ${h.hidden('id', c.player.id)} <br />
        ${h.hidden('first', c.player.first)} <br />
        ${h.hidden('last', c.player.last)} <br />
        ${h.hidden('position', c.player.position)} <br />
        ${h.submit('delete_player', "Delete Player")}
    ${h.end_form()}

This template assumes that there is a 'player' value assigned to the
context and not suprisingly - it's going to be a full blown instance
of the Player object that we first saw in chapter 12.  The helper
functions let us define our HTML form using simple functions.  This
means you won't have to worry about escaping characters or remember
the particular details of the HTML attributes.  The helper.tag
functions will do sensible things by default.

I've setup the edit and delete forms to point to different URLs.  You
might want to 'conserve' URLs but having discrete URLs for each action
has advantages - especially for debugging.  You can trivially view
which URLs are being hit on a webserver by reading log files.  Seeing
the same kind of behavior if the URLs are the same, but the behavior
is dictated by some form value - well that's a whole lot harder to
debug.  It's also a lot harder to setup in your controllers because
you need to dispatch the behavior on a per method level.  Why not just
have separate methods for separate behaviour - everybody will thank
you for it when they need to debug your code in the future.

Before we create our controller methods for create, edit and delete -
we'll create a formencode schema to provide basic validation.  Again -
Pylons doesn't provide validation behaviour - it just leverages
another library to do so.  In rostertool/controllers/roster.py ::

    class PlayerForm(formencode.Schema):
        # You need the next line to drop the submit button values
        allow_extra_fields=True

        first = formencode.validators.String(not_empty=True)
        last = formencode.validators.String(not_empty=True)
        position = formencode.validators.String(not_empty=True)

This simply provides basic string verification on our inputs. Note how
this doesn't provide any hint as to what the HTML form looks like - or
that it's HTML at all. FormEncode can validate arbitrary Python
dictionaries and return errors about them.

I'm just going to show you the add method, and the edit_player
methods.  You should try to implement the save_player and
delete_player methods to make sure you understand what's going on
here. ::

    from pylons.decorators import validate
    from rostertool.model import Session, Player

    @validate(schema=PlayerForm(), form='index', post_only=False, on_get=True)
    def add_player(self):
        first = self.form_result['first']
        last = self.form_result['last']
        position = self.form_result['position']
        session = Session()
        if session.query(Player).filter_by(first=first, last=last).count() > 0:
            h.flash("Player already exists!")
            return h.redirect_to(controller='roster')
        player = Player(first, last, position)
        session.add(player)
        session.commit()
        return h.redirect_to(controller='roster', action='index')

    def edit_player(self, id):
        session = Session()
        player = session.query(Player).filter_by(id=id).one()
        c.player = player
        return render('edit_player.html')

A couple of notes here.  edit_player is passed in the 'id' attribute
directly by Routes.  In the edit_player method - 'player' is assigned
to the context, but the context is never explicitly passed into the
template renderer. Pylons is going to automatically take the
attributes bound to the context and write them into template and
render the HTML output.

With the add_player method, I'm using the validate decorator to
enforce the inputs against the PlayerForm. In the case of error, the
form attribute of the decorator is used to load an action against the
current controller. In this case - 'index' - so the front page loads.

The SQLAlchemy code should be familiar to you if you have already gone
through chapter 12.  The lsat line of the add_player method is a
redirect to prevent problems with hitting reload in the browser.  Once
all data manipulation has occured - the server redirects the client to
a results page.  In the case that a user hits reload on the result
page - no data will be mutated.

Here's the signatures of the remaining methods you'll need to
implement to make things work:

 * save_player(self):
 * delete_player(self):

If you get stuck, you can always consult the working sample code on
the book website.

Adding in a JSON API
--------------------

JSON integration into Pylons is very straight forward.  The steps are
roughly the same as adding controller methods for plain HTML views.
You invoke paste, paste then generates your controller stubs and test
stubs, you add in some routes to wire controllers to URLs and then you
just fill in the controller code. ::

    $ cd ROSTERTOOL_HOME/rostertool
    $ paster controller api

Pylons provides a special @jsonify decorator which will automatically
convert Python primitive types into JSON objects.  It will *not*
convert the POST data into an object though - that's your
responsibility. Adding a simple read interface into the player list
requires only adding a single method to your ApiController ::

    @jsonify
    def players(self):
        session = Session()
        players = [{'first': p.first, 
                    'last': p.last, 
                    'position': p.position, 
                    'id': p.id} for p in session.query(Player).all()]
        return players

adding a hook so that people can POST data to your server in JSON
format to create new player is almost as easy ::

    import simplejson as json

    @jsonify
    def add_player(self):
        obj = json.loads(request.body)
        schema = PlayerForm()
        try:
            form_result = schema.to_python(obj)
        except formencode.Invalid, error:
            response.content_type = 'text/plain'
            return 'Invalid: '+unicode(error)
        else:
            session = Session()
            first, last, position = obj['first'], obj['last'], obj['position']
            if session.query(Player).filter_by(last=last, first=first,
                    position=position).count() == 0:
                session.add(Player(first, last, position))
                session.commit()
                return {'result': 'OK'}
            else:
                return {'result':'fail', 'msg': 'Player already exists'}

Unit testing, Functional Testing and Logging
--------------------------------------------

## Regular nosetests testscases, and using the TestController object to
make sure our URLs are behaving in the way that we expect.

XXX: Show how Pylon's logger supports chainsaw for people
coming from the log4j world.

Deployment into a servlet container
-----------------------------------

# TODO: copy screenshots from work...
# Installing snakefight
# Using bdist_war
# use snakefight to deploy the application into Glassfish v2.1

Conclusion
----------

We've only scratched the surface of what's possible with Pylons, but I
hope you've gotten a taste of whats available.

The paste configuration files have an enormous number of configurable
options.'

FormEncode supports *much* more advanced form validation techniques
than I've shown, but I hope you can see how easy it is to just get
started with the most basic validation routines.


