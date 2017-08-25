Airbrake python notifier integrations
=====================================

<img src="http://f.cl.ly/items/3Z1A202C1U2j3E1O1N0n/python%2009.19.32.jpg" width=800px>

* [Airbrake Python Integrations README](https://github.com/airbrake/airbrake-python-integrations)
* [Airbrake Python README](https://github.com/airbrake/airbrake-python)

Integrations built on top of the airbrake python notifier for quick use with popular frameworks and libraries.

### Introduction

[Airbrake](https://airbrake.io/) is an online tool that provides robust exception
tracking in any of your Python applications. In doing so, it allows you to easily
review errors, tie an error to an individual piece of code, and trace the cause
back to recent changes. The Airbrake dashboard provides easy categorization,
searching, and prioritization of exceptions so that when errors occur, your team
can quickly determine the root cause.

### Key features

This library is built on top of [Airbrake Python](https://github.com/airbrake/airbrake-python). The difference
between _Airbrake Python_ and _Airbrake Python Integrations_ is that the
`airbrake-integrations` package is just a collection of integrations
with frameworks or other libraries. The `airbrake` package is the core library
that performs exception sending and other heavy lifting.

Normally, you just need to depend on this package, select the integration you are
interested in and follow the instructions for it. If the framework or
application you use does not have an integration available, you can depend on
the `airbrake` package and ignore this package entirely.

The list of integrations that are available in this package includes:

* Django
* Flask
* Twisted

### Installation

To install airbrake-integrations, run:
```bash
pip install airbrake-integrations
```

It's highly suggested that you add the package to your `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

### Configuration

#### Django

To install the middleware and catch exceptions in your views:

- Add the following to your `settings.py` file; replacing the value with your
project's id and key:

```python
AIRBAKE = {
    "PROJECT_ID": 123,
    "API_KEY": "123abcde",
    "ENVIRONMENT": "test"
}
```

- Add the middleware to your `settings.py` file; making sure that the
airbrake middleware is at the top of the list. Django processes middleware
in order from the end of this list to start, so placing it at the end will
catch all exceptions before it.

```python
MIDDLEWARE = [
    'airbrake_integrations.django.middleware.AirbrakeNotifierMiddleware',
    ...
]
```

Note that any middleware that catches exceptions and does not allow them to
flow through will not be sent to airbrake. It's important to make sure any
middleware that also process exceptions will raise the original exception:

```python
def process_exception(self, request, exception):
    raise exception
```

An example django app can be found in /examples/django

#### Flask

To catch exceptions, use the Airbrake extension:

Make sure the airbrake configuration fields are set:
```
AIRBRAKE_PROJECT_ID = 123456
AIRBRAKE_API_KEY = '1290180gsdf8snfaslfa0'
AIRBRAKE_ENVIRONMENT = "production"
```

And then install the extension!
```python
from airbrake_integrations.flask.app import AirbrakeApp

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
ab = AirbrakeApp(app)
```

An example flask app can be found in /examples/flask

To run the example:
```bash
export FLASK_APP=example.py
flask run
```

#### Twisted

```python
from airbrake_integrations.twisted.observer import AirbrakeLogObserver
from twisted.logger import globalLogBeginner, Logger

settings = {
    "AIRBRAKE": {
        "PROJECT_ID": 1234,
        "API_KEY": "1234567890asdfghjkl"
    }
}

observers = [AirbrakeLogObserver(settings)]

globalLogBeginner.beginLoggingTo(observers, redirectStandardIO=False)

log = Logger()
try:
    raise Exception("A gremlin in the system is angry")
except:
    log.failure("Error")
```

This creates an observer that looks the `globalLogPublisher` twisted object, and checks all events for any possible exceptions.

An example flask app can be found in /examples/twisted
