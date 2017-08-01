import json

import pytest

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

        self.header = {
            "Authorization": "valid_token",
        }

    # skip this test until authorization is implemented
    @pytest.mark.skip(reason="Authorization is not implemented yet")
    def test_fetching_user_contributions_by_unauthorised_user(self):
        '''
        Test that an unauthorized gets a 401 error when consuming the user
        contributions endpoint
        '''
        response = self.client.get(
            '/api/v1/contributions/?user=-Kabc',
            headers={"Authorization": "invalid_token"}
        )
        self.assert401(response)

        # check that error message is in the response
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_json['error'], 'Unauthorized')

    def test_fetching_contributions_of_user_with_three_contribution(self):
        '''
        Test that an authorized user gets valid responses when
        fetching user contributions for a user with three contribution
        '''
        response = self.client.get(
            '/api/v1/contributions/?user={}'.format(self.user1_id),
            headers=self.header
        )
        self.assert200(response)

        # check that the number of contributions is 3 for user1
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(response_json['contributions']), 3)

        # check that user1's resource contribution has two tags and a link
        for contribution in response_json['contributions']:
            if contribution['contribution_type'] == 'resource':
                self.assertTrue(len(contribution['tags']) == 2)
                self.assertTrue(
                    contribution['description'] == 'http://www.python.com')

        # check that the response json contains an expected value
        self.assertTrue(
            any(contribution.get('title') == "Python testing"
                for contribution in response_json['contributions'])
        )

        # check that the response_json ideas contain tags
        for contribution in response_json['contributions']:
            if contribution['contribution_type'] == 'idea':
                test_idea = contribution
                break
        self.assertTrue('tags' in test_idea)

        # check that the current user is the owner of the contributions
        self.assertTrue(
            all(contribution.get('user_id') == str(self.user1_id)
                for contribution in response_json['contributions'])
        )

    def test_fetching_contributions_of_user_with_one_contribution(self):
        '''
        Test that an authorized user gets valid responses when
        fetching user contributions for a user with one contribution
        '''
        # check that the number of contributions is 1 for user2
        response = self.client.get(
            '/api/v1/contributions/?user={}'.format(self.user2_id),
            headers=self.header
        )
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(response_json['contributions']), 1)

        # check that the response json does not contain an unexpected value
        self.assertFalse(
            any(contribution.get('title') == "Fake contribution title"
                for contribution in response_json['contributions'])
        )

    def test_fetching_user_contributions_when_none_exist(self):
        '''
        Test that an authorized user with no contributions gets a 200 status
        code and a message when consuming the user contributions endpoint
        '''
        response = self.client.get(
            '/api/v1/contributions/?user={}'.format('-Knocontributions'),
            headers=self.header
        )
        self.assert200(response)

        # check that the contributions key is null and that a message exists
        response_json = json.loads(response.data.decode('utf-8'))
        with self.assertRaises(KeyError):
            response_json['contributions']
        self.assertEqual(response_json['message'],
                         'You do not have any contributions yet')
