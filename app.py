# Dependency Libraries
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime
from dotenv import load_dotenv
import pytz

# Dependency Files/Var
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from config import JWT_SECRET_KEY

load_dotenv()

est_timezone = pytz.timezone('US/Eastern')
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

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

# Sign up endpoint


@app.route('/signup', methods=['POST'])
def signUp():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    # Finds first existing username and email from JSON payload, if none - return none
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)).first()

    if existing_user:
        return jsonify({'message': 'User Already Exists'}), 409

    new_user = User(
        username=username,
        email=email
    )
    new_user.password = data.get('password')  # Calls setter to hash password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User Successfully Created'}), 201


@app.route('/signin', methods=['POST'])
def signIn():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Finds first existing username and email from JSON payload, if none - return none
    existing_user = User.query.filter_by(username=username).first()

    if not existing_user or not existing_user.check_password(password):
        return jsonify({'message': 'Invalid Credentials'}), 401

    access_token = create_access_token(identity=existing_user.id)

    return jsonify(access_token=access_token), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
