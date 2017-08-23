import sys

from airbrake import Airbrake
from airbrake.notifier import build_error
from twisted.logger import Logger, ILogObserver
from zope.interface import implementer


@implementer(ILogObserver)
class AirbrakeLogObserver(object):
    def __init__(self, settings):
        if not settings.get('AIRBRAKE', False) or \
                settings['AIRBRAKE'].get('DISABLE', False):
            return

        self.enabled = True
        project_id = settings['AIRBRAKE'].get('PROJECT_ID', None)
        api_key = settings['AIRBRAKE'].get('API_KEY', None)
        host = settings['AIRBRAKE'].get('HOST', None)
        timeout = settings['AIRBRAKE'].get('TIMEOUT', None)
        environment = settings['AIRBRAKE'].get('ENVIRONMENT', None)
        self.ab = Airbrake(project_id, api_key, host, timeout,
                           environment=environment, send_uncaught_exc=False)

    def __call__(self, event):
        if not event["log_failure"] or not self.ab:
            return

        error = build_error(
            event["log_failure"].value,
            message=event["log_failure"].getErrorMessage()
        )
        notice = self.ab.build_notice(error)

        self.ab.notify(notice)
