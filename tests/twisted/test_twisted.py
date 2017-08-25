import mock
import unittest

from airbrake.notifier import Airbrake
from twisted.internet import protocol, reactor, endpoints, defer
from twisted.logger import globalLogBeginner, Logger
from twisted.test import proto_helpers

from airbrake_integrations.twisted.observer import AirbrakeLogObserver


def deep_failure(msg):
    return fail_with_traceback(msg)


def fail_with_traceback(msg):
    raise Exception(msg)


class AirbrakeTestCase(unittest.TestCase):

    def setUp(self):
        settings = {
            "AIRBRAKE": {
                "PROJECT_ID": 123,
                "API_KEY": "1234567890asdfghjkl;"
            }
        }
        self.ab = AirbrakeLogObserver(settings)

        self.exception_msg = "There is a nasty gremlin in this system"

        self.log = Logger(observer=self.ab)

    @mock.patch.object(Airbrake, "notify")
    def test_send_exception(self, notify):
        try:
            deep_failure(self.exception_msg)
        except:
            self.log.failure("Error")

        exception = notify.call_args[0][0]
        self.assertTrue(exception.errors[0]['message'] == self.exception_msg)

        func_names = ['test_send_exception',
                      'deep_failure', 'fail_with_traceback']
        exception_func_names = map((lambda trace: trace["function"]),
                                   exception.errors[0]['backtrace'])
        self.assertTrue(set(func_names) == set(exception_func_names))

    @mock.patch.object(Airbrake, "notify")
    def test_send_global_exception(self, notify):
        observers = [self.ab]
        globalLogBeginner.beginLoggingTo(observers)

        log = Logger()
        try:
            deep_failure(self.exception_msg)
        except:
            log.failure("Error")

        exception = notify.call_args[0][0]
        print("exception: %s" % exception)

        self.assertTrue(exception.errors[0]['message'] == self.exception_msg)

        func_names = ['test_send_global_exception',
                      'deep_failure', 'fail_with_traceback']
        exception_func_names = map((lambda trace: trace["function"]),
                                   exception.errors[0]['backtrace'])
        self.assertTrue(set(func_names) == set(exception_func_names))
