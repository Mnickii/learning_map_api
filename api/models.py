from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_pic_url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    contributions = db.relationship('Contribution', backref='contributor', lazy='dynamic', cascade='all, delete-orphan')


class ResourceContribution(db.Model):
    __tablename__ = 'ResourceContributions'

    resourceContributions_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.String)
    tags = db.Column(db.String, nullable=False)
    links = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

