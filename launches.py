from json import loads
from requests import get
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_envvar('LAUNCHES_DEV_ENV')

@app.route('/')
def index():
    res = get("https://api.spacexdata.com/v3/launches")
    data = loads(res.text)
    return render_template("launches.html", data=data)

if __name__ == '__main__':
    app.run()
