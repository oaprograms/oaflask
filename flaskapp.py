import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import api
import models
from models import db
import codecs

app = Flask(__name__)
app.register_blueprint(api.api)

app.config.from_pyfile('flaskapp.cfg')

db.init_app(app)


#db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route('/initdb/')
def initdb():
    db.create_all()
    return 'db.create_all() succeeded'

@app.route('/initdata/')
def initdata():
    with codecs.open('data.txt', "r", "utf-8") as f:
        lines = f.read().split('\n')
        for line in lines:
            if line.strip():
                u = models.User().from_csv(line)
                db.session.add(u)
                db.session.commit()
    return 'data init succeeded'


@app.route('/dropdb/')
def dropdb():
    db.drop_all()
    return 'db.drop_all() succeeded'


if __name__ == '__main__':
    app.run()
