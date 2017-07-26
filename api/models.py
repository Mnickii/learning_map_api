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


#many to many relationship between contributions and tags
contribution_tag = db.Table('contribution_tag',
                    db.Column('contribution_id', db.String, db.ForeignKey(
                        'Contribution.id'), nullable=False),
                    db.Column('tag_id', db.String, db.ForeignKey(
                        'Tag.id'), nullable=False))


class ContributionType(db.Model, SerializerMixin):

    __tablename__ = "ContributionType"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '<ContributionType %r>' % self.name


class Tag(db.Model, SerializerMixin):
    """
    The Tag Model
    """

    __tablename__ = "Tag"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<Tag %r>' % self.name


class Contribution(db.Model, SerializerMixin):

    __tablename__ = "Contribution"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.String, nullable=False)
    approver_id = db.Column(db.String)
    tags = db.relationship("Tag", secondary="contribution_tag", backref="contributions",
                           lazy="dynamic")
    contribution_type_id = db.Column('contribution_type_id', db.String,
                                  db.ForeignKey('ContributionType.id'))
    status = db.Column(db.String(20), default="pending")

    def __repr__(self):
        return '<Contribution %r>' % self.title


class Path(db.Model, SerializerMixin):
    """
    To define fields for a learning path/role
    """
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Path %r>' % self.name
