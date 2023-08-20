"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, Character, Planet

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

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(list(map(lambda user: user.serialize(), users))), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("Debes enviar informacion en el body", status_code=400)
    if "username" not in body:
        raise APIException("Debes enviar tu username", status_code=400)
    if "email" not in body:
        raise APIException("Debes enviar tu email", status_code=400)
    if "password" not in body:
        raise APIException("Debes enviar tu contraseña", status_code=400)
    new_user = User(username = body['username'], email = body['email'], password = body['password'], is_active = True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route("/people", methods=["GET"])
def get_people():
    people = Character.query.all()
    return jsonify(list(map(lambda person: person.serialize(), people))), 200

@app.route("/character/<int:character_id>", methods=["GET"])
def get_single_people(character_id):
    person = Character.query.get(character_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify(list(map(lambda planet: planet.serialize(), planets))), 200

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route("/user/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify(list(map(lambda favorite: favorite.serialize(), favorites))), 200

@app.route("/user/<int:user_id>/favorite/character/<int:character_id>", methods=["POST"])
def add_favorite_character(user_id, character_id):
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite:
        return jsonify({"msg": "Character already in favorites"}), 400
    new_favorite = Favorite(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route("/user/<int:user_id>/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(user_id, character_id):
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite character not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted"}), 200

@app.route("/user/<int:user_id>/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        return jsonify({"msg": "Planet already in favorites"}), 400
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route("/user/<int:user_id>/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
