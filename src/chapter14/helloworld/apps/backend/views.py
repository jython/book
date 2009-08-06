from com.sun.enterprise.connectors.work import CommonWorkManager
from django.http import HttpResponse
from django.shortcuts import render_to_response
from javax.jms import Session, DeliveryMode, Message
from javax.jms import TopicConnection, TopicSession
from javax.naming import InitialContext
from javax.resource.spi.work import Work, WorkListener
import datetime, time

from pylogger import LogWrapper

logger = LogWrapper()

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


class WorkUnit(Work):
    """
    This is an implementation of the Work interface.
    """
    def __init__(self, job_id):
        self.job_id = job_id

    def release(self):
        logger.warn("[%d] Glassfish asked the job to stop quickly" % self.job_id)

    def run(self):
        for i in range(20):
            logger.info("[%d] just doing some work" % self.job_id)

def index(request):
    #  The threadpool name is 
    pool_name = 'backend-workers'

    wm = CommonWorkManager(pool_name)
    listener = SimpleWorkListener()
    wm_created = False
    if wm:
        wm_created = True

    num_jobs = 5
    for i in range(num_jobs):
        work = WorkUnit(i)
        wm.scheduleWork(work, -1, None, listener)

    # check the listener
    while len(listener.completed) < num_jobs:
        logger.info("Found %d jobs completed" % len(listener.completed))
        time.sleep(0.1)

    return render_to_response('backend/index.html', \
             {'wm': wm, \
              'wm_created': wm_created, \
              'listener': listener})


