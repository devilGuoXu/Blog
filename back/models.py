from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_delete = db.Column(db.Boolean, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now())
    u_arts = db.relationship('Article', backref='user_art')
    u_types = db.relationship('ArticleType', backref='user_type')

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()


class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    at_name = db.Column(db.String(10), unique=True, nullable=False)
    us = db.Column(db.Integer, db.ForeignKey('user.id'))
    arts = db.relationship('Article', backref='art_tp')

    __tablename__ = 'articletype'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def dele(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Integer, db.ForeignKey('articletype.id'))
    us = db.Column(db.Integer, db.ForeignKey('user.id'))

    __tablename__ = 'article'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def dele(self):
        db.session.delete(self)
        db.session.commit()
