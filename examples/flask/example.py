from flask import Flask
from airbrake_python_integrations.flask.airbrake import AirbrakeApp

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
ab = Airbrake(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'
