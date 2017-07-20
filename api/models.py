from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SerializerMixin(object):
    """
    Contains the serialize method to convert objects to a dictionary
    """

    def serialize(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns
                if column.name not in ['idea_id', 'resource_id']}


# Shows the many to many relationship between Ideas and Tags
idea_tag = db.Table('idea_tag',
                    db.Column('idea_id', db.Integer, db.ForeignKey(
                        'Ideas.id'), nullable=False),
                    db.Column('tags_id', db.Integer, db.ForeignKey(
                        'Tags.id'), nullable=False),
                    db.PrimaryKeyConstraint('idea_id', 'tags_id'))

# Shows the many to many relationship between Resource and Tags
resource_tag = db.Table('resource_tag',
                        db.Column('resource_id', db.Integer, db.ForeignKey(
                            'Resources.resource_id'), nullable=False),
                        db.Column('tags_id', db.Integer, db.ForeignKey(
                            'Tags.id'), nullable=False),
                        db.PrimaryKeyConstraint('resource_id', 'tags_id'))


class Idea(db.Model, SerializerMixin):
    """
    The Idea Model
    """

    __tablename__ = "Ideas"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship("Tag", backref="idea_tag",
                           lazy="dynamic", cascade='all, delete-orphan')
    status = db.Column(db.String(20), default="pending")
    owner_id = db.Column(db.String, nullable=False)
    description = db.Column(db.String(140))
    tags = db.relationship("Tag", secondary="idea_tag",
                           backref="ideas", lazy="dynamic")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")

    def __repr__(self):
        return '<Idea %r>' % self.title


class Tag(db.Model, SerializerMixin):
    """
    The Tag Model
    """

    __tablename__ = "Tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<Tag %r>' % self.tag


class Resource(db.Model, SerializerMixin):
    """
    The Resources Model
    """

    __tablename__ = "Resources"

    resource_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    owner_id = db.Column(db.String, nullable=False)
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")
    tags = db.relationship("Tag", secondary="resource_tag",
                           backref="resources", lazy="dynamic")
    links = db.relationship("Link", backref="resource_link", lazy="dynamic")

    def __repr__(self):
        return '<Resource %r>' % self.title


class Skill(db.Model, SerializerMixin):
    """
    The Skill Model
    """

    __tablename__ = "Skills"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")
    owner_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Skill %r>' % self.title


class Link(db.Model, SerializerMixin):
    """
    The Link Model
    """

    __tablename__ = "Links"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("Resources.resource_id"))

    def __repr__(self):
        return '<Link %r>' % self.url


class Path(db.Model, SerializerMixin):
    """
    To define fields for a learning path/role
    """
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Path %r>' % self.name
