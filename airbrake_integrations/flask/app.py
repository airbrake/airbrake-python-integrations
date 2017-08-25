from airbrake import Airbrake
from flask import got_request_exception


class AirbrakeApp(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        project_id = app.config.get('AIRBRAKE_PROJECT_ID', None)
        api_key = app.config.get('AIRBRAKE_API_KEY', None)
        host = app.config.get('AIRBRAKE_HOST', None)
        environment = app.config.get('AIRBRAKE_ENVIRONMENT', None)
        if project_id and api_key:
            self.ab = Airbrake(
                project_id, api_key, host, environment=environment
            )
            got_request_exception.connect(self.process_exception, sender=app)

    def process_exception(self, *args, **kwargs):
        if not self.ab:
            return
        self.ab.notify(kwargs["exception"])
