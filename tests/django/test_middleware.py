import os
import mock

from django.http import HttpRequest, HttpResponse
from django.test import TestCase, override_settings
from django.core.exceptions import PermissionDenied

from airbrake_integrations.django.middleware import AirbrakeNotifierMiddleware
from airbrake.notifier import Airbrake


class AirbrakeMiddlewareTestCase(TestCase):

    def setUp(self):
        # django.setup()
        self.ab_middleware = AirbrakeNotifierMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

    @mock.patch.object(Airbrake, "notify")
    def test_middleware_exception(self, notify):
        exception = PermissionDenied("test_err")
        self.ab_middleware.process_exception(self.request, exception)
        exception = notify.call_args[0][0]
        self.assertTrue(str(exception) == "test_err")
        self.assertTrue(isinstance(exception, PermissionDenied))
