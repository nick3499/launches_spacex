# launches_spacex
Flask: Request SpaceX Data: Launches (Unofficial Repo)

![capture]

## launches.sh

 - In a Unix-like terminal emulator, run `$ sudo bash launches.sh`.
 - `export FLASK_APP=launches.py` sets sets the `FLASK_APP` environment variable to `launches.py` which then launches with the `flask run` command string.
 - `export FLASK_ENV=development` sets [debug mode](http://flask.pocoo.org/docs/1.0/config/#environment-and-debug-features)

```sh
#!/bin/bash

export FLASK_APP=launches.py
export FLASK_ENV=development
flask run
```

```sh
$ sudo bash launches.sh
 * Serving Flask app "launches.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

Then load this URL in a common Web browser --> `http://127.0.0.1:5000/`

## launches.py

`launches.py` is a Flask app which imports `Flask`, `render_template`, `json` and `requests` modules.

 - `app = Flask(__name__) ` instantiates Flask
 - `@app.route('/')` is a decorator which modifies the `index()` function  
 - `requests.get("https://api.spacexdata.com/v3/launches")` requests a JSON blob from the SpaceX API
 - `json.loads(res.text)` assigns the blob to a local variable
 - `render_template("launches.html", data=data)` renders the `launches.html` template which uses a [Jinja2 for loop](http://jinja.pocoo.org/docs/2.10/templates/#for) to iterate through a list of launches

```py
if __name__ == '__main__':
    app.run(debug=True)
```

The block above has to do with running this app as a standalone module.

```py
import json
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    res = requests.get("https://api.spacexdata.com/v3/launches")
    data = json.loads(res.text)
    return render_template("launches.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
```

## launches.html

`launches.html` is a template which features Jinja2 template engine syntax, e.g. `{{ i.mission_name }}`.

 - `{% for i in data %} ... {% endfor %}` iterates the template through a list of launches
 - `{{ i.flight_number }}` demos Jinja2 handlebars or mustache syntax which is used to pass values from the SpaceX API to the template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Launches | SpaceX</title>
  <style>
    div {
      padding: 10px;
      margin: 10px;
      background-color: #BBFFFF;
      box-shadow: 5px 5px 5px #D8D8D8;
    }
  </style>
</head>
<body>
  <h1>Launches | SpaceX</h1>
  <hr>
  {% for i in data %}
  <div>
    <h3>Mission</h3>
    <table>
      <tr><td>Mission patch:</td><td><img src="{{ i.links.mission_patch_small }}"></td></tr>
      <tr><td>Flight number:</td><td>{{ i.flight_number }} ({{ i.launch_date_local[0:10] }})</td></tr>
      <tr><td>Name:</td><td>{{ i.mission_name }}</td></tr>
    </table>
    <h3>Rocket</h3>
    <table>
      <tr><td>Name:</td><td>{{ i.flight_number }}</td></tr>
      <tr><td>Type:</td><td>{{ i.mission_name }}</td></tr>
    </table>
    <h3>Payload</h3>
    <table>
      <tr><td>Type:</td><td>{{ i.rocket.second_stage.payloads.0.payload_type }}</td></tr>
      <tr><td>ID:</td><td>{{ i.rocket.second_stage.payloads.0.payload_id }}</td></tr>
      <tr><td>Customer(s):</td><td>{{ ', '.join(i.rocket.second_stage.payloads.0.customers) }}</td></tr>
      <tr><td>Nationality:</td><td>{{ i.rocket.second_stage.payloads.0.nationality }}</td></tr>
      <tr><td>Manufacturer:</td><td>{{ i.rocket.second_stage.payloads.0.manufacturer }}</td></tr>
    </table>
    <h3>Orbit</h3>
    <table>
      <tr><td>Type:</td><td>{{ i.rocket.second_stage.payloads.0.orbit }}</td></tr>
      <tr><td>Ref. sys.:</td><td>{{ i.rocket.second_stage.payloads.0.orbit_params.reference_system }}</td></tr>
      <tr><td>Regime:</td><td>{{ i.rocket.second_stage.payloads.0.orbit_params.regime }}</td></tr>
    </table>
    <h3>Links</h3>
    <ul>
      <li><a href="{{ i.links.article_link }}">Article</a></li>
      <li><a href="{{ i.links.wikipedia }}">Wikipedia</a></li>
      <li><a href="{{ i.links.video_link }}">Video</a></li>
    </ul>
    <h3>Details</h3>
    <tr><td>Details:</td><td>{{ i.details }}</td></tr>
  </div>
  {% endfor %}
</body>
</html>
```

[capture]: https://github.com/nick3499/launches_spacex/blob/master/spacex-launches.png
