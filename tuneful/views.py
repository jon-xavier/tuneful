from flask import render_template, Response

from tuneful import app

from database import session

import decorators
import models
import json

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def get_songs():
    songs = session.query(models.Song).all()
    
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

