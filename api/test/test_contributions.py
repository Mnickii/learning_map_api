from flask import json
import unittest

from learning_map_api.api.test.base import BaseTestCase
from learning_map_api.api.models import (
    db, Resource, Idea, Skill, Tag, Link
)


class TestUserContributions(BaseTestCase):

    def setUp(self):
        # inherit setUp method from BaseTestCase
        BaseTestCase.setUp(self)

        # create test user with three contributions
        self.user1_id = '-Kabc'

        self.resource = Resource(
            title="Python testing",
            description="tdd is fun",
            owner_id=self.user1_id
        )

        self.tag = Tag(
            tag="Python"
        )
        self.tag.resource_tag = self.resource

        self.tag2 = Tag(
            tag="testing"
        )
        self.tag2.resource_tag = self.resource

        self.link = Link(
            url="http://www.python.com"
        )
        self.link.resource_link = self.resource

        self.idea = Idea(
            title="Assessments",
            description="add links to skill assessment",
            owner_id=self.user1_id
        )
        self.tag2.idea_tag = self.idea

        self.skill = Skill(
            title="setup Flask",
            description="valuable skill to have",
            owner_id=self.user1_id
        )

        # create test user with one contribution
        self.user2_id = '-Kdef'

        self.resource2 = Resource(
            title="Angular2 testing",
            description="test before code is fun",
            owner_id=self.user2_id
        )

        self.link2 = Link(
            url="http://www.angular.com"
        )
        self.link2.resource_link = self.resource2

        db.session.add_all([self.resource, self.resource2,
                            self.idea, self.skill])
        db.session.commit()

    # skip this test until authorization is implemented
    @unittest.skip("Skipping since authorization is not implemented yet")
    def test_fetching_contributions_by_unauthorised_user(self):
        '''
        Test that an unauthorized gets a 401 error when consuming the user
        contributions endpoint
        '''
        response = self.client.get(
            '/api/v1/contributions/unauthorized'
        )
        self.assert401(response)

        # check that error message is in the response
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_json['message'], 'Unauthorized')

    def test_fetching_contributions_by_authorised_user(self):
        '''
        Test that an authorized user with contributions gets a 200 status code
        when consuming the user contributions endpoint
        '''
        response = self.client.get(
            '/api/v1/contributions/{}'.format(self.user1_id)
        )
        self.assert200(response)

        # check that the number of contributions is 3 for user1
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(response_json['contributions']), 3)

        # check that the response json contains an expected value
        self.assertTrue(
            any(contribution.get('title') == "Python testing"
                for contribution in response_json['contributions'])
        )

        # check that the response_json resources and ideas contain tags and
        # links
        for contribution in response_json['contributions']:
            if contribution['category'] == 'resource':
                test_resource = contribution
                break
        for contribution in response_json['contributions']:
            if contribution['category'] == 'idea':
                test_idea = contribution
                break
        self.assertTrue('tags' in test_resource and 'links' in test_resource)
        self.assertTrue('tags' in test_idea and 'links' not in test_idea)

        # check that the current user is the owner of the contributions
        self.assertTrue(
            all(contribution.get('owner_id') == str(self.user1_id)
                for contribution in response_json['contributions'])
        )

        # check that the number of contributions is 1 for user2
        response = self.client.get(
            '/api/v1/contributions/{}'.format(self.user2_id)
        )
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(response_json['contributions']), 1)

        # check that the response json does not contain an unexpected value
        self.assertFalse(
            any(contribution.get('title') == "Fake contribution title"
                for contribution in response_json['contributions'])
        )

    def test_fetching_contributions_when_none_exist(self):
        '''
        Test that an authorized user with no contributions gets a 200 status
        code and a message when consuming the user contributions endpoint
        '''
        response = self.client.get(
            '/api/v1/contributions/{}'.format('no_contributions')
        )
        self.assert200(response)

        # check that the contributions key is null and that a message exists
        response_json = json.loads(response.data.decode('utf-8'))
        with self.assertRaises(KeyError):
            response_json['contributions']
        self.assertEqual(response_json['message'],
                         'You do not have any contributions yet')
