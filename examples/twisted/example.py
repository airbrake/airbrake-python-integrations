import unittest

from twisted.internet import protocol, reactor, endpoints
from twisted.logger import globalLogBeginner, Logger
from airbrake_integrations.twisted.observer import AirbrakeLogObserver


class Echo(protocol.Protocol):
    log = Logger()

    def dataReceived(self, data):
        try:
            raise Exception("A gremlin in the system received data")
        except:
            self.log.failure("Error")
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()


settings = {
    "AIRBRAKE": {
        "PROJECT_ID": 1234,
        "API_KEY": "1234567890asdfghjkl"
    }
}

server_address = "tcp:1234"
endpoints.serverFromString(reactor, server_address).listen(EchoFactory())
print("Running example airbrake echo server on %s" % server_address)

observers = [AirbrakeLogObserver(settings)]

globalLogBeginner.beginLoggingTo(observers, redirectStandardIO=False)

reactor.run()
