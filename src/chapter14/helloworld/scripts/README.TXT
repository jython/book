The connection factory @ jms/MyConnectionFactory needs to have a property
called "ClientId" with some unique string value to ensure that messages are not
dropped if there are no subscribers.

imqjmsra.jar is located in glassfish v2's :

    GLASSFISH_HOME/lib/install/applications/jmsra/imqjmsra.jar

The rest of the JAR files required are found in :

    GLASSFISH_HOME/lib/


