from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    users = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %s>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_day = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    characters = db.relationship('Favorite', backref='character', lazy=True)
    
    def __repr__(self):
        return '<Character %s>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_day": self.birth_day,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    population = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    planets = db.relationship('Favorite', backref='planet', lazy=True)
    
    def __repr__(self):
        return '<Character %s>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return '<Favorite %r>' % self.user_id

    def serialize(self):
        character = Character.query.filter_by(id=self.character_id).first()
        planet = Planet.query.filter_by(id=self.planet_id).first()
        if character and planet:
            return {
                "character_id": self.character_id,
                "planet_id": self.planet_id,
                "characters": character.name,
                "planets": planet.name,
            }
        if character:
            return {
                "character_id": self.character_id,
                "characters": character.name,
            }
        if planet:
            return {
                "planet_id": self.planet_id,
                "planets": planet.name,
            }
