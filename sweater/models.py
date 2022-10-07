from datetime import datetime
from flask_login import UserMixin
from sweater import db




class Direction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(50), nullable=False)
    ed_form = db.Column(db.String(100), nullable=False)
    subjects = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Integer, nullable=True)
    paid = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Direction %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    min_score = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Subject %r>' % self.id


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    vuzopedia_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<University %r>' % self.id


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Log %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment %r>' % self.id


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Boolean, default=True, nullable=False)
    comment_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Like %r>' % self.id


class Ranks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), default=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)   # if user_score > score than user can have that rank

    def __repr__(self):
        return '<Rank %r>' % self.id
