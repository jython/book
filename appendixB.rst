Appendix B:  Jython Cookbook - A compilation of community submitted code examples
=================================================================================

There are a plethora of examples for using Jython that can be found on the web.  This
appendix is a compilation of some of the most useful examples that we have found.  There
are hundreds of examples available on the web.  These that were chosen are focused on topics
that are not widely covered elsewhere on the web.

Unless otherwise noted, each
of these examples have been originally authored for working on versions of Jython prior to 2.5.x but
we have tested each of them using Jython 2.5.1 and function as advertised.


Logging
-------

Using log4j With Jython - Josh Juneau
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Are you still using the Jython print command to show your errors? How about in a production environment, are you using any formal logging?
If not, you should be doing so...and the Apache log4j API makes it easy to do so. Many Java developers have grown to love the log4j API
and it is utilized throughout much of the community. That is great news for Jython developers since we've got direct access to Java libraries!

**Setting Up Your Environment**

The most difficult part about using log4j with Jython is the setup. You must ensure that the log4j.jar archive resides somewhere
within your Jython PATH (usually this entails setting the CLASSPATH to include necessary files). You then set up a properties file for use
with log4j. Within the properties file, you can include appender information, where logs should reside, and much more.

*Example properties file:*

::
    log4j.rootLogger=debug, stdout, R
    
    log4j.appender.stdout=org.apache.log4j.ConsoleAppender
    log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
    
    # Pattern to output the caller's file name and line number.
    log4j.appender.stdout.layout.ConversionPattern=%5p [%t] (%F:%L) - %m%n
    
    log4j.appender.R=org.apache.log4j.RollingFileAppender
    log4j.appender.R.File=C:\\Jython\\testlog4j.log
    
    log4j.appender.R.MaxFileSize=100KB
    # Keep one backup file
    log4j.appender.R.MaxBackupIndex=1
    
    log4j.appender.R.layout=org.apache.log4j.PatternLayout
    log4j.appender.R.layout.ConversionPattern=%p %t %c - %m%n

You are now ready to use log4j in your Jython application. As you can see, if you've ever used log4j with Java, it is pretty much the same.

**Using log4j in a Jython Application**

Once again, using log4j within a Jython application is very similar to it's usage in the Java world.

First, you must import the log4j packages:

::
    from org.apache.log4j import *

Second, you obtain a new logger for your class or module and set up a PropertyConfigurator:

::
    logger = Logger.getLogger("myClass")
    # Assume that the log4j properties resides within a folder named "utilities"
    PropertyConfigurator.configure(sys.path[0] + "/utilities/log4j.properties")

Lastly, use log4j:

::
    # Example module within the class:
    def submitDocument(self, event):
        try:
            # Assume we perform some SQL here              
        except SQLException, ex:
            self.logger.error("docPanel#submitDocument ERROR: %s" % (ex))

Your logging will now take place within the file you specified in the properties file for log4j.appender.R.File.

**Using log4j in Jython Scripts**

Many may ask, why in the world would you be interested in logging information about your scripts? Most of the time a script is
executed interactively via the command line. However, there are plenty of instances where it makes sense to have the system invoke
a script for you. As you probably know, this technique is used quite often within an environment to run nightly tasks, or even daily
tasks which are automatically invoked on a scheduled basis. For these cases, it can be extremely useful to log errors or information
using log4j. Some may even wish to create a separate automated task to email these log files after the tasks complete.

The overall implementation is the same as above, the most important thing to remember is that you must have the log4j.jar archive
and properties file within your Jython path. Once this is ready to go you can use log4j in your script.

::
    from org.apache.log4j import *
    logger = Logger.getLogger("scriptname")
    PropertyConfigurator.configure("C:\path_to_properties\log4j.properties")
    logger.info("Test the logging")

  
Author: Josh Juneau
URL:  http://wiki.python.org/jython/JythonMonthly/Articles/August2006/1

Another log4j Example
~~~~~~~~~~~~~~~~~~~~~

This example require several things.

- log4j on the classpath
- log4j.properties (below) in the same directory as the example
- example.xml (below) in the same directory as the example below
- And of course Jython

**log4j Example**

This is a simple example to show how easy it is to use log4j in your own scripts. The source is well documented but
if you have any questions or want to more info use your favorite search engine and type in log4j.

::
    
    from org.apache.log4j import *
     
    class logtest:
        def __init__(self):
            log.info("start of Logtest")
            log.debug('just before file read')
            try:
                log.warn('file read proceding to processing')
                xmlStringData = open('example.xml').read()
            except:
                #yes, more could have been done here but this is just an example
                log.error('file read FAILURE')
            log.info('file read proceding to processing')
            # since this is just an example processing would go here.
            log.warn('its just an example, OK?')
            pi = 3.141592681
            msg = 'do you like?' + str(pi)
            log.info(msg)
            log.debug('lets try to parse the string')
            if '[CDATA' in xmlStringData:
            log.warn('No CDATA section.')
            #say good bye and close the log file.
            log.info('That all. The End. Good Bye')
            log.shutdown()
            
            
    if __name__ == '__main__':
        # loggingTest is just a string that identifies this log.
        log = Logger.getLogger("loggingTest")
        #use the config data in the properties file
        PropertyConfigurator.configure('log4j.properties')
        log.info('This is the start of the log file')
        logit = logtest()
        print '\n\nif you change the log level in the properties'
        print "file you'll get varing amouts of log data."

**log4j.properties**

This file is required by the code above. it need to be in the same directory as the example however It can be anywhere as log as
you provide a full path to the file. It configures how log4j operates. If it is not found it defaults to a default logging level.
Since this is for example purposes the file below is larger then really needed.

::
    #define loging level and output
    log4j.rootLogger=debug, stdout, LOGFILE
    #log4j.rootLogger=info, LOGFILE
    # this 2 lines tie the apache logging into log4j
    #log4j.logger.org.apache.axis.SOAPPart=DEBUG
    #log4j.logger.httpclient.wire.header=info
    #log4j.logger.org.apache.commons.httpclient=DEBUG
    
    # where is the logging going. 
    # This is for std out and defines the log output format
    log4j.appender.stdout=org.apache.log4j.ConsoleAppender
    log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
    log4j.appender.stdout.layout.ConversionPattern=%d{HH:mm:ss,SSS} | %p | [%c] %m%n %t
    
    #log it to a file as well. and define a filename, max file size and number of backups
    log4j.appender.LOGFILE=org.apache.log4j.RollingFileAppender
    log4j.appender.LOGFILE.File=jythonTest.log
    log4j.appender.LOGFILE.MaxFileSize=100KB
    # Keep one backup file
    log4j.appender.LOGFILE.MaxBackupIndex=1
    
    log4j.appender.LOGFILE.layout=org.apache.log4j.PatternLayout
    # Pattern for logfile - only diff is that date is added
    log4j.appender.LOGFILE.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss} | %p | [%c] %m%n
    # Other Examples: only time, loglog level, loggerName
    #log4j.appender.LOGFILE.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss},%p,%c %m%n
    #above plus filename, linenumber, Class Name, method name
    #log4j.appender.LOGFILE.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss},%p,%c,%F,%L,%C{1},%M %m%n

**Example xml file**

This is here for completeness. Any text file could be use with the example above by changing the 'open' line
in the above line.

::
    <?xml version="1.0" encoding="utf-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                       xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <SOAP-ENV:Body>
        <GetXmlReport xmlns="http://localhost/Services/GetXmlReport">
          <xmlrequest>
            <Inquiry>
              <Client>
                <Type>W</Type>
              </Client>
              <Report>I</Report>
              <Provider>
                <ProviderID>TU</ProviderID>
              </Provider>
              <ClientInfo>
                <Name>
                  <First>Cathrine</First>
                  <Middle />
                  <Surname>Knight</Surname>
                </Name>
                <Account>34-5424-77</Account>
                <DateOfBirth>10/12/1938</DateOfBirth>
                <Address>
                  <Line1>4780 Centerville</Line1>
                  <CityStPostal>Saint Paul, MN 55127</CityStPostal>
                </Address>
              </ClientInfo>
            </Inquiry>
          </xmlrequest>
        </GetXmlReport>
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>

URL:  http://wiki.python.org/jython/Log4jExample

Working with Spreadsheets
-------------------------

Below are a few Apache Poi examples. These examples requires Apache Poi installed and on the classpath.

**Create Spreadsheet**

This is from the Jython mailing list and was posted September 2007

This is based on Java code at http://officewriter.softartisans.com/OfficeWriter-306.aspx and converted to Jython by Alfonso Reyes

::
    #jython poi example. from Jython mailing list
     
    from java.io import FileOutputStream
    from java.util import Date
    from java.lang import System, Math
    from org.apache.poi.hssf.usermodel import *
    from org.apache.poi.hssf.util import HSSFColor
     
    startTime = System.currentTimeMillis()
     
    wb = HSSFWorkbook()
    fileOut = FileOutputStream("POIOut2.xls")
     
     
    # Create 3 sheets
    sheet1 = wb.createSheet("Sheet1")
    sheet2 = wb.createSheet("Sheet2")
    sheet3 = wb.createSheet("Sheet3")
    sheet3 = wb.createSheet("Sheet4")
     
    # Create a header style
    styleHeader = wb.createCellStyle()
    fontHeader = wb.createFont()
    fontHeader.setBoldweight(2)
    fontHeader.setFontHeightInPoints(14)
    fontHeader.setFontName("Arial")
    styleHeader.setFont(fontHeader)
     
    # Create a style used for the first column
    style0 = wb.createCellStyle()
    font0 = wb.createFont()
    font0.setColor(HSSFColor.RED.index)
    style0.setFont(font0)
     
     
    # Create the style used for dates.
    styleDates = wb.createCellStyle()
    styleDates.setDataFormat(HSSFDataFormat.getBuiltinFormat("m/d/yy h:mm"))
     
     
    # create the headers
    rowHeader = sheet1.createRow(1)
    # String value
    cell0 = rowHeader.createCell(0)
    cell0.setCellStyle(styleHeader)
    cell0.setCellValue("Name")
     
     
    # numbers
    for i in range(0, 8, 1):
        cell = rowHeader.createCell((i + 1))
        cell.setCellStyle(styleHeader)
        cell.setCellValue("Data " + str( (i + 1)) )
     
    # Date
    cell10 = rowHeader.createCell(9)
    cell10.setCellValue("Date")
    cell10.setCellStyle(styleHeader)
     
    for i in range(0, 100, 1):
        # create a new row
        row = sheet1.createRow(i + 2)
        for j in range(0, 10, 1):
            # create each cell
            cell = row.createCell(j)
            # Fill the first column with strings
            if j == 0:
                cell.setCellValue("Product " + str(i))
                cell.setCellStyle(style0)  
            # Fill the next 8 columns with numbers.
            elif j < 9:
                cell.setCellValue( (Math.random() * 100))
            # Fill the last column with dates.
            else:
                cell.setCellValue(Date())
                cell.setCellStyle(styleDates)
    # Summary row
    rowSummary = sheet1.createRow(102)
    sumStyle = wb.createCellStyle()
    sumFont = wb.createFont()
    sumFont.setBoldweight( 5)
    sumFont.setFontHeightInPoints(12)
    sumStyle.setFont(sumFont)
    sumStyle.setFillPattern(HSSFCellStyle.FINE_DOTS)
    sumStyle.setFillForegroundColor(HSSFColor.GREEN.index)
    cellSum0 = rowSummary.createCell( 0)
    cellSum0.setCellValue("TOTALS:")
    cellSum0.setCellStyle(sumStyle)
     
     
    # numbers
    # B
    cellB = rowSummary.createCell( 1)
    cellB.setCellStyle(sumStyle)
    cellB.setCellFormula("SUM(B3:B102)")

**Read an Excel file**

Posted to the Jython-users mailing list by Alfonso Reyes on October 14, 2007 This Jython code will open and read an existant
Excel file you can download the file at http://www.nabble.com/file/p13199712/Book1.xls

::
    """    read.py
    Read an existant Excel file (Book1.xls) and show it on the screen
    """
    from org.apache.poi.hssf.usermodel import *
    from java.io import FileInputStream
    
    file = "H:Book1.xls"
    print file
    fis = FileInputStream(file)
    wb = HSSFWorkbook(fis)
    sheet = wb.getSheetAt(0)
    
    # get No. of rows
    rows = sheet.getPhysicalNumberOfRows()
    print wb, sheet, rows
    
    cols = 0 # No. of columns
    tmp = 0
    
    # This trick ensures that we get the data properly even if it
    # doesnÕt start from first few rows
    for i in range(0, 10,1):
        row = sheet.getRow(i)
        if(row != None):
            tmp = sheet.getRow(i).getPhysicalNumberOfCells()
            if tmp > cols:
                cols = tmp
    print cols
    
    for r in range(0, rows, 1):
        row = sheet.getRow(r)
        print r
        if(row != None):
            for c in range(0, cols, 1):
                cell = row.getCell(c)
                if cell != None:
                    print cell
    
    #wb.close()
    fis.close()

URL: http://wiki.python.org/jython/PoiExample

Jython and XML
--------------

Element tree

Here is a simple example of using element tree with Jython. Element tree is useful for storing hierarchical
data structures, such as simplified XML infosets, into memory and then save them to disk.
More information on element tree is at http://effbot.org/zone/element-index.htm.

Download element tree from http://effbot.org/downloads/

::
    from  elementtree import ElementTree as ET
    
    root = ET.Element("html")
    head = ET.SubElement(root, "head")
    title = ET.SubElement(head, "title")
    title.text = "Page Title"
    body = ET.SubElement(root, "body")
    body.set("bgcolor", "#ffffff")
    body.text = "Hello, World!"
    tree = ET.ElementTree(root)
    tree.write("page.xhtml")
    
    import sys
    tree.write(sys.stdout)

which produces:

::
    <html><head><title>Page Title</title></head><body bgcolor="#ffffff">Hello, World!</body></html>


URL:  http://wiki.python.org/jython/XmlRelatedExamples

Writing and Parsing RSS with ROME - Josh Juneau
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Introduction**

RSS is an old technology now...it has been around for years. However, it is a technology which remains very useful for
disseminating news and other information. The ROME project on java.net is helping to make parsing, generating, and publishing
RSS and Atom feeds a breeze for any Java developer.

Since I am particularly fond of translating Java to Jython code, I've taken simple examples from the Project ROME wiki and
translated Java RSS reader and writer code into Jython. It is quite easy to do, and it only takes a few lines of code.

Keep in mind that you would still need to build a front-end viewer for such an RSS reader, but I think you will get the idea
of how easy it can be just to parse a feed with Project ROME and Jython.

**Setting Up The CLASSPATH**

In order to use this example, you must obtain the ROME and JDOM jar files and place them into your CLASSPATH.

Windows:
::
    set CLASSPATH=C:\Jython\Jython2.2\rome-0.9.jar;%CLASSPATH%
    set CLASSPATH=C:\Jython\Jython2.2\jdom.jar;%CLASSPATH%
    
OSX:
::
    export CLASSPATH=/path/to/rome-0.9.jar:/path/to/jdom.jar

**Parsing Feeds**

Parsing feeds is easy with ROME. Using ROME with Jython makes it even easier with the elegant Jython syntax. I am not a professional
Python or Jython programmer, I am a Java programmer by profession, so my Jython interpretation may be even wordier than it should be.

I took the FeedReader example from the ROME site and translated it into Jython below. You can copy and paste the following code
into your own FeedReader.py module and run it to parse feeds. However, the output is unformatted and ugly...creating a good
looking front end is up to you.

FeedReader.py
::
    ########################################
    # File: FeedReader.py
    #
    # This module can be used to parse an RSS feed
    ########################################
    from java.net import URL
    from java.io import InputStreamReader
    from java.lang import Exception
    from java.lang import Object
    from com.sun.syndication.feed.synd import SyndFeed
    from com.sun.syndication.io import SyndFeedInput
    from com.sun.syndication.io import XmlReader
    
    class FeedReader(Object):
       def __init__(self, url):
          self.inUrl = url
    
       def readFeed(self):
          ok = False
          #####################################
          # If url passed in is blank, then use a default
          #####################################
          if self.inUrl != '':
             rssUrl = self.inUrl
          else:
             rssUrl = "http://www.dzone.com/feed/frontpage/java/rss.xml"
          #####################################
          # Parse feed located at given URL
          #####################################
          try:
             feedUrl = URL(rssUrl)
             input = SyndFeedInput()
             feed = input.build(XmlReader(feedUrl))
             ####################################
             # Do something here with feed data
             ####################################
             print(feed)
             ok = True
          except Exception, e:
             print 'An exception has occurred', e
          if ok != True:
             print 'An error has occurred in this reader'
    
    if __name__== "__main__":
        reader = FeedReader('')
        reader.readFeed()
        print '****************Command Complete...RSS has been parsed*****************'

**Creating Feeds**

Similar to parsing a feed, writing a feed is also quite easy. When one creates a feed, it appears to be a bit more complex
than parsing, but if you are familiar with XML and it's general structure then it should be relatively easy.

Creating a feed is a three step process. You must first create the feed element itself, then you must add individual feed entries,
and lastly you must publish the XML.

FeedWriter.py
::
    ########################################
    # File: FeedReader.py
    #
    # This module can be used to create an RSS feed
    ########################################
    from com.sun.syndication.feed.synd import *
    from com.sun.syndication.io import SyndFeedOutput
    from java.io import FileWriter
    from java.io import Writer
    from java.text import DateFormat
    from java.text import SimpleDateFormat
    from java.util import ArrayList
    from java.util import List
    from java.lang import Object
    
    class FeedWriter(Object):
        ####################################
        # Set up the date format
        ####################################
        def __init__(self, type, name):
           self.DATE_PARSER = SimpleDateFormat('yyyy-MM-dd')
           self.feedType = type
           self.fileName = name
    
        def writeFeed(self):
           ok = False
           try:
            ################################
            # Create the feed itself
            ################################
              feed = SyndFeedImpl()
              feed.feedType =self.feedType
              feed.title = 'Sample Feed (created with ROME)'
              feed.link = 'http://rome.dev.java.net'
              feed.description = 'This feed has been created using ROME and Jython'
     
             ###############################
             # Add entries to the feed
             ###############################
              entries = ArrayList()
              entry = SyndEntryImpl()
              entry.title = 'ROME v1.0'
              entry.link = 'http://wiki.java.net/bin/view/Javawsxml/Rome01'
              entry.publishedDate = self.DATE_PARSER.parse("2004-06-08")
              description = SyndContentImpl()
              description.type = 'text/plain'
              description.value = 'Initial Release of ROME'
              entry.description = description
              entries.add(entry)
         
              entry = SyndEntryImpl()
              entry.title = 'ROME v2.0'
              entry.link = 'http://wiki.java.net/bin/view/Javawsxml/Rome02'
              entry.publishedDate = self.DATE_PARSER.parse("2004-06-16")
              description = SyndContentImpl()
              description.type = 'text/plain'
              description.value = 'Bug fixes, minor API changes and some new features'
              entry.description = description
              entries.add(entry)
    
              entry = SyndEntryImpl()
              entry.title = 'ROME v3.0'
              entry.link = 'http://wiki.java.net/bin/view/Javawsxml/Rome03'
              entry.publishedDate = self.DATE_PARSER.parse("2004-07-27")
              description = SyndContentImpl()
              description.type = 'text/plain'
              description.value = '<p>More Bug fixes, mor API changes, some new features and some Unit testing</p>'
              entry.description = description
              entries.add(entry)
    
              feed.entries = entries
             ###############################
             # Publish the XML
             ###############################
              writer = FileWriter(self.fileName)
              output = SyndFeedOutput()
              output.output(feed,writer)
              writer.close()
     
              print('The feed has been written to the file')
    
              ok = True
      
           except Exception, e:
              print 'There has been an exception raised',e
    
           if ok == False:
              print 'Feed Not Printed'
    
    if __name__== "__main__":
        ####################################
        # You must change his file location
        # if not using Windows environment
        ####################################
        writer = FeedWriter('rss_2.0','C:\\TEMP\\testRss.xml')
        writer.writeFeed()
        print '****************Command Complete...RSS XML has been created*****************'

After you have created the XML, you'll obviously need to place it on a web server somewhere so that others can use your feed.
The FeedWriter.py module would probably be one module amongst many in an application for creating and managing RSS Feeds, but you get the idea.

**Conclusion**

As you can see, using the ROME library to work with RSS feeds is quite easy. Using the ROME library within a Jython application
is straight forward. As you have now seen how easy it is to create and parse feeds, you can apply these technologies to a more
complete RSS management application if you'd like. The world of RSS communication is at your fingertips!

Author:  Josh Juneau
URL:  http://wiki.python.org/jython/JythonMonthly/Articles/October2007/1

Using the CLASSPATH - Steve Langer
----------------------------------

**Introduction**

During Oct-Nov 2006 there was a thread in the jython-users group titled "adding JARs to sys.path". More accurately
the objective there was to add JARs to the sys.path at runtime. Several people asked the question, "Why would you want to do that?"
Well there are at least 2 good reasons. First, if you want to distribute a jython or Java package that includes non-standard
Jars in it. Perhaps you want to make life easier for the target user and not demand that they know how to set environment variables.
A second even more compelling reason is when there is no normal user account to provide environment variables.

"What?", you ask. Well, in my case I came upon this problem in the following way. I am working on an open source IHE
Image Archive Actor and needed a web interface. I'm using AJAX on the client side to route database calls through CGI to a
jython-JDBC enabled API. Testing the jython-JDBC API from the command line worked fine, I had the PostGres driver in my CLASSPATH.
But, when called via the web interface I got "zxJDBC error, postGres driver not found" errors. Why? Because APACHE was calling
the API and APACHE is not a normal account with environment variables.

**What to do?**

The jython-users thread had many suggestions but none were found to work. For books, Chapter 11 of O'Reilly's "Jython Essentials"
mentions under "System and File Modules" that "... to load a class at runtime one also needs an appropriate class loader."
Of course, no mention is made beyond that. After a while, it occured to me that perhaps someone in the Java world had found a similar
problem and had solved it. Then all that would be required is to translate that solution. And that is exactly what happened.

**Method**

For brevity we will not repeat the original Java code here. This is how I call the Jython class (note that one can use either
addFile or addURL depending on whether the Jar is on a locally accesable file system or remote server).

::
    import sys
    from com.ziclix.python.sql import zxJDBC
    
    d,u,p,v = "jdbc:postgresql://localhost/img_arc2","postgres","","org.postgresql.Driver"
    
    try :
        # if called from command line with .login CLASSPATH setup right,this works
        db = zxJDBC.connect(d, u, p, v)
    except:
        # if called from Apache or account where the .login has not set CLASSPATH
        # need to use run-time CLASSPATH Hacker
        try :
            jarLoad = classPathHacker()
            a = jarLoad.addFile("/usr/share/java/postgresql-jdbc3.jar")
            db = zxJDBC.connect(d, u, p, v)
        except :
            sys.exit ("still failed \n%s" % (sys.exc_info() ))

And here is the class "classPathHacker" which is what the original author called his solution. In fact, you can simply Google
on "classPathHacker" to find the Java solution.

::
    class classPathHacker :
    ##########################################################
    # from http://forum.java.sun.com/thread.jspa?threadID=300557
    #
    # Author: SG Langer Jan 2007 translated the above Java to this
    #       Jython class
    # Purpose: Allow runtime additions of new Class/jars either from
    #       local files or URL
    ######################################################
            import java.lang.reflect.Method
            import java.io.File
            import java.net.URL
            import java.net.URLClassLoader
            import jarray
    
            def addFile (self, s):
            #############################################
            # Purpose: If adding a file/jar call this first
            #       with s = path_to_jar
            #############################################
                    module = "utils:classPathHacker: addFile"
    
                    # make a URL out of 's'
                    f = self.java.io.File (s)
                    u = f.toURL ()
                    a = self.addURL (u)
                    return a
    
            def addURL (self, u):
            ##################################
            # Purpose: Call this with u= URL for
            #       the new Class/jar to be loaded
            #################################
                    module = "utils:classPathHacker: addURL"
    
                    parameters = self.jarray.array([self.java.net.URL], self.java.lang.Class)
                    sysloader =  self.java.lang.ClassLoader.getSystemClassLoader()
                    sysclass = self.java.net.URLClassLoader
                    method = sysclass.getDeclaredMethod("addURL", parameters)
                    a = method.setAccessible(1)
                    jar_a = self.jarray.array([u], self.java.lang.Object)
                    b = method.invoke(sysloader, jar_a)
                    return u

**Conclusions**

That's it. Depressingly short for what it does, but then that's another proof of the power of this language. I hope you find
this as powerful and useful as I have. It allows the possibility of distributing jython packages with all their file dependencies
within the installation directory, freeing the user or developer from the need to alter user environment variables, which should
lead to more programmer control and thus higher reliabliity.

Author:  Steve Langer
URL:  http://wiki.python.org/jython/JythonMonthly/Articles/January2007/3

Ant
---

**The following Ant example works with Jython version 2.2.1 and earlier only due to the necessary jythonc usage.  Jythonc
is no longer distributed with Jython as of 2.5.0.  This example could be re-written using object factories to work with
current versions of Jython.**

Writing Ant Tasks With Jython - Ed Takema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ant is the current tool of choice for java builds. This is so partially because it was the first java oriented build tool
on the scene and because the reigning champion *Make* was getting long in the tooth and had fallen out of favour with the
java crowd. But Java builds are getting more and more difficult and these days there is general dissatisfaction with ant1.
Note particularly Bruce Eckel's Comments and Martin Fowler's further comments. The comments to Bruce Eckels's posting show
similar fustrations. Fowler summarizes the issues like this:

... Simple builds are easy to express as a series of tasks and dependencies. For such builds the facilities of ant/make
work well. But more complex builds require conditional logic, and that requires more general programming language constructs
- and that's where ant/make fall down.
Ken Arnold's article The Sum of Ant led me to Jonathon Simon's article Scripting with Jython Instead of XML and got me thinking
about extending ant with Jython. Simon's article presents a technique to drive Ant tasks, testing, etc all from Jython.
What I am presenting is a technique to embed Jython scripts into Ant which is admittedly backwards from Simon's approach,
but hopefully adds power and flexibility to ant builds.

My experience working with large builds automated through ant is not dissimilar to what Fowler is referring to. Eventually, builds
need to do either a lot of odd conditional logic in the xml file and ends up burying the logic in scripts, or in a large number of
custom tasks written in java. This is particularly the case if your builds include non-java source that ant just isn't smart about
building. In one case in particular, the set of custom tasks for the build is really its own system with maintenance and staff costs
that are quite substantial. A large number of scripts can quickly become a problem for enterprise build systems as they are difficult
to standardize and cross platform issues are always looming.

Fortunately, all is not lost. Ant continues to evolve and version 1.6 was a significant step forward for large build systems. Mike Spille,
in his article ANT's Finally a Real Build Tool, demonstrates that the new <import> tag now allows build managers to write truly modular
and standardized build systems based on Ant! As Ant grows up, more and more of these issues will get resolved.

One of the strengths that Make always had was the ability to easily call scripts and command utilities. This is something that is definitely
possible with Ant script/exec tasks, but it feels very un-java. What we need is an elegant way to add adhoc behaviour to Ant builds
... in a java-ish way.

Writing Custom Ant Tasks
~~~~~~~~~~~~~~~~~~~~~~~~

What I think can do the job is to take a more considered approach to using a scripting tool inside an ant build. Rather than just create
a mishmash of scripts that are called from exec or script tasks, I suggest that we write custom ant build tasks in a high level scripting
language...in this case, Jython.

Writing custom ant tasks allows a build manager to leverage the huge number of already written tasks in their builds while writing
what naturally belongs in a more flexible tool in custom ant tasks that can themselves then be reused, are as cross platform as java
itself, and wholly integrated into Ant. Because Ant uses java introspection to determine the capabilities of custom tasks, Jython
is the perfect tool to accomplish this. All we need to do is ensure that the methods that Ant expects are present in the Jython
classes and Ant won't notice the difference.

What we will implement is the perennial SimpleTask which is nothing more than a 'Hello World' for ant. It should be sufficient
to demonstrate the key steps.

**Setup Development Environment**

To compile the jython source in this article you will need to add the ant.jar file to your classpath. This will make it
available to Jython to extend which we'll do below. To do that define your classpath:

::
    <DOS>
    set CLASSPATH=c:\path\to\ant\lib\ant.jar

::
    <UNIX>
    export CLASSPATH=/path/to/ant/lib/ant.jar


**SimpleTask Jython Class**

The following is a very simple Ant task written in Jython(python). Save this as SimpleTask.py

::
    
    from org.apache.tools.ant import Task
    
    class SimpleTask(Task): 
    
      message = ""
    
      def execute(self):
         """@sig public void execute()"""
         Task.log(self, "Message: " + self.message)
    
      def setMessage(this, aMessage):
         """@sig public void setMessage(java.lang.String str)"""
         this.message = aMessage


This simple Jython class extends the ant Task superclass. For each of the properties we want to support for this task, we write a setXXXXX
method where XXXXX corresponds to the property we are going to set in the ant build file. Ant creates an object from the class, calls the
setXXXXX methods to setup the properties and then calls the execute method (actually, it calls the perform method on the Task superclass
which calls the execute() method). So lets try it out.

**Compiling Jython Code To A Jar**

To build this into a jar file for use in Ant, do the following:

::
    jythonc -a -c -d -j myTasks.jar SimpleTask.py

This will produce a jar file myTasks.jar and include the jython core support classes in the jar. Copy this jar file into your
ant installation's lib directory. In my case I copy it to c:\tools\ant\lib.

**Build.XML file to use the Task**

Once you've got that working, here is a very simple test ant build file to test your custom jython task.

::
    <project name="ant jython demo" default="testit" basedir=".">
    
      <!-- Define the tasks we are building -->
      <taskdef name="Simple" classname="SimpleTask" />
    
      <!-- Test Case starts here -->
      <target name="testit"> 
         <Simple message="Hello World!" />
      </target>
    
    </project>

**A Task Container Task**

All right, that is a pretty simple task. What else can we do?  Well, the sky is the limit really. Here is an example
of a task container. In this case, the task holds references to a set of other tasks (SimpleTask tasks in this case):

::
    from org.apache.tools.ant import Task
    from org.apache.tools.ant import TaskContainer
    
    class SimpleContainer(TaskContainer): 
    
      subtasks = []
    
      def execute(this):
         """@sig public void execute()"""
         
         for task in this.subtasks:
             task.perform()        
         
      def createSimpleTask(self):
         """@sig public java.lang.Object createSimpleTask()"""   
    
         task = SimpleTask()
         self.subtasks.append(task)
         return task
    
    class SimpleTask(Task): 
    
      message = ""
    
      def execute(self):
         """@sig public void execute()"""
         Task.log(self, "Message: " + self.message)
    
      def setMessage(this, aMessage):
         """@sig public void setMessage(java.lang.String str)"""
         this.message = aMessage


The SimpleContainer extends the TaskContainer java class. Its createSimpleTask method creates a SimpleTask object and returns
it to Ant so its properties can be set. Then when all the tasks have been added to the container and their properties set, the execute
method on the SimpleContainer class is called which in turn calls the perform method on each of the contained tasks. Note that the
perform method is inherited from the Task superclass and it in turn calls the the execute method which we have overriden.

**Build.XML file to use the TaskContainer**

Here is a ant build file to test your custom jython task container. Note that you don't need to include a task definition
for the contained SimpleTask unless you want to use it directly. The createSimpleTask factory method does it for you.

::
    <project name="ant jython demo" default="testit" basedir=".">
    
      <!-- Define the tasks we are building -->
      <taskdef name="Container" classname="SimpleContainer" />
    
      <!-- Test Case starts here -->
      <target name="testit"> 
    
         <Container> 
    
             <SimpleTask message="hello" />
             <SimpleTask message="there" />
    
         </Container>
    
      </target>
    
    </project>

**Things To Look Out For**

As I learned this technique I discovered that the magic doc strings are really necessary to force Jython to put the right methods
in the generated java classes. For example:

::
    """@sig public void execute()"""

This is primarily due to Ant's introspection that looks for those specific methods and signatures. These docstrings are required
or Ant won't recognize the classes as Ant tasks.

I also learned that for Jython to extend a java class, it must specifically import the java classes using this syntax:

::
    from org.apache.tools.ant import Task
    from org.apache.tools.ant import TaskContainer
    
    class MyTask(Task):
       ...
    You can not use this syntax:
    
    import org.apache.tools.ant.Task
    import org.apache.tools.ant.TaskContainer
    
     class MyTask(org.apache.tools.ant.Task):
        ...


This is because, for some reason, Jython doesn't figure out that MyTask is extending this java class and so doesn't generate the
right Java wrapper classes. You will know that this working right when you see output like the following when you run the jythonc compiler:

::
    processing SimpleTask
    
    Required packages:
      org.apache.tools.ant
    
    Creating adapters:
    
    Creating .java files:
      SimpleTask module
        SimpleTask extends org.apache.tools.ant.Task <<<

Summary
~~~~~~~

So there you have it. Here is a quick summary then of why this is a helpful technique.

First, it is a lot faster to write ant tasks that integrate with third party tools and systems using a glue language and python/jython
is excellent at that. That is really my prime motivation for trying out this technique.

Secondly, Jython has the advantage over other scripting languages (which could be run using Ant's exec or script tasks) because
it can be tightly integrated with Ant (i.e. use the same logging methods, same settings, etc). This makes it easier to build a standardized
build environment.

Finally, and related to the last point, Jython can be compiled to java byte code which runs like any java class file. This means you don't
have to have jython installed to use the custom tasks and your custom task, if written well, can run on a wide variety of platforms.

I think this is a reasonable way to add flexibility and additional integration points to Ant builds.

Author: Ed Taekema
URL:  http://www.fishandcross.com/articles/AntTasksWithJython.html

