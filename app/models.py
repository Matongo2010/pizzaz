from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Order(db.Model):
    __tablename__ ='order'
    id = db.Column(db.Integer, primary_key=True)

    pepperonni = db.Column(db.String(30))
    mushrooms = db.Column(db.String(30))
    peppers = db.Column(db.String(30))
    sauce = db.Column(db.String(30))
    crust = db.Column(db.String(30))
    order_total = db.Column(db.Integer)

    ordertime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
