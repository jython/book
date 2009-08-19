Chapter 12- Databases and Jython: Object Relational Mapping and Using JDBC
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



Finally we will look at zxJDBC package, which is a standard part of
Jython since version 2.1 and complies with the Python 2.0 DBI
standard. zxJDBC can be an appropriate choice for simple one-off
scripts where database portabibility is not a concern. In addition,
it's (generally) necessary to use zxJDBC when writing a new dialect
for SQLAlchemy or Django. [But not strictly true: you can use pg8000,
a pure Python DBI driver, and of course write your own DBI
drivers. But please don't do that.] So knowing how zxJDBC works can
useful when working with these packages. However, it's too low level
for us to recommend for more general usage. Use SQLAlchemy or Django
if at all possible.

Finally, JDBC itself is also directly accessible, like any other Java
package from Jython. Simply use the java.sql package. In practice this
should be rarely necessary. [XXX But perhaps something about how we
can still look at the underlying JDBC connection and result sets, if
necessary?  and if so, how?] [XXX there was also an article on doing
this on IBM developer works if I'm not mistaken]


zxJDBC – Using Python’s DB API via JDBC
=======================================

Introduction to zxJDBC
----------------------

The zxJDBC package provides an easy-to-use Python wrapper around
JDBC. zxJDBC bridges two standards:

 * JDBC is the standard platform for database access in Java.
 * DBI is the standard database API for Python apps.

zxJDBC, part of Jython, provides a DBI 2.0 standard compliant
interface to JDBC. Over 200 drivers are available for JDBC [XXX
http://developers.sun.com/product/jdbc/drivers], and they all work
with zxJDBC. High performance drivers are available for all major
relational databases, including DB2, Derby, MySQL, Oracle, PostgreSQL,
SQLite, SQLServer, and Sybase. And drivers are also available for
non-relational and specialized databases too.

However, unlike JDBC, zxJDBC when used in the simplest way possible,
blocks SQL injection attacks, minimizes overhead, and avoids resource
exhaustion. In addition, zxJDBC defaults to using a transactional
model (when available), instead of autocommit.

First we will look at connections and cursors, which are the key
resources in working with zxJDBC, just like any other DBI
package. Then we will look at what you can do them with them, in terms
of typical queries and data manipulating transactions.


Getting Started
---------------

drivers and such

Connections
-----------



Cursors
-------


Resource Management
-------------------

Creating and Executing Queries
------------------------------

Retrieving Data
---------------

Iteration
---------


Object Relational Mapping
=========================

While zxJDBC certainly offers a viable option for database access via Jython, there are many other solutions available.  Many developers today are choosing to use ORM (Object Relational Mapping) solutions to work with the database.  This section is not an introduction to ORM, we assume that you are at least a bit familiar with the topic.  Furthermore, the ORM solutions that are about to be discussed have an enormous amount of very good documentation already available either on the web or in book format.  Therefore, this section will give insight on how to use these technologies with Jython, but it will not go into great detail on how each ORM solution works.  With that said, there is no doubt in stating that these solutions are all very powerful and capable for standalone and enterprise applications alike.



In the next couple of sections, we’ll cover how to use some of the most popular ORM solutions available today with Jython.  You’ll learn how to set up your environment and how to code Jython to work with each ORM.  By the end of this chapter, you should have enough knowledge to begin working with these ORMs using Jython, and even start building Jython ORM applications.

SqlAlchemy
----------

No doubt about it, SqlAlchemy is one of the most widely known and used ORM solutions for the Python programming language.  It has been around long enough that its maturity and stability make it a great contender for use in your applications.  It is simple to setup, and easy-to-use for both new databases and legacy databases alike.  You can seriously download and install SqlAlchemy and begin using it in a very short amount of time.  The syntax for using this solution is very straight forward, and as with other ORM technologies, working with database entities occurs via the use of a mapper that links a special Jython class to a particular table in the database.  The overall result is that the application is persisted through the use of entity classes as opposed to database SQL transactions.



In this section we will cover the installation and configuration of SqlAlhemy with Jython.  It will then show you how to get started using it through a few short examples, we will not get into great detail as there are plenty of excellent references on SqlAlchemy already.  However, this section should fill in the gaps for making use of this great solution on Jython.



Installation
~~~~~~~~~~~~

We’ll begin by downloading SqlAlchemy from the website (http://www.sqlalchemy.org), at the time of this writing the version that should be used is 0.6.  This version has been installed and tested with the Jython 2.5.0 release.  Once you’ve downloaded the package, unzip it to a directory on your workstation and then traverse to that directory in your terminal or command prompt.  Once you are inside of your SqlAlchemy directory, issue the following command to install: ::



	jython setup.py install


Once you’ve completed this process, SqlAlchemy should be successfully installed into your jython Lib\site-packages directory.  You can now access the SqlAlchemy modules from jython, and you can open up your terminal and check to ensure that the install was a success by importing sqlalchemy and checking the version. ::



	>>> import sqlalchemy
	>>> sqlalchemy.__version__
	'0.6beta1'
	>>> 


After we’ve ensured that the installation was a success, it is time to begin working with SqlAlchemy via the terminal.  However, we have one step left before we can begin.  Jython uses zxJDBC to implement the Python database API in Java.  The end result is that most of the dialects that are available for use with SqlAlchemy will not work with Jython out of the box.  This is because the dialects need to be re-written to implement zxJDBC.  At the time of this writing, I could only find one completed dialect, zxoracle, that was rewritten to use zxJDBC, and I’ll be showing you some examples based upon zxoracle in the next sections.  However, other dialects are in the works including SQLServer and MySQL.  The bad news is that SqlAlchemy will not yet work with every database available, on the other hand, Oracle is a very good start and implementing a new dialect is not very difficult.  You can find the zxoracle.py dialect included in the source for this book.  Browse through it and you will find that it may not be too difficult to implement a similar dialect for the database of your choice.  You can either place zxoracle somewhere on your Jython path, or place it into the Lib directory in your Jython installation. 

Lastly, we will need to ensure that our database JDBC driver is somewhere on our path so that Jython can access it.  Once you’ve performed the procedures included in this section, start up jython and practice some basic SqlAlchemy using the information from the next couple of sections.

Using SqlAlchemy
~~~~~~~~~~~~~~~~

We can work directly with SqlAlchemy via the terminal or command line.  There is a relatively basic set of steps you’ll need to follow in order to work with it.  First, import the necessary modules for the tasks you plan to perform.  Second, create an engine to use while accessing your database.  Third, create your database tables if you have not yet done so, and map them to Python classes using a SqlAlchemy mapper.  Lastly, begin to work with the database.



Now there are a couple of different ways to do things in this technology, just like any other.  For instance, you can either follow a very granular process for table creation, class creation, and mapping that involves separate steps for each, or you can use what is known as a declarative procedure and perform all of these tasks at the same time.  I will show you how to do each of these in this chapter, along with performing basic database activities using SqlAlchemy.  If you are new to SqlAlchemy, I suggest reading through this section and then going to sqlalchemy.org and reading through some of the large library of documentation available there.  However, if you’re already familiar with SqlAlchemy, you can move on if you wish because the rest of this section is a basic tutorial of the ORM solution itself.



Our first step is to create an engine that can be used with our database.  Once we’ve got an engine created then we can begin to perform database tasks making use of it.  Type the following lines of code in your terminal, replacing database specific information with the details of your development database. ::


	>>> import zxoracle
	>>> from sqlalchemy import create_engine
	>>> db = create_engine('zxoracle://schema:password@hostname:port/database)

Next, we’ll create the metadata that is necessary to create our database table using SqlAlchemy.  You can create one or more tables via metadata, and they are not actually created until after the metadata is applied to your database engine using a create_all() call on the metadata.  In this example, I am going to walk you through the creation of a table named Player that will be used in an application example in the next section. ::



	>>>player = Table('player', metadata,
	...     Column('id', Integer, primary_key=True),
	...     Column('first', String(50)),
	...     Column('last', String(50)),
	...     Column('position', String(30)))
	>>> metadata.create_all(engine)

Our table should now exist in the database and the next step is to create a Python class to use for accessing this table. ::



	class Player(object):
	    def __init__(self, first, last, position):
	        self.first = first
	        self.last = last
	        self.position = position

	    def __repr__(self):
	        return "<Player('%s', '%s', '%s')>" %(self.first, self.last, self.position)
::


The next step is to create a mapper to correlate the Player python object and the player database table.  To do this, we use the mapper() function to create a new Mapper object binding the class and table together.  The mapper function then stores the object away for future reference. ::



	>>> from sqlalchemy.orm import mapper
	>>> mapper(Player, player)
	<Mapper at 0x4; Player>

Creating the mapper is the last step in the process of setting up the environment to work with our table.  Now, let’s go back and take a quick look at performing all of these steps in an easier way.  If we want to create a table, class, and mapper all at once then we can do this declaratively.  Please note that with the Oracle dialect, we need to use a sequence to generate the auto-incremented id column for the table.  To do so, import the sqlalchemy.schema.Sequence object and pass it to the id column when creating.  You must ensure that you’ve manually created this sequence in your Oracle database or this will not work. ::



	SQL> create sequence id_seq
	  2  start with 1
	  3  increment by 1;

	Sequence created.

	# Delarative creation of the table, class, and mapper
	>>> from sqlalchemy.ext.declarative import declarative_base
	>>> from sqlalchemy.schema import Sequence
	>>> Base = declarative_base()
	>>> class Player(object):
	...     __tablename__ = 'player'
	...     id = Column(Integer, Sequence(‘id_seq’), primary_key=True)
	...     first = Column(String(50))
	...     last = Column(String(50))
	...     position = Column(String(30))
	...     def __init__(self, first, last, position):
	...         self.first = first
	...         self.last = last
	...         self.position = position
	...     def __repr__(self):
	...         return "<Player('%s','%s','%s')>" % (self.first, self.last, self.position)
	...
        
It is time to create a session and begin working with our database.  We must create a session class and bind it to our database engine that was defined with create_engine­ earlier.  Once created, the Session class will create new session object for our database.  The  Session class can also do other things that are out of scope for this section, but you can read more about them at sqlalchemy.org or other great references available on the web. ::



	>>> from sqlalchemy.orm import sessionmaker
	>>> Session = sessionmaker(bind=db)


We can start to create Player objects now and save them to our session.  The objects will be persisted in the database once they are needed, this is also known as a flush().  If we create the object in the session and then query for it, sqlalchemy will first persist the object to the database and then perform the query. ::

	#Import sqlalchemy module and zxoracle
	>>> import zxoracle
	>>> from sqlalchemy import create_engine
	>>> from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey
	>>> from sqlalchemy.schema import Sequence

	# Create engine
	>>> db = create_engine('zxoracle://schema:password@hostname:port/database’)

	# Create metadata and table
	>>> metadata = MetaData()
	>>> player = Table('player', metadata,
	...     Column('id', Integer, Sequence('id_seq'), primary_key=True),
	...     Column('first', String(50)),
	...     Column('last', String(50)),
	...     Column('position', String(30)))
	>>> metadata.create_all(db)

	# Create class to hold table object
	>>> class Player(object): 
	...     def __init__(self, first, last, position):                            
	...         self.first = first 
	...         self.last = last
	...         self.position = position
	...     def __repr__(self):
	...         return "<Player('%s','%s','%s')>" % (self.first, self.last, self.position)

	# Create mapper to map the table to the class
	>>> from sqlalchemy.orm import mapper
	>>> mapper(Player, player)
	<Mapper at 0x4; Player>

	# Create Session class and bind it to the database
	>>> from sqlalchemy.orm import sessionmaker
	>>> Session = sessionmaker(bind=db)
	>>> session = Session()     

	# Create player objects, add them to the session
	>>> player1 = Player('Josh', 'Juneau', 'forward')
	>>> player2 = Player('Jim', 'Baker', 'forward')
	>>> player3 = Player('Frank', 'Wierzbicki', 'defense')
	>>> player4 = Player('Leo', 'Soto', 'defense')
	>>> player5 = Player('Vic', 'Ng', 'center')
	>>> session.add(player1)
	>>> session.add(player2)
	>>> session.add(player3)
	>>> session.add(player4)
	>>> session.add(player5)

	# Query the objects
	>>> forwards = session.query(Player).filter_by(position='forward').all()
	>>> forwards
	[<Player('Josh','Juneau','forward')>, <Player('Jim','Baker','forward')>]
	>>> defensemen = session.query(Player).filter_by(position='defense').all()
	>>> defensemen 
	[<Player('Frank','Wierzbicki','defense')>, <Player('Leo','Soto','defense')>]
	>>> center = session.query(Player).filter_by(position='center').all()
	>>> center
	[<Player('Vic','Ng','center')>]


Well, hopefully from this example you can see the benefits of using SqlAlchemy.  Of course, you can perform all of the necessary SQL actions such as insert, update,  select, and delete against the objects.  However, as said before there are many very good tutorials where you can learn how to do these things.  We’ve barely scratched the surface of what you can do with SqlAlchemy, it is a very powerful tool to add to any Jython or Python developer’s arsenal.

Hibernate
---------

Hibernate is a very popular object relational mapping solution used in the Java world.  As a matter of fact, it is so popular that many other ORM solutions are either making use of hibernate or extending it in various ways.  As Jython developers, we can make use of Hibernate to create powerful hybrid applications.  Since Hibernate works by mapping POJO (plain old Java object) classes to database tables, we cannot map our Jython objects to it directly.  While we could always try to make use of an object factory to coerce our Jython objects into a format that hibernate could use, this approach leaves a bit to be desired.  Therefore, if you wish to create an application coded entirely using Jython, this would probably not be the best ORM solution.  However, most Jython developers are used to doing a bit of work in Java and as such, they can harness the maturity and power of the hibernate API to create first-class hybrid applications.  This section will show you how to create database persistence objects using Hibernate and Java, and then use them directly from a Jython application.  The end result, code the entity POJOs in Java, place them into a JAR file along with hibernate and all required mapping documents, and then import the JAR into your Jython application and use.



I have found that the easiest way to create such an application is to make use of an IDE like Eclipse or Netbeans.  Then create two separate projects, one of the projects would be a pure Java application that will include the entity beans.  The other project would be a pure Jython application that would include everything else.  In this situation, you could simply add resulting JAR from your Java project into the sys.path of your Jython project and you’ll be ready to go.  However, this works just as well if you do not wish to use an IDE.



It is important to note that this section will provide you with one use case for using Jython, Java, and Hibernate together.  There may be many other scenarios in which this combination of technologies would work out just as well, if not better.  It is also good to note that this section will not cover hibernate in any great depth; we’ll just scratch the surface of what it is capable of doing.  There are a plethora of great hibernate tutorials available on the web if you find this solution to be useful.



Entity Classes and Hibernate Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Since our hibernate entity beans must be coded in Java, most of the hibernate configuration will reside in your Java project.  Hibernate works in a straightforward manner.  You basically map a table to a POJO and use a configuration file to map the two together.  It is also possible to use annotations as opposed to XML configuration files, but for the purposes of this use case I will show you how to use the configuration files.  



The first configuration file we need to assemble is the hibernate.cfg.xml, which goes in the root of your Java project.  The purpose of this file is to define your database connection information as well as declare which entity configuration files will be used in your project.  For the purposes of this example, we will be using the Postgresql database, and we’ll be using one of my classic examples of the hockey roster application.  This makes for a very simple use-case as we only deal with one table here, the Player table.  Hibernate makes it very possible to work with multiple tables and even associate them in various ways. ::



	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE hibernate-configuration PUBLIC "-//Hibernate/Hibernate Configuration DTD 3.0//EN" "http://hibernate.sourceforge.net/hibernate-configuration-3.0.dtd">
	<hibernate-configuration>
	  <session-factory>
	    <!-- Database connection settings -->
	    <property name="connection.driver_class">org.postgresql.Driver</property>
	    <property name="connection.url">jdbc:postgresql://localhost/database-name</property>
	    <property name="connection.username">username</property>
	    <property name="connection.password">password</property>
	    <!-- JDBC connection pool (use the built-in) -->
	    <property name="connection.pool_size">1</property>
	    <!-- SQL dialect -->
	    <property name="dialect">org.hibernate.dialect.PostgreSQLDialect</property>
	    <mapping resource="org/jythonbook/entity/Player.hbm.xml"/>
	  </session-factory>
	</hibernate-configuration>


Our next step is to code the plain old Java object for our database table.  In this case, we’ll code an object named Player that contains only four database columns: id, first, last, and position.  As you’ll see, we use standard public accessor methods with private variables in this class.  ::

	package org.jythonbook.entity;

	public class Player {

	    public Player(){}
	    
	    private long id;
	    private String first;
	    private String last;
	    private String position;
	    
	    public long getId(){
	        return this.id;
	    }

	    private void setId(long id){
	        this.id = id;
	    }
	    
	    public String getFirst(){
	        return this.first;
	    }
	    
	    public void setFirst(String first){
	        this.first = first;
	    }
	    
	    public String getLast(){
	        return this.last;
	    }
	    
	    public void setLast(String last){
	        this.last = last;
	    }
	    
	    public String getPosition(){
	        return this.position;
	    }
	    
	    public void setPosition(String position){
	        this.position = position;
	    }

	}

Lastly, we will create a configuration file that will be used by hibernate to map our POJO to the database table itself.  We’ll ensure that the primary key value is always populated by using a generator class type of increment.  Hibernate also allows for the use of other generators, including sequences if desired.  The player.hbm.xml file should go into the same package as our POJO, in this case, the org.jythonbook.entity package. ::



	<?xml version="1.0"?>
	<!DOCTYPE hibernate-mapping PUBLIC
	"-//Hibernate/Hibernate Mapping DTD 3.0//EN"
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
	<hibernate-mapping
	package="org.jythonbook.entity">

	    <class name="Player" table="player" lazy="true">
	        <comment>Player for Hockey Team</comment>

	        <id name="id" column="id">
	            <generator class="increment"/>
	        </id>

	        <property name="first" column="first"/>
	        <property name="last" column="last"/>
	        <property name="position" column="position"/>

	    </class>

	</hibernate-mapping>

That is all we have to do inside of the Java project for our simple example.  Of course, you can add as many entity classes as you’d like to your own project.  The main point to remember is that all of the entity classes are coded in Java, and we will code the rest of the application in Jython.



Jython Implementation Using the Java Entity Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



The remainder of our use-case will be coded in Jython.  Although all of the hibernate configuration files and entity classes are coded and place within the Java project, we’ll need to import that project into the Jython project, and also import the hibernate JAR file so that we can make use of it’s database session and transactional utilities to work with the entities.  In the case of Netbeans, you’d create a Python application then set the Python platform to Jython 2.5.0.  After that, you should add all of the required hibernate JAR files as well as the Java project JAR file to the Python path from within the project properties.  Once you’ve set up the project and taken care of the dependencies, you’re ready to code the implementation.



As said previously, for this example we are coding a hockey roster implementation.  The application runs on the command line and basically allows one to add players to a roster, remove players, and check the current roster.  All of the database transactions will make use of the Player entity we coded in our Java application, and we’ll make use of hibernate’s transaction management from within our Jython code. ::

    # HockeyRoster.py
    #
    # Implemenatation logic for the HockeyRoster application
    
    # Import Player class from the Player module
    from org.hibernate.cfg import Environment
    from org.hibernate.cfg import Configuration
    from org.hibernate import Query
    from org.hibernate import Session
    from org.hibernate import SessionFactory
    from org.hibernate import Transaction
    from org.jythonbook.entity import Player
    import sys
    
    # Define a list to hold each of te Player objects
    playerList = []
    factory = None
    
    # makeSelection()
    #
    # Creates a selector for our application.  The function prints output to the
    # command line.  It then takes a parameter as keyboard input at the command line
    # in order to choose our application option.
    
    def makeSelection():
        validOptions = ['1','2','3','4','5']
        print "Please chose an option\n"
    
        selection = raw_input("Press 1 to add a player, 2 to print the roster, 3 to search for a player on the team, 4 to remove player, 5 to quit: ")
        if selection not in validOptions:
            print "Not a valid option, please try again\n"
        else:
            if selection == '1':
                addPlayer()
            elif selection == '2':
                printRoster()
            elif selection == '3':
                searchRoster()
            elif selection == '4':
                removePlayer()
            else:
                global runApp
                runApp = False
                print "Thanks for using the HockeyRoster application."
    
    # addPlayer()
    #
    # Accepts keyboard input to add a player object to the roster list.  This function
    # creates a new player object each time it is invoked and appends it to the list.
    def addPlayer():
        addNew = 'Y'
        print "Add a player to the roster by providing the following information\n"
        while addNew.upper() == 'Y':
            first = raw_input("First Name: ")
            last = raw_input("Last Name: ")
            position = raw_input("Position: ")
            id = len(playerList)
            session = factory.openSession()
            try:
                tx = session.beginTransaction()
                player = Player()
                player.first = first
                player.last = last
                player.position = position
                session.save(player)
                tx.commit()
            except Exception,e:
                if tx!=None:
                    tx.rollback()
                    print e
            finally:
                session.close()
    
           # playerList.append(player)
            print "Player successfully added to the roster\n"
            addNew = raw_input("Add another? (Y or N)")
        makeSelection()
    
    # printRoster()
    #
    # Prints the contents of the list to the command line as a report
    def printRoster():
        print "====================\n"
        print "Complete Team Roster\n"
        print "======================\n\n"
        playerList = returnPlayerList()
        for player in playerList:
            print "%s %s - %s" % (player.first, player.last, player.position)
        print "\n"
        print "=== End of Roster ===\n"
        makeSelection()
    
    # searchRoster()
    #
    # Takes input from the command line for a player's name to search within the
    # roster list.  If the player is found in the list then an affirmative message
    # is printed.  If not found, then a negative message is printed.
    def searchRoster():
        index = 0
        found = False
        print "Enter a player name below to search the team\n"
        first = raw_input("First Name: ")
        last = raw_input("Last Name: ")
        position = None
        playerList = returnPlayerList()
        while index < len(playerList):
            player = playerList[index]
            if player.first.upper() == first.upper() and player.last.upper() == last.upper():
                found = True
                position = player.position
            index = index + 1
        if found:
            print '%s %s is in the roster as %s' % (first, last, position)
        else:
            print '%s %s is not in the roster.' % (first, last)
        makeSelection()
    
    def removePlayer():
        index = 0
        found = False
        print "Enter a player name below to remove them from the team roster\n"
        first = raw_input("First Name: ")
        last = raw_input("Last Name: ")
        position = None
        playerList = returnPlayerList()
        foundPlayer = Player()
        while index < len(playerList):
            player = playerList[index]
            if player.first.upper() == first.upper() and player.last.upper() == last.upper():
                found = True
                foundPlayer = player
            index = index + 1
        if found:
            print '%s %s is in the roster as %s, are you sure you wish to remove?' % (foundPlayer.first, foundPlayer.last, foundPlayer.position)
            yesno = raw_input("Y or N")
            if yesno.upper() == 'Y':
                session = factory.openSession()
                try:
                    delQuery = "delete from Player player where id = %s" % (foundPlayer.id)
    
                    tx = session.beginTransaction()
                    q = session.createQuery(delQuery)
                    q.executeUpdate()
                    tx.commit()
                    print 'The player has been removed from the roster', foundPlayer.id
                except Exception,e:
                    if tx!=None:
                        tx.rollback()
                    print e
                finally:
                    session.close
            else:
                print 'The player will not be removed'
        else:
            print '%s %s is not in the roster.' % (first, last)
        makeSelection()
    
    def returnPlayerList():
        session = factory.openSession()
        try:
            tx = session.beginTransaction()
            playerList = session.createQuery("from Player").list()
            tx.commit()
        except Exception,e:
            if tx!=None:
                tx.rollback()
            print e
        finally:
            session.close
        return playerList
    
    
    # main
    #
    # This is the application entry point.  It simply prints the applicaion title
    # to the command line and then invokes the makeSelection() function.
    if __name__ == "__main__":
        print "Hockey Roster Application\n\n"
        cfg = Configuration().configure()
    
        factory = cfg.buildSessionFactory()
        global runApp
        runApp = True
        while runApp:
            makeSelection()
    
    
We begin our implementation in the main block, where the hibernate configuration is loaded.  All of the hibernate configuration resides within the Java project, so we are not working with XML here, just making use of it.  The code then begins to branch so that various tasks can be performed.  In the case of adding a player to the roster, a user could enter the number 1 at the command prompt.  You can see that the addPlayer() function simply creates a new Player object, populates it, and saves it into the database.  Likewise, the searchRoster() function calls another function named returnPlayerList() which queries the player table using hibernate query language and returns a list of Player objects.



In the end, we have a completely scalable solution.  We can code our entities using a mature and widely used Java ORM solution, and then implement the rest of the application in Jython.  This allows us to make use of the best features of the Python language, but at the same time, persist our data using Java.



Conclusion
==========

You would be hard-pressed to find too many enterprise-level applications today that do not make use of a relational database in one form or another.  The majority of applications in use today use databases to store information as they help to provide robust solutions.  That being said, the topics covered in this chapter are very important to any developer.  In this chapter we learned that there are many different ways to implement database applications in Jython, specifically through the Java database connectivity API or an object relational mapping solution.






