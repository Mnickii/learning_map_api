from flask_testing import TestCase

from learning_map_api.api import create_flask_app
from learning_map_api.api.models import db, User, Resource, Idea, Skill, Tag, Link


class BaseTestCase(TestCase):

    def create_app(self):
        self.app = create_flask_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        return self.app

    def setUp(self):
        db.drop_all()
        db.create_all()

        # create test user with three contributions
        self.user1 = User(
            user_pic_url='www.pic.com/1/',
            name='larry'
        )

        self.resource = Resource(
            title="Python testing",
            description="tdd is fun",
        )
        self.resource.contributed_by = self.user1

        self.tag = Tag(
            title="Python"
        )
        self.tag.resource_tag = self.resource

        self.tag2 = Tag(
            title="testing"
        )
        self.tag2.resource_tag = self.resource

        self.link = Link(
            url="http://www.python.com"
        )
        self.link.resource_link = self.resource

        self.idea = Idea(
            title="Assessments",
            description="add links to skill assessment",
        )
        self.idea.contributed_by = self.user1
        self.tag2.idea_tag = self.idea

        self.skill = Skill(
            title="setup Flask",
            description="valuable skill to have",
        )
        self.skill.contributed_by = self.user1

        # create test user with one contribution
        self.user2 = User(
            user_pic_url='www.pic.com/2/',
            name='Dan'
        )

        self.resource2 = Resource(
            title="Angular2 testing",
            description="test before code is fun",
        )
        self.resource2.contributed_by = self.user2

        self.link2 = Link(
            url="http://www.angular.com"
        )
        self.link2.resource_link = self.resource2

        # create test user with no contribution
        self.user3 = User(
            user_pic_url='www.pic.com/3/',
            name='Delores'
        )

        db.session.add_all([self.user1, self.user2, self.user3,
                            self.resource, self.resource2,
                            self.idea, self.skill])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
