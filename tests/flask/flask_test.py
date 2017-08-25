import mock
import os
import unittest

from flask import Flask, got_request_exception
from requests.exceptions import RequestException

from airbrake_integrations.flask.app import AirbrakeApp
from airbrake.notifier import Airbrake


class Config(object):
    AIRBRAKE_PROJECT_ID = 123
    AIRBRAKE_API_KEY = '1234'
    AIRBRAKE_ENVIRONMENT = "test"
    DATABASE_URI = 'sqlite://:memory:'


class AirbrakeTestApp(object):

    def __init__(self, test_exception):
        self.test_exception = test_exception
        self.app = Flask("testing-app")
        self.app.config.from_object(
            'tests.flask.flask_test.Config')
        # self.app.testing = True
        self.ab = AirbrakeApp(self.app)
        self.app = self.ab.app
        self.app.add_url_rule('/', 'index', self.hello_world)

    def hello_world(self):
        raise self.test_exception
        return 'Hello, World!'


class AirbrakeTestCase(unittest.TestCase):

    def setUp(self):
        self.exception_msg = "There is a nasty gremlin in this system"
        self.exception = RequestException(self.exception_msg)
        self.test_app = AirbrakeTestApp(self.exception)
        self.client = self.test_app.app.test_client()
        got_request_exception.connect(
            self.test_app.ab.process_exception, sender=self.test_app.app
        )

    @mock.patch.object(Airbrake, "notify")
    def test_send_exception(self, notify):
        rv = self.client.get('/')
        exception = notify.call_args[0][0]
        self.assertTrue(str(exception) == self.exception_msg)
        self.assertTrue(isinstance(exception, RequestException))
