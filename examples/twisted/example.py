from twisted.internet import protocol, reactor, endpoints
from airbrake_python_integrations.twisted.observer import AirbrakeLogObserver


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        raise Exception("A gremlin in the system received data: %s" % data)
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

ab = AirbrakeLogObserver(settings)

server_address = "tcp:1234"
endpoints.serverFromString(reactor, server_address).listen(EchoFactory())
print("Running example airbrake echo server on %s" % server_address)
reactor.run()
