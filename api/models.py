from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_pic_url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    ideas = db.relationship('Idea', backref='contributed_by',
                            lazy='dynamic', cascade='all, delete-orphan')
    resources = db.relationship(
        'Resource', backref='contributed_by', lazy='dynamic',
        cascade='all, delete-orphan'
    )
    skills = db.relationship(
        'Skill', backref='contributed_by', lazy='dynamic',
        cascade='all, delete-orphan'
    )


class Idea(db.Model):

    __tablename__ = "Ideas"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship("Tag", backref="idea_tag",
                           lazy="dynamic", cascade='all, delete-orphan')
    status = db.Column(db.String(20), default="pending")
    contributor_id = db.Column(
        db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

    def __repr__(self):
        return '<Idea %r>' % self.title


class Resource(db.Model):

    __tablename__ = "Resources"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    owner_id = db.Column(db.Integer)
    description = db.Column(db.String(140))
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship("Tag", backref="resource_tag",
                           lazy="dynamic", cascade='all, delete-orphan')
    links = db.relationship("Link", backref="resource_link",
                            lazy="dynamic", cascade='all, delete-orphan')
    contributor_id = db.Column(
        db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

    def __repr__(self):
        return '<Resource %r>' % self.title


class Skill(db.Model):

    __tablename__ = "Skills"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(20), default="pending")
    contributor_id = db.Column(
        db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

    def __repr__(self):
        return '<Skill %r>' % self.title


class Tag(db.Model):

    __tablename__ = "Tags"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    idea_id = db.Column(db.Integer, db.ForeignKey("Ideas.id"))
    resource_id = db.Column(db.Integer, db.ForeignKey("Resources.id"))

    def __repr__(self):
        return '<Tag %r>' % self.title


class Link(db.Model):

    __tablename__ = "Links"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("Resources.id"))

    def __repr__(self):
        return '<Link %r>' % self.url
