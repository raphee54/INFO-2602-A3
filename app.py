from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///a3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True # use false for production
db = SQLAlchemy(app)

@app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)

# When the Flask app is shutting down, close the database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

from A_3.models import Anime

@app.route("/")
def hello():
    return '<h1>Hello<h1>'

@app.route("/anime")
def animesList():
    records = Anime.query.order_by(Anime.name.asc()).all()
    return render_template('index.html', anime_list = records)
    
@app.route("/anime/<id>")
def anime(id):
    record = Anime.query.get(id)
    return render_template('detail.html', anime = record)


