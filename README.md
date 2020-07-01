# launches_spacex
[Flask](https://pypi.org/project/Flask/): Request SpaceX Launches Data (Unofficial Repo)

![capture]

## Virtual Environment

A Python virtual environment helps prevent changes to _system Python_ which would render an OS unstable. For example, if a Python module requires a previous version of a dependency, which _system Python_ also uses, and then changes such an existing dependency to another version, system instability can result. So, a Python virtual environment can help contain Python development within its own sandbox to help prevent it from knocking the swing set over or tilting the merry-go-round. For developers, virtual environments can become a system security measure of sorts.

Below, is an example of virtual environment creation:

```shell
user_foo@foo_host:~/Desktop$ python3 -m venv foo
user_foo@foo_host:~/Desktop$ cd foo
user_foo@foo_host:~/Desktop/foo$ ls -l
total 20
drwxrwxr-x 2 user_foo user_foo 4096 Jul  1 10:11 bin
drwxrwxr-x 2 user_foo user_foo 4096 Jul  1 09:30 include
drwxrwxr-x 3 user_foo user_foo 4096 Jul  1 09:30 lib
lrwxrwxrwx 1 user_foo user_foo    3 Jul  1 09:30 lib64 -> lib
-rw-rw-r-- 1 user_foo user_foo   69 Jul  1 10:10 pyvenv.cfg
drwxrwxr-x 3 user_foo user_foo 4096 Jul  1 10:10 share
$ source bin/activate
(foo) user_foo@foo_host:~/Desktop/foo$
```

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

Flask will indicate which address to load in a web browser. Notice that the debugger was activated based on the instruction in the `.cfg` file.

```bash
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

Then load `http://127.0.0.1:5000/` in a web browser.

## launches.py

`launches.py` is a Flask app which imports `flask.Flask()`, `flask.render_template()`, `json.loads()` and `requests.get()` modules.

 - `app = Flask(__name__)` instantiates Flask class
 - `app.config.from_envvar('LAUNCHES_DEV_ENV')` sets a specific environmental variable for configuration.
 - `@app.route('/')` is a decorator which modifies the `index()` function, and declares a route. Whenever a user loads the root URL `/`, the `index()` function is executed.
 - `requests.get("https://api.spacexdata.com/v3/launches")` requests a JSON blob from the SpaceX API.
 - `data = json.loads(res.text)` assigns the blob to a local variable
 - `render_template("launches.html", data=data)` renders the `launches.html` template which uses a [Jinja2 for loop](http://jinja.pocoo.org/docs/2.10/templates/#for) to iterate through a list of launches

```py
if __name__ == '__main__':
    app.run()
```

The block above has to do with running the app as a standalone module. If this script was imported into another Python app, its `__name__` value would be `launches` instead of `__main__`.

```python
import json
from requests import get
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_envvar('LAUNCHES_DEV_ENV')

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
 - `{{ i.flight_number }}` demos Jinja2 handlebars (or mustache syntax) used to pass values from the SpaceX API to the template.

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

## Alternate Start-up

The following shell script will force debugger activation, and, if a template is modified, it will reload:

### launches.sh

```bash
export FLASK_APP=launches.py
export FLASK_DEBUG=1
export TEMPLATES_AUTO_RELOAD=1
flask run
```

[capture]: https://github.com/nick3499/launches_spacex/blob/master/screen_capture.png
