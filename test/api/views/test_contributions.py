import json

from learning_map_api.test.base import BaseTestCase
from learning_map_api.api.models import (
    db, Contribution, Tag, ContributionType
)


class ContributionsTestCase(BaseTestCase):

    def setUp(self):
        # inherit setUp method from BaseTestCase
        BaseTestCase.setUp(self)

        # create test user with three contributions
        self.user1_id = '-Kabc'

        resource_type = ContributionType(id="-Kres", name="resource")

        self.resource = Contribution(
            id="-Kpqr",
            title="Python testing",
            description="http://www.python.com",
            user_id=self.user1_id
        )
        self.resource.contribution_type = resource_type

        self.tag = Tag(
            id="-Kstu",
            name="Python"
        )
        self.resource.tags.append(self.tag)

        self.tag2 = Tag(
            id="-Kvwx",
            name="testing"
        )
        self.resource.tags.append(self.tag2)

        idea_type = ContributionType(id="-Kide", name="idea")

        self.idea = Contribution(
            id="-Kuvw",
            title="Assessments",
            description="add links to skill assessment",
            user_id=self.user1_id
        )
        self.idea.contribution_type = idea_type

        self.idea.tags.append(self.tag2)

        skill_type = ContributionType(id="-Kski", name="skill")

        self.skill = Contribution(
            id="-Kngo",
            title="setup Flask",
            description="valuable skill to have",
            user_id=self.user1_id
        )

        self.skill.contribution_type = skill_type

        # create test user with one contribution
        self.user2_id = '-Kdef'

        self.resource2 = Contribution(
            id="-Kre2",
            title="Angular2 testing",
            description="http://www.angular.com",
            user_id=self.user2_id
        )

        self.resource2.contribution_type = resource_type

        db.session.add_all([self.resource, self.resource2,
                            self.idea, self.skill])
        db.session.commit()

    def test_view_all_contributions(self):

        response = self.client.get('/api/v1/contributions',
                                   )
        self.assert200(response)
