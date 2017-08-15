import mock
import django

import airbrake
from airbrake.notice import Notice
from django.http import HttpRequest, HttpResponse
from django.test import TestCase, override_settings
from django.core.exceptions import PermissionDenied

from airbrake.notifier import Airbrake


class AirbrakeMiddlewareTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.response = HttpResponse()
        self.logger = airbrake.getLogger(
            api_key='fakekey', project_id='fakeprojectid')

    def view_log_exception(self, err_text, body):
        self.logger.error(err_text)
        return HttpResponse(body)

    @mock.patch.object(Airbrake, "notify")
    def test_logging_exception(self, notify):
        err_text = "Test Error"
        body = "<html><body>I am a banana.</body></html>"
        resp = self.view_log_exception(err_text, body)
        self.assertTrue(resp.content, body)
        exception = notify.call_args[0][0]
        self.assertTrue(isinstance(exception, Notice))
        self.assertEqual(exception.errors[0]["message"], err_text)
        self.assertEqual(exception.context["severity"], "error")
