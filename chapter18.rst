Chapter 18: Deployment Targets
++++++++++++++++++++++++++++++

Deployment of Jython applications varies from container to container.  However, they are all very similar and usually allow deployment of WAR file or exploded directory web applications.  Deploying to "the cloud" is a different scenario all together.  Some cloud environments have typical Java application servers available for hosting, while others such as the Google App Engine, and moble run a bit differently.  In this chapter, we'll discuss how to deploy web based Jython applications to a few of the more widely used Java application servers.  We will also cover deployment of Jython web applicaitons to the Google App Engine and mobile devices.  While many of the deployment scenarios are quite similar, this chapter will walk through some of the differences from container to container.

In the end, one of the most important things to remember is that we need to make jython available to our application.  There are different ways to do this, either by ensuring that the *jython.jar* file is included with the application server, or by packaging the JAR directly into each web application.  This chapter assumes that you are using the latter technique.  Placing the *jython.jar* directly into each web application is a good idea because it allows the web application to follow the Java paradigm of "deploy anywhere".  You do not need to worry whether you are deploying to Tomcat or Glassfish because the Jython runtime is embedded in your application.


Application Servers
===================

As with any Java web application, the standard web archive (WAR) files are universal throughout the Java application servers available today.  This is good because it makes things a bit easier when it comes to the "write once run everywhere" philosophy that has been brought forth with the Java name.  The great part of using Jython for deployment to application servers is just that, we can harness the technologies of the JVM to make our lives easier and deploy a Jython web application to any application server in the WAR format with very little tweaking.

If you have not yet used Django or Pylons on Jython, then you may not be aware that the resulting application to be deployed is in the WAR format.  This is great because it leaves no assumption as to how the application should be deployed.  All WAR files are deployed in the same manner according to each application server.  This section will discuss how to deploy a WAR file on each of the three most widely used Java application servers.  Now, all application servers are not covered in this section mainly due to the number of servers available today.  Such a document would take more than one section of a book no doubt.  However, you should be able to follow similar deployment instructions as those discussed here for any of the application servers available today for deploying Jython web applications in the WAR file format.

Tomcat
------

Arguably the most widely used of all Java application servers, Tomcat offers easy management and a small footprint compared to some of the other options available.  Tomcat will plug into most IDEs that are in-use today, so you can manage the web container from within your development environment.  This makes it handy to deploy and undeploy applications on-the-fly.  For the purposes of this section, I've used Netbeans 6.7, so there may be some references to it.

To get started, download the Apache Tomcat server from the site at http://tomcat.apache.org/.  Tomcat is constantly evolving, so I'll note that when writing this book the deployment procedures were targeted for the 6.0.20 release.  Once you have downloaded the server and placed it into a location on your hard drive, you may have to change permissions.  I had to use the *chmod +x* command on the entire apache-tomcat-6.0.20 directory before I was able to run the server.  You will also need to configure an administrative account by going into the */conf/tomcat-users.xml* file and adding one.  Be sure to grant the administrative account the "manager" role.  This should look something like the following once completed.
::

    *tomcat-users.xml*
    <tomcat-users>
       <user username="admin" password="myadminpassword" roles="manager"/>
    </tomcat-users>

After this has been done you can add the installation to an IDE environment of your choice if you'd like.  For instance, if you wish to add to Netbeans 6.7 you will need to go to the "Services" tab in the navigator, right-click on servers, choose "Tomcat 6.x" option, and then fill in the appropriate information pertaining to your environment.  Once complete, you will be able to start, stop, and manage the Tomcat installation from the IDE.

Deploying Web Start
-------------------

Deploying a web-start application is as easy as copying the necessary files to a location on the web server that is accessible via the web.  In the case of Tomcat, you will need to copy the contents of your web start application to a single directory contained within the "<tomcat-root>/webapps/ROOT" directory.  For instance, if you have a web-start application entitled *JythonWebStart*, then you would package the JAR file along with the JNLP and HTML file for the application into a directory entitled *JythonWebStart* and then place that directory into the "<tomcat-root>/webapps/ROOT" directory.

Once the application has been copied the appropriate locations, you should be able to access it via the web if Tomcat is started.  The URL should look something like the following: *http://your-server:8080/JythonWebStart/launch.jnlp*.  Of course, you will need to user your server name and the port that you are using along with the appropriate JNLP name for your application.

Deploying a WAR or Exploded Directory Application
-------------------------------------------------

To deploy a web application to Tomcat, you have two options.  You can either use a WAR file including all content for your entire web application, or you can deploy an exploded directory application which is basically copy-and-paste for your entire web application directory structure into the "<tomcat-root>/webapps/ROOT" directory.  Either way will work the same, and we will discuss each technique in this section.

For manual deployment of a web application, you can copy either your exploded directory web application or your WAR file into the "<tomat-root>/webapps" directory.  By default, Tomcat is setup to "autodeploy" applications.  This means that you can have Tomcat started when you copy your WAR or exploded directory into the "webapps" location.  Once you've done this then you should see some feedback from the Tomcat server if you have a terminal open (or from within the IDE).  After a few seconds the application should be deployed successfully and available via the URL.  The bonus to deploying exploded directory applications is that you can take any file within the application and change it at will.  Once you are done with the changes, that file will be redeployed when you save it...this really saves on development time!

If you do not wish to have autodeploy enabled (perhaps in a production environment), then you can deploy applications on startup of the server.  This process is basically the same as "autodeploy" except any new applications that are copied into the "webapps" directory are not deployed until the server is restarted.  Lastly, you can always make use of the Tomcat manager to deploy web applications as well.  To do this, open your web browser to the index of Tomcat, usually http://localhost:8080/index.html, and then click on the "Manager" link in the left-hand menu.  You will need to authenticate at that point using your administrator password, but once you are in the console deployment is quite easy.  In an effort to avoid redundancy, I will once again redirect you to the Tomcat documentation for more information on deploying a web application via the Tomcat manager console.

Glassfish
---------

At the time of this writing, the Glassfish V2 application server was mainstream and widely used.  The Glassfish V3 server was still in preview mode but showed a lot of potential for Jython application deployment.  In this section, we will cover WAR and web-start deployment to Glassfish V2 since it is the most widely used version.  We will also discuss deployment for Django on Glassfish V3 since this version has added support for Django (and more Python web frameworks soon).  Glassfish is very similar to Tomcat in terms of deployment, but there are a couple of minor differences which will be covered in this section.

To start out, you will need to download a glassfish distribution from the site at https://glassfish.dev.java.net/.  Again, I recommend downloading V2 since it is the most widely used at the time of this writing.  Installation is quite easy, but a little more involved than that of Tomcat.  The installation of Glassfish will not be covered in this text as it varies depending upon which version you are using.  There are detailed instructions for each version located on the Glassfish website, so I will redirect you there for more information.

Once you have Glassfish installed, you can utilize the server via the command-line or terminal, or you can use an IDE just like Tomcat.  To register a Glassfish V2 or V3 installation with Netbeans 6.7, just go to the "Services" tab in the Netbeans navigator and right-click on "Servers" and then add the version you are planning to register.  Once the "Add Server Instance" window appears, simply fill in the information depending upon your environment.

There is an administrative user named "admin" that is set up by default with a Glassfish installation.  In order to change the default password, it is best to startup Glassfish and log into the administrative console.  The default administrative console port is 4848.  

Deploying Web Start
~~~~~~~~~~~~~~~~~~~

Deploying a web start application is basically the same as any other web server, you simply make the web start JAR, JNLP, and HTML file accessible via the web.  On Glassfish, you need to traverse into your "domain" directory and you will find a "docroot" inside.  The path should be similar to "<glassfish-install-loc>/domains/domain1/docroot".  Anything placed within the docroot area is visible to the web, so of course this is where you will place any web-start application directories.  Again, a typical web start application will consist of your application JAR file, a JNLP file, and an HTML page used to open the JNLP.  All of these files should typically be placed inside a directory appropriately named per your application, and then you can copy this directory into docroot.

WAR File and Exploded Directory Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again, there are a variety of ways to deploy an application using Glassfish.  Let's assume that you are using V2, you have the option to "hot deploy" or use the Glassfish Admin Console to deploy your application.  Glassfish will work with either an exploded directory or WAR file deployment scenario.  By default, the Glassfish "autodeploy" aption is turned on, so it is quite easy to either copy your WAR or exploded directory application into the autodeploy location to deploy.  If the application server is started, it will automatically start your application (if it runs without issues).  The autodeploy directory for Glassfish V2 resides in the location "<glassfish-install-loc>/domains/domain1/autodeploy".

Glassfish v3 Django Deployment
------------------------------

The Glassifish V3 server has some capabilities built into it to help facilitate the process of deploying a Django application.  In the future, there will also be support for other Jython web frameworks such as Pylons.


Other Java Application Servers
------------------------------

If you have read through the information contained in the previous sections, then you have a fairly good idea of what it is like to deploy a Jython web application to a Java application server.  There is no difference between deploying Jython web applications and Java web applications for the most part.  You must be sure that you include *jython.jar* as mentioned in the introduction, but for the most part deployment is the same.  However, I have run into cases with some application servers such as JBoss where it wasn't so cut-and-dry to run a Jython application.  For instance, I have tried to deploy a Jython servlet application on JBoss application server 5.1.0 GA and had lots of issues.  For one, I had to manually add *servlet-api.jar* to the application because I was unable to compile the application in Netbeans without doing so...this was not the case with Tomcat or Glassfish.  Similarly, I had issues trying to deploy a Jython web application to JBoss as there were several errors that had incurred when the container was scanning *jython.jar* for some reason.

All in all, with a bit of tweaking and perhaps an additional XML configuration file in the application, Jython web applications will deploy to *most* Java application servers.  The bonus to deploying your application on a Java application server is that you are in complete control of the environment.  For instance, you could embed the *jython.jar* file into the application server lib directory so that it was loaded at startup and available for all applications running in the environment.  Likewise, you are in control of other necessary components such as database connection pools and soforth.  If you deploy to another service that lives in "the cloud", you have very little control over the environment.  In the next section, we'll study one such environment by Google which is known as the Google App Engine.  While this "cloud" service is an entirely different environment than your basic Java web application server, it contains some nice features that allow one to test applications prior to deployment in the cloud.

Google App Engine
=================

The new kid on the block, at least for the time of this writing, is the Google App Engine.  Fresh to the likes of the Java platform, the Google App Engine can be used for deploying applications written in just about any language that runs on the JVM, Jython included.  The App Engine went live in April of 2008, allowing Python developers to begin using it's services to host Python applications and libraries.  In the spring of 2009, the App Engine added support for the Java platform.  Along with support of the Java language, most other languages that run on the JVM will also deploy and run on the Google App Sever, including Jython.  It has been mentioned that more programming languages will be supported at some point in the future, but at the time of this writing Python and Java were the only supported languages.

The App Engine actually runs a slimmed-down version of the standard Java library.  You must download and develop against the Google App Engine SDK for Java in order to ensure that your application will run in the environment.  You can download the SDK by visiting this link: http://code.google.com/appengine/downloads.html along with viewing the extensive documentation available on the Google App Engine site.  The SDK comes complete with a web server that can be used for testing your code before deploying, and several demo applications ranging from easy JSP programs to sophisticated demos that use Google authentication.  No doubt about it, Google has done a good job at creating an easy learning environment for the App Engine so that developers can get up and running quickly.

In this section you will learn how to get started using the Google App Engine SDK, and how to deploy some Jython web applications.  You will learn how to deploy a Jython servlet application as well as a WSGI application utilizing modjy.  If you have not done so already, be sure to visit the link mentioned in the previous chapter and download the SDK so that you can follow along in the sections to come.

Please note that the Google App Engine is a very large topic.  Entire books could be written on the subject of developing Jython applications to run on the App Engine.  With that said, I will cover the basics to get up and running with developing Jython applications for the App Engine.  Once you've read through this section I suggest to go to the Google App Engine documentation for further details.

Starting with an SDK Demo
-------------------------

We will start by running the demo application known as "guestbook" that comes with the Google App Engine SDK.  This is a very simple Java application that allows one to sign in using an email address and post messages to the screen.  In order to start the SDK web server and run the "guestbook" application, open up a terminal and traverse into the directory where you expanded the Google App Engine .zip file and run the following command: ::
    
    <app-engine-base-directory>/bin/dev_appserver.sh demos/guestbook/war
    

Of course, if you are running on windows there is a corresponding .bat script for you to run that will start the web server.  Once you've issued the preceeding command it will only take a second or two before the web server starts.  You can then open a browser and traverse to *http://localhost:8080* to invoke the "guestbook" application.  This is a basic JSP-based Java web application, but we can deloy a Jython application and use it in the same manner as we will see in a few moments.  You can stop the web server by pressing "CNTRL+C".

Working with a Project
----------------------

A particular project directory structure must be followed when developing an application for the App Engine.  Eclipse has a plugin that makes it easy to generate Google App Engine projects and deploy them to the App Engine.  If interested in making use of the plugin, please visit http://code.google.com/appengine/docs/java/tools/eclipse.html to read more information and download the plugin.  In this text we will not be using Eclipse, but rather, we will make use of Netbeans 6.7 to develop a simple Jython servlet application to deploy on the App Engine.  Netbeans also has an App Engine plugin that is available on the Kenai site appropriately named *nbappengine* (http://kenai.com/projects/nbappengine).  You can either download and install the plugin according to the directions on the project website, or simply create a new Netbeans project and make use of the template provided with the App Engine SDK (<app-engine-base-directory/demos/new_project_template) to create your project directory structure.  For the purposes of this tutorial, we will make use of the *nbappengine* plugin.

In order to install the *nbappengine* plugin, you add the 'App Engine' update center to the Netbeans plugin center by choosing the *Settings* tab and adding the update center using http://deadlock.netbeans.org/hudson/job/nbappengine/lastSuccessfulBuild/artifact/build/updates/updates.xml.gz as the URL.  Once you've added the new update center you can select the *Available Plugins* tab and add all of the plugins in the "Google App Engine" category then choose *Install*.  After doing so, you can add the "App Engine" as a server in your Netbeans environment using the "Services" tab.  To add the server, point to the base directory of your Google App Engine SDK.  Once you have added the App Engine server to Netbeans then it will become an available deployment option for your web applications.

Create a new Java web project and name it *JythonGAE*.  For the deployment server, choose "Google App Engine", and you will notice that when your web application is created an additional file will be created within the *WEB-INF* directory named *appengine-web.xml*.  This is the Google App Engine configuration file for the JythonGAE application.  At this point we will need to create a couple of additional directories within our WEB-INF project directory.  We should create a *lib* directory and place *jython.jar* and *appengine-api-1.0-sdk-1.2.2.jar* into the directory.  Note that the App Engine JAR may be named differently according to the version that you are using.  We should now have a directory structure that resembles the following:

JythonGAE
    WEB-INF
        lib
            jython.jar
            appengine-api-1.0-sdk-1.2.2.jar
        appengine-web.xml
        web.xml


Now that we have the applicaton set up, it is time to begin building the actual logic.  We will need to ensure that the *PyServlet* class is initialized at startup and that all files ending in *.py* are passed to it.  As we've seen in chapter 13, this is done in the *web.xml* deployment descriptor.

::

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE web-app
         PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
        "http://java.sun.com/dtd/web-app_2_3.dtd">
    <web-app>
    
      <display-name>modjy demo application</display-name>
      <description>
         modjy WSGI demo application
      </description>
      
      <servlet>
        <servlet-name>PyServlet</servlet-name>
         <servlet-class>org.python.util.PyServlet</servlet-class>
        <init-param>
          <param-name>python.home</param-name>
          <param-value>/Applications/jython/jython2.5.0/</param-value>
        </init-param>
        
        <load-on-startup>1</load-on-startup>
      </servlet>
      
      <servlet-mapping>
        <servlet-name>PyServlet</servlet-name>
        <url-pattern>*.py</url-pattern>
      </servlet-mapping>
      
        </web-app>


The next piece of the puzzle is the actual code.  In this example, we'll make use of the same example that was used in chapter 13 with JSP and Jython.  The code below sets up two Jython servlets that perform some mathematical logic, and a JSP to display the results.

::

    *add_numbers.py*
    import javax
    class add_numbers(javax.servlet.http.HttpServlet):
        def doGet(self, request, response):
            self.doPost(request, response)
        def doPost(self, request, response):
            x = request.getParameter("x")
            y = request.getParameter("y")
            if not x or not y:
                sum = "<font color='red'>You must place numbers in each value box</font>"
            else:
                try:
                    sum = int(x) + int(y)
                except ValueError, e:
                    sum = "<font color='red'>You must place numbers only in each value box</font>"
            request.setAttribute("sum", sum)
            dispatcher = request.getRequestDispatcher("testJython.jsp")
            dispatcher.forward(request, response)
            
    *add_to_page.py*
    import java, javax, sys

    class add_to_page(javax.servlet.http.HttpServlet):
        def doGet(self, request, response):
            self.doPost(request, response)
            
        def doPost(self, request, response):
            addtext = request.getParameter("p")
            if not addtext:
                addtext = ""
                
            request.setAttribute("page_text", addtext)
            dispatcher = request.getRequestDispatcher("testJython.jsp")
            dispatcher.forward(request, response)
            
    *testjython.jsp*
    
    <%@page contentType="text/html" pageEncoding="UTF-8"%>
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
    <%@ taglib prefix="c" uri="http://java.sun.com/jstl/core" %>
    
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>Jython JSP Test</title>
        </head>
        <body>
            <form method="GET" action="add_to_page.py">
                <input type="text" name="p">
                <input type="submit">
            </form>
            <br/>
                <p>${page_text}</p>
            <br/>
            <form method="GET" action="add_numbers.py">
                <input type="text" name="x">
                +
                <input type="text" name="y">
                =
                ${sum}
                <br/>
                <input type="submit" title="Add Numbers">
            </form>
        </body>
    </html>


That's it, now you can deploy the application to your Tomcat environment and it should run without any issues.  You can also choose to deploy to the Google App Engine SDK web server to test for compatability.


Deploy Modjy to GAE
-------------------

We can easily deploy WSGI applications using Jython's modjy API as well.  To do so, you need to add an archive of the Jython *Lib* directory to your WEB-INF project directory.  According to the modjy website, you need to obtain the source for Jython, then zip the *Lib* directory and place it into another directory along with a file that will act as a pointer to the zip archive.  The modjy site names the directory *python-lib* and names the pointer file *all.pth*.  This pointer file can be named anything as long as the suffix is *.pth*.  Inside the pointer file you need to explicitly name the zip archive that you had created for the *Lib* directory contents.  Let's assume you named it lib.zip, in this case we will put the text "lib.zip" without the quotes into the *.pth* file.  Now if we add the modjy *demo_app.py* demonstration application to the project then our directory structure should look as follows:

modjy_app
    demo_app.py
    WEB-INF
        lib
            jython.jar
            appengine-api-1.0-sdk-1.2.2.jar
        python-lib
            lib.zip
            all.pth
   
Now if we run the application using Tomcat it should run as expected.  Likewise, we can run it using the Google App Engine SDK web server and it should provide the expected results.

Summary
-------

The Google App Engine is certainly an important deployment target for Jython.  Google offers free hosting for smaller applications, and they also base account pricing on bandwidth.  No doubt that it is a good way to put up a small site, and possibly build on it later.  Most importantly, you can deploy Django, Pylons, and other applications via Jython to the App Engine by setting up your App Engine applications like the examples I had shown in this chapter.


Mobile
======

Conclusion
==========