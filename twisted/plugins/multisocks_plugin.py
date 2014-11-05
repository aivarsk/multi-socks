from twisted.internet import reactor, protocol
from twisted.application import service, internet

from twisted.protocols.socks import SOCKSv4

class MultiSOCKSv4(SOCKSv4):
    def __init__(self, interface, whitelist):
        SOCKSv4.__init__(self, None, reactor)
        self.interface = interface
        self.whitelist = whitelist

    def _allow(self):
        ''' Check client IP against whitelist.
            Reads a file on every call to allow whitelist modifications while proxy is running.
            TODO: SOCKSv5 + login/pass would be a better idea
        '''
        if not self.whitelist:
            return True
        try:
            allowed = open(self.whitelist).read()
        except:
            # XXX: No whitelist -> allow all
            return True
        return self.transport.getPeer().host in allowed

    def connectionMade(self):
        if self._allow():
            SOCKSv4.connectionMade(self)
        else:
            self.transport.loseConnection()

    def connectClass(self, host, port, klass, *args):
        return protocol.ClientCreator(reactor, klass, *args) \
            .connectTCP(host, port ,bindAddress=(self.interface, 0))

class MultiSOCKSv4Factory(protocol.Factory):
    def __init__(self, interface, whitelist):
        self.interface = interface
        self.whitelist = whitelist

    def buildProtocol(self, addr):
        return MultiSOCKSv4(self.interface, self.whitelist)

def parseAddr(addr):
    try:
        interface, port = addr.split(':')
        return interface, int(port)
    except ValueError:
        raise ValueError('Invalid proxy address "%s", must be in "IP:port" format' % (addr))


def addrList(val):
    return [parseAddr(x) for x in val.split(',')]

addrList.coerceDoc = 'Must be a comma-seperated list of IP:port'

from twisted.python import usage

class Options(usage.Options):
    synopsis = '-a <ip1:port1,ip2:port2,...> -w <whitelist file>'
    optParameters = [
        ['addr', 'a', [('127.0.0.1', 1080)], None, addrList],
        ['whitelist', 'w', None, None, None],
    ]

from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'multi-socks'
    description = 'SOCKSv4 proxy for servers with multiple IPs'
    options = Options

    def makeService(self, config):
        application = service.MultiService()
        for interface, port in config['addr']:
            server = internet.TCPServer(port, MultiSOCKSv4Factory(interface, config['whitelist']), interface=interface)
            application.addService(server)
        return application

serviceMaker = ServiceMaker()
