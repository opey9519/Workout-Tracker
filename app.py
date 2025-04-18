from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Table to store User data


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hashed = db.Column(db.String(60))

    @property
    def password(self):
        raise AttributeError('Password field is write-only')

    @property.setter
    def password(self, password):
        self._password_hashed = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hashed, password)

    def __repr__(self):
        return f'<User: {self.username}>'

    # Table to store list of exercises


class Exercises(db.Model):
    pass

# Table to store User's workouts


class Workouts(db.Model):
    pass

# Table to store details about workouts


class Workout_Exercises(db.Model):
    pass


if __name__ == '__main__':
    app.run()
