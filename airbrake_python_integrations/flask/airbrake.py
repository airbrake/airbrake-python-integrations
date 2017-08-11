from airbrake import Airbrake


class AirbrakeApp(object):
    def __init__(self, config):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        if hasattr(app.config, 'AIRBRAKE') \
                and not app.config.AIRBRAKE.get('DISABLE', False):
            self.enabled = True
            project_id = app.config.AIRBRAKE.get('PROJECT_ID', None)
            api_key = app.config.AIRBRAKE.get('API_KEY', None)
            host = app.config.AIRBRAKE.get('HOST', None)
            timeout = app.config.AIRBRAKE.get('TIMEOUT', None)
            environment = app.config.AIRBRAKE.get('ENVIRONMENT', None)
            self.ab = Airbrake(project_id, api_key, host, timeout,
                               environment=environment)
