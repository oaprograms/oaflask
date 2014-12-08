__author__ = 'Ognjen'
from flask import Blueprint, jsonify, request
import models
from models import db
from models import User
from error import ValidationError
from functools import wraps, update_wrapper
from datetime import datetime
from sqlalchemy_searchable import search
from flask import make_response

api = Blueprint('api', __name__)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-cache'
        return response
    return update_wrapper(no_cache, view)

@api.route("/users/", methods=['GET'])
@nocache
def get_users():
    return jsonify({"users" : [u.to_json() for u in User.query.all()]})

@api.route("/users/search/<search_query>", methods=['GET'])
@nocache
def search_users(search_query): # TODO
    #q = search(db.session.query(User), unicode(search_query)).limit(10).all()
    q = User.query.search(unicode(search_query)).limit(10).all()
    return jsonify({"users" : [u.to_json() for u in q]})

@api.route("/users-full/", methods=['GET'])
@nocache
def get_users_full():
    return jsonify({"users" : [u.to_json(full_info=True) for u in User.query.all()]})

@api.route("/users/<int:id>", methods=['GET'])
@nocache
def get_user(id):
    u = User.query.get_or_404(id)
    return jsonify(u.to_json(full_info=True))

@api.route("/users/", methods=['POST'])
def new_user():
    u = User()
    u.from_json(request.json)
    print request.json
    db.session.add(u)
    db.session.commit()
    return jsonify({})

@api.route("/users/<int:id>", methods=['PUT'])
def edit_user(id):
    u = User.query.get_or_404(id)
    u.from_json(request.json)
    db.session.add(u)
    db.session.commit()
    return jsonify({})

@api.route("/users/<int:id>", methods=['DELETE'])
def delete_user(id):
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({})

@api.route("/users/<int:id>/friends/", methods=['PUT'])
def add_friend(id):
    if not 'friend' in request.json:
        raise ValidationError('request should contain {friend: id}')
    models.add_friendship(id, request.json['friend'])
    #db.session.commit()
    print 'friend added ' + str((id, request.json['friend']))
    return jsonify({})

@api.route("/users/<int:id>/friends/<int:id2>", methods=['DELETE'])
def remove_friend(id, id2):
    models.remove_friendship(id, id2)
    #db.session.commit()
    print 'friend removed ' + str((id, id2))
    return jsonify({})

@api.route("/users/<int:id>/friends/", methods=['GET'])
@nocache
def get_users_friends(id):
    return jsonify({"users" : [u.to_json() for u in models.get_friends(id)]})

@api.route("/users/<int:id>/fof/", methods=['GET'])
@nocache
def get_users_friends_of_friends(id):
    return jsonify({"users" : models.get_fof(id)}) #TODO

@api.route("/users/<int:id>/suggested/", methods=['GET'])
@nocache
def get_users_suggested_friends(id):
    return jsonify({"users" : models.get_suggested(id)})


def bad_request(message):
    response = jsonify({'error':'bad request','message':message})
    response.status_code=400
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])