"""
This is a standalone client that listens messages from JMS 
"""
from java.io import BufferedReader, InputStreamReader
from java.lang import System
from java.util import Properties
from javax.jms import TopicConnectionFactory, MessageListener, Session
from javax.naming import InitialContext, Context
import time

class TopicListener(MessageListener):

    def go(self):
        props = Properties()
        props.put(Context.INITIAL_CONTEXT_FACTORY,"com.sun.appserv.naming.S1ASCtxFactory")
        props.put(Context.PROVIDER_URL,"iiop://127.0.0.1:3700")

        context = InitialContext(props)
        tfactory = context.lookup("jms/MyConnectionFactory")

        tconnection = tfactory.createTopicConnection('receiver', 'receiver')
        tconnection.setClientID('myClientId:recv')
        tsession = tconnection.createTopicSession(False, Session.AUTO_ACKNOWLEDGE)

        subscriber = tsession.createDurableSubscriber(context.lookup("jms/MyFirstTopic"), 'mysub')

        subscriber.setMessageListener(self)

        tconnection.start()

        while True:
            time.sleep(1)
        # context.close()
        # tconnection.close()

    def onMessage(self, message):
        print message.getText()

TopicListener().go()
