from django.conf import settings
try:
    # MiddlewareMixin is not available on older versions of Django
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from airbrake import Airbrake


class AirbrakeNotifierMiddleware(MiddlewareMixin):
    """Send an error to airbrake for all exceptions"""

    def __init__(self, *args, **kwargs):
        super(AirbrakeNotifierMiddleware, self).__init__(*args, **kwargs)
        self.enabled = False
        if hasattr(settings, 'AIRBRAKE') \
                and not settings.AIRBRAKE.get('DISABLE', False):
            self.enabled = True
            project_id = settings.AIRBRAKE.get('PROJECT_ID', None)
            api_key = settings.AIRBRAKE.get('API_KEY', None)
            host = settings.AIRBRAKE.get('HOST', None)
            timeout = settings.AIRBRAKE.get('TIMEOUT', None)
            environment = settings.AIRBRAKE.get('ENVIRONMENT', None)
            self.ab = Airbrake(project_id, api_key, host, timeout,
                               environment=environment)

    def process_exception(self, request, exception):
        if self.enabled:
            self.ab.notify(exception)


class AirbrakeStatusMiddleware(MiddlewareMixin):
    """Send an error to airbrake on 4x/5x response status codes"""
    pass
