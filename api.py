__author__ = 'Ognjen'
from flask import Blueprint, jsonify, request
import models
from models import db
from models import User
api = Blueprint('api', __name__)
from errors import ValidationError

@api.route("/users/", methods=['GET'])
def get_users():
    return jsonify({"users" : [u.to_json() for u in User.query.all()]})

@api.route("/users-full/", methods=['GET'])
def get_users_full():
    return jsonify({"users" : [u.to_json(full_info=True) for u in User.query.all()]})

@api.route("/users/<int:id>", methods=['GET'])
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

@api.route("/users/<int:id>/friends/", methods=['GET'])
def get_users_friends(id):
    return jsonify({"users" : ["list of users"]})

@api.route("/users/<int:id>/fof/", methods=['GET'])
def get_users_friends_of_friends(id):
    return jsonify({"users" : ["list of users"]})

@api.route("/users/<int:id>/suggested/", methods=['GET'])
def get_users_suggested_friends(id):
    return jsonify({"users" : ["list of users"]})


def bad_request(message):
    response = jsonify({'error':'bad request','message':message})
    response.status_code=400
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])