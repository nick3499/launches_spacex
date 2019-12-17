# launches_spacex
[Flask](https://pypi.org/project/Flask/): Request SpaceX Launches Data (Unofficial Repo)

![capture]

## launches.sh

```bash
export LAUNCHES_DEV_ENV=launches.cfg
python3 launches.py
```
`LAUNCHES_DEV_ENV` sets path to this app's env config file.

## launches.cfg

```bash
DEBUG = True
```

Then load `http://127.0.0.1:5000/` in a web browser.

## launches.py

`launches.py` is a Flask app which imports `flask.Flask`, `flask.render_template`, `json` and `requests` modules.

 - `app = Flask(__name__)` instantiates Flask class
 - `@app.route('/')` is a decorator which modifies the `index()` function, and declares a route. Whenever a user loads the root URL `/`, the `index()` function is executed.
 - `requests.get("https://api.spacexdata.com/v3/launches")` requests a JSON blob from the SpaceX API
 - `data = json.loads(res.text)` assigns the blob to a local variable
 - `render_template("launches.html", data=data)` renders the `launches.html` template which uses a [Jinja2 for loop](http://jinja.pocoo.org/docs/2.10/templates/#for) to iterate through a list of launches

```py
if __name__ == '__main__':
    app.run()
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
    app.run()
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
    <h3>{{ i.mission_name }}</h3>
    <table>
      <tr><td>Mission patch:</td><td><img src="{{ i.links.mission_patch_small }}"></td></tr>
      <tr><td>Flight number:</td><td>{{ i.flight_number }} ({{ i.launch_date_local[0:10] }})</td></tr>
      <tr><td>Details:</td><td>{{ i.details }}</td></tr>
      <tr><td>Launch site:</td><td>{{ i.launch_site.site_name_long }}</td></tr>
    </table>
    <h3>Rocket</h3>
    <table>
      <tr><td>Name:</td><td>{{ i.rocket.rocket_name }}</td></tr>
      <tr><td>Type:</td><td>{{ i.rocket.rocket_type }}</td></tr>
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
    <table>
      <tr><td><a href="{{ i.links.video_link }}" target="_blank">Video</a></td></tr>
      <tr><td><a href="{{ i.links.flickr_images[0] }}" target="_blank">Image</a></td></tr>
      <tr><td><a href="{{ i.links.presskit }}" target="_blank">Presskit [PDF]</a></td></tr>
      <tr><td><a href="{{ i.links.article_link }}" target="_blank">Article</a></td></tr>
      <tr><td><a href="{{ i.links.wikipedia }}" target="_blank">Wikipedia</a></td></tr>
    </table>
  </div>
  {% endfor %}
</body>
</html>
```

## Alternative Start Up

A startup shell script is recommended over a `.flaskenv` file. Unexpected results were experienced with a `.flaskenv` file. A shell script could contain the following:

```sh
export FLASK_APP=launches
export FLASK_ENV=development
flask run
```

`$ bash launches.sh`

[capture]: https://github.com/nick3499/launches_spacex/blob/master/screen_capture.png
