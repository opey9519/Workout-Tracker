# Dependency Libraries
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime
from dotenv import load_dotenv
import pytz

# Dependency Files/Var
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

load_dotenv()

est_timezone = pytz.timezone('US/Eastern')
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)


# Table to store User data


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hashed = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(est_timezone))

    workouts = db.relationship('Workout', backref='user')

    @property
    def password(self):
        raise AttributeError('Password field is write-only')

    @password.setter
    def password(self, password):
        self._password_hashed = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hashed, password)

    def __repr__(self):
        return f'<User: {self.username}>'


# Table to store list of exercises
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))
    muscle_group = db.Column(db.String(60), nullable=False)

    workout_exercises = db.relationship('WorkoutExercise', backref='exercise')

# Table to store User's workouts


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scheduled_time = db.Column(db.DateTime, default=datetime.now(est_timezone))
    completed = db.Column(db.Boolean, nullable=False)
    notes = db.Column(db.String(200))

    workout_exercises = db.relationship('WorkoutExercise', backref='workout')

# Table to store details about workouts


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)


@app.route('/test_db')
def test_db():
    pass


if __name__ == '__main__':
    app.run()
