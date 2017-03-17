import mock

from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from django.conf import settings

from ab.django.middleware import AirbrakeNotifierMiddleware
from airbrake.notifier import Airbrake

settings.configure(
  DATABASES={
    'default': {
      'NAME': ':memory:',
      'ENGINE': 'django.db.backends.sqlite3',
      'TEST_NAME': ':memory:',
    },
  },
  AIRBRAKE={
    'PROJECT_ID': "project123",
    'API_KEY': "key123",
    'HOST': 'https://custom-hostname.io',
    'TIMEOUT': 2,
    'ENVIRONMENT': "debug",
  }
)


class AirbrakeTestCase(TestCase):

  def setUp(self):
    self.ab_middleware = AirbrakeNotifierMiddleware()
    self.request = HttpRequest()
    self.response = HttpResponse()

  @mock.patch.object(Airbrake, "notify")
  def test_middleware_exception(self, notify):
    exception = PermissionDenied("test_err")
    self.ab_middleware.process_exception(self.request, exception)
    exception = notify.call_args[0][0]
    self.assertTrue(isinstance(exception, PermissionDenied))