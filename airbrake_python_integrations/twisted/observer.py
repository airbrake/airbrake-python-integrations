from airbrake import Airbrake
from airbrake.notifier import build_error
from twisted.logger import globalLogPublisher, Logger


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
                           environment=environment)

        log = Logger()
        globalLogPublisher.addObserver(self.event_observer)

    def event_observer(self, event):
        if not event.get('isError', False) or not 'failure' in event or not self.ab:
            return
        import pdb
        pdb.set_trace()

        error = build_error(
            event["failure"],
            message=event["failure"].getErrorMessage()
        )
        notice = self.ab.build_notice(error)

        self.ab.notify(notice)
