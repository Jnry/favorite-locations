from flask import Flask, render_template, session, request, json, abort, g
import requests

import config
import database
import flapi

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = database.MySQL()
    g.db.connect(config.production_db)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

app.config.update(
    DEBUG=True,
)

@app.route('/')
def index():
    """index page"""
    return render_template("index.html")

api = flapi.init_api(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
