import uuid
import jwt
import datetime
from FreeNetflix.creds import db
from flask import Flask, Blueprint, render_template, request, jsonify
from passlib.hash import pbkdf2_sha256
bp = Blueprint("netflix", __name__)

# ADD USER
@bp.route("/user/account",methods=['POST'])
def SignUp():
    if request.method == 'POST':
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        username = request.json["username"]
        password = request.json["password"]
        hashed_pass = pbkdf2_sha256.hash(password)
        username_duplicate_check = db.users.find_one({"username" : username})
        if not username_duplicate_check:
            db.users.insert_one(
                {
                    "firstname" : firstname,
                    "lastname" : lastname,
                    "username" : username,
                    "password" : hashed_pass,
                    "myList" : [],
                    "token" : str(uuid.uuid4())
                }
            )
        else:
            return jsonify({"status" : 404, "message" : "username already present"})
        return jsonify({"status" : 200, "message" : "user successfully added"})    

# LOGIN USER        
@bp.route("/user/account/login", methods=['POST'])
def Login():
    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]
        find_user = db.users.find_one({"username" : username})
        if find_user:
            hashed_pass = find_user["password"]
            if pbkdf2_sha256.verify(password,hashed_pass):
                user = {
                    "firstname" : find_user['firstname'],
                    "lastname" : find_user['lastname'],
                    "username" : find_user['username'],
                    "myList" : find_user['myList'],
                    "token" : find_user['token']
                }
                token = jwt.encode({"bearer" : user, "exp" : datetime.datetime.utcnow() + datetime.timedelta(days=7)}, "DaMNsimPLeSecREtKEy")
                print(token)
                return jsonify({"status" : 200,"token" : str(token)})
        print('error')
        return jsonify({"status" : 404, "message" : "username or password is incorrect"})