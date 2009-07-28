# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from com.sun.enterprise.connectors.work import CommonWorkManager
from javax.resource.spi.work import Work, WorkManager

from javax.naming import InitialContext
from javax.jms import TopicConnection, TopicSession, TopicPublisher
from javax.jms import Session, TextMessage, DeliveryMode, Message
import datetime
from java.util import ArrayList

class WorkUnit(Work):
    """
    This is an implementation of the Work interface.
    """
    def release(self):
        print "Glassfish asked the job to stop quickly"
        pass

    def run(self):
        fout = open('c:\\tmp\\journal.log', 'a')
        for i in range(20):
            fout.write('Running work!\n')
        fout.close()

def send_jms(request):
    """
    This just grabs the JMS queue and sends a message to it.
    """
    context = InitialContext()
    tfactory = context.lookup("jms/MyConnectionFactory")

    tconnection = tfactory.createTopicConnection()
    tsession = tconnection.createTopicSession(False, Session.AUTO_ACKNOWLEDGE)
    publisher = tsession.createPublisher(context.lookup("jms/MyFirstTopic"))

    message = tsession.createTextMessage()
    msg = "Hello there buddy: %s" % datetime.datetime.now()
    message.setText(msg)
    publisher.publish(message, DeliveryMode.PERSISTENT, 
            Message.DEFAULT_PRIORITY,
            20000,
            )

    context.close()
    tconnection.close()
    return render_to_response('backend/send_jms.html', {'msg': msg})

def index(request):
    #  The threadpool name is 
    pool_name = 'backend-workers'

    wm = CommonWorkManager(pool_name)
    wm_created = False
    if wm:
        wm_created = True

    work_list = ArrayList()
    work = WorkUnit()
    work_item = wm.scheduleWork(work)
    work_list.add(work_item)
    wm.waitForAll(work_list, WorkManager.INDEFINITE);

    # Get the results
    # TODO: change this to just iterate over the work_list and get the results
    result = work_item.getResult();

    return render_to_response('backend/index.html', {'wm': wm, 'wm_created': wm_created})
