from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import time
import sys

class Client(LineReceiver):

    def connectionMade(self):
        print(time.time())

    def dataReceived(self, data):
        print('message_version: {0}'.format(data))
        for i in range(0,len(data)-8):
            if data[i:i+7] == b'version':
                print('PREFIX: {0}, hex: {1}'.format(data[0:i], data[0:i].hex()))
                return
        


class ClientFactory(ClientFactory):
    protocol = Client

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)



assert len(sys.argv) == 2
addr, port = sys.argv[1].split(':')
def main(reactor):
    factory = ClientFactory()
    reactor.connectTCP(addr, int(port), factory)
    return factory.done

if __name__ == '__main__':
    task.react(main)
