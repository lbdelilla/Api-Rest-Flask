import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, UserFavChar


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all() 
    userList = list(map(lambda obj : obj.serialize(), users ))

    response_body = {
        "msg": " This is the list of users ",
        "results" : userList
    }

    return jsonify(response_body), 200

@app.route("/user/<int:id>", methods = ["GET"])
def user_by_id(id):
    user = db.get_or_404(User, id)
    result = user.serialize()
    response_body = {"msg" : "ok",
                     "result": result }
    return jsonify(response_body), 200


@app.route("/user/<int:id>", methods = ["DELETE"])
def delete_user(id):
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    
    return jsonify("Ok"), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all() 
    charactersList = list(map(lambda obj : obj.serialize(), characters ))

    response_body = {
        "msg": " This is the list of characters ",
         "total_records": len(result),
        "results" : charactersList
    }

    return jsonify(response_body), 200  

@app.route("/characters/<int:id>")
def character_by_id(id):
    character = db.get_or_404(Characters, id)
    result = character.serialize()
    response_body = {"msg" : "ok",
                     "result": result }
    return jsonify(response_body), 200  


@app.route('/user', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    user = User(email = body["email"], password= body["password"], is_active = True)
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": " The new user has been created correctly "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['POST'])
def create_characters():
    body = json.loads(request.data)
    characters = Characters(name = body["name"], status = body["status"], species= body["species"], gender = body["gender"])
    db.session.add(characters)
    db.session.commit()

    response_body = {
        "msg": " The new character has been created correctly "
    }

    return jsonify(response_body), 200 

@app.route('/user/favorites-characters/<int:user_id>', methods=['GET'])
def get_user_fav_char(user_id):
    favorites = db.get_or_404(UserFavChar, user_id)
    result = favorites.serialize()
    response_body = {"msg" : "ok",
                     "total_records": len(result),
                     "result": result }
    return jsonify(response_body), 200  


@app.route('/user/favorites/characters', methods=['POST'])
def create_user_fav_char():
    request_body = request.get_json()
    favorite = UserFavChar(user_id = request_body["user_id"], 
                           characters_id = request_body["characters_id"])
    db.session.add(favorite)
    db.session.commit()
    return jsonify(request_body), 200

@app.route('/favorites', methods=['GET'])
def get_user_fav():
    favorites = UserFavChar.query.all() 
    result = list(map(lambda obj : obj.serialize(), favorites ))

    response_body = {"msg" : "ok",
                     "total_records": len(result),
                     "result": result }

    return jsonify(response_body), 200  

@app.route("/user/favorites-characters/<int:user_id>", methods = ["DELETE"])
def delete_user_fav(user_id):
    favorites1 = UserFavChar.query.get(user_id)
    if favorites1 is None:
        raise APIException('Favorites not found', status_code=404)
    db.session.delete(favorites1)
    db.session.commit()
    
    return jsonify("Ok"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
