__author__ = 'Ognjen'
from flask import Blueprint, jsonify, request
import models
from models import db
from models import User
api = Blueprint('api', __name__)

@api.route("/users/", methods=['GET'])
def get_users():
    return jsonify({"users" : [u.to_json() for u in User.query.all()]})

@api.route("/users/<int:id>/friends/", methods=['GET'])
def get_users_friends(id):
    return jsonify({"users" : ["list of users"]})

@api.route("/users/<int:id>/fof/", methods=['GET'])
def get_users_friends_of_friends(id):
    return jsonify({"users" : ["list of users"]})

@api.route("/users/<int:id>/suggested/", methods=['GET'])
def get_users_suggested_friends(id):
    return jsonify({"users" : ["list of users"]})

@api.route("/users/<int:id>", methods=['GET'])
def get_user(id):
    u = User.query.get_or_404(id)
    return jsonify(u.to_json())

@api.route("/users/", methods=['POST'])
def new_user():
    #u = User.from_json(request.json)
    #db.session.add(u)
    #db.session.commit()
    return jsonify({})

@api.route("/users/<int:id>", methods=['PUT'])
def edit_user(id):

    #u = User.query.get_or_404(id)
    #u.from_json(request.json)
    #db.session.add(u)
    #db.session.commit()
    return jsonify({})

@api.route("/users/<int:id>", methods=['DELETE'])
def delete_user(id):
    #u = User.query.get_or_404(id)
    #db.session.delete(u)
    #db.session.commit()
    return jsonify({})
