"""
This is a StompJMS client that will send messages from Jython or
CPython using STOMP and send messages to a JMS provider.  The client
supports durable message subscribers.

This module requires the python-stomp client. You need a version that
supports durable message subscribers. Obtain a copy from here :

    http://bitbucket.org/crankycoder/python-stomp/overview/
"""
import sys
import stomp
import socket
from pprint import pprint
import time
import argparse

def parse_args():
    desc ="""
Demo client for STOMP-JMS gateway.

examples: 
    
    1) Create a sender on the durable_client_id ClientId.  Subscribers
    who bind to this clientId are expected to be durable.

    stompjms -c durable_client_id -u send -p send -x send

    2) Create a durable subscriber

    stompjms -c durable_client_id -u recv -p recv -x recv -d

"""
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-c", dest='client_id', required=True, type=str, help='ClientId of the jms.TopicConnection')
    parser.add_argument("-u", dest='username', required=True, type=str, help='Username for the JMS broker')
    parser.add_argument("-p", dest='password', required=True, type=str, help='Password for the JMS broker')
    parser.add_argument("-x", dest='method', required=True, type=str, choices=['send', 'recv'], help='Transmission mode')
    parser.add_argument("-s", dest='sub_name', required=False, type=str, help='Subscription name for durable JMS subscribers')
    parser.add_argument("-t",
            dest='topic',
            default='/topic/MyFirstTopic',
            type=str,
            help='Topic name to subscribe to')

    return parser.parse_args()

class StompJMS(object):
    """
    This is a thin wrapper around python-stomp to provide a sensible 
    interface to JMS via stompconnect
    """
    def __init__(self, debug=False):
        """
        Get a STOMP object
        """
        self.serv = stomp.Stomp('localhost', 6666, debug=debug)

    def connect(self, client_id, username, password, topic, sub_name):
        self.topic = topic
        self.sub_name = sub_name
        self.serv.connect({'client-id': client_id, 'login': username, 'passcode': password})

    def disconnect(self):
        self.serv.disconnect()

    def recv(self):
        """
        Yield frames as they come in
        """
        config = {'destination': self.topic,
                  'ack': 'client'}
        if self.sub_name:
            config['durable-subscription-name']=self.sub_name

        self.serv.subscribe(config)

        while True:
            frame = self.serv.receive_frame()
            if frame.command == 'MESSAGE':
                self.serv.ack(frame)
                yield frame
            else:
                # TODO: do something with the frame here?
                pass

    def send(self, msg=None):
        if msg is None:
            msg = 'this is a test from cmdline %s' % time.time()
        self.serv.send({'destination': self.topic, 'body': msg})

if __name__ == '__main__':
    args = parse_args()

    stomper = StompJMS(debug=True)
    stomper.connect(args.client_id, args.username, args.password, args.topic, args.sub_name)
    if args.method == 'send':
        while True:
            stomper.send()
            time.sleep(5)
    else:
        msg_iter = stomper.recv()
        while True:
            print "Received: ", msg_iter.next()

