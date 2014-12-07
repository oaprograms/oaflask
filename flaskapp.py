import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, make_response
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
    return make_response(open('templates/index.html').read())

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route('/admin-resetdb/')
def resetdb():
    dropdb()
    initdb()
    initdata()
    return 'reset succeeded'

#@app.route('/initdb/')
def initdb():
    db.create_all()
    return 'db.create_all() succeeded'

#@app.route('/initdata/')
def initdata():
    with codecs.open('data.txt', "r", "utf-8") as f:
        lines = f.read().split('\n')
        for line in lines:
            if line.strip():
                u = models.User()
                u.from_csv(line)
                db.session.add(u)
        db.session.commit()
        for line in lines:
            if line.strip():
                id = int(line.split(';')[0])
                friend_ids = [int(f) for f in line.split(';')[-1].split(',')]
                for f in friend_ids:
                    models.add_friendship(id, f)
        db.session.commit()
    return 'data init succeeded'


#@app.route('/dropdb/')
def dropdb():
    db.drop_all()
    return 'db.drop_all() succeeded'


if __name__ == '__main__':
    app.run()
